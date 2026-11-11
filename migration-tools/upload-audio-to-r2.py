#!/usr/bin/env python3
"""Upload Camelon audio from the gh-pages tree to a Cloudflare R2 bucket.

Dependency-free (Python 3 standard library only) — signs requests with
AWS Signature V4 against R2's S3-compatible endpoint.

Credentials come from the ENVIRONMENT ONLY, never from this file:
    R2_ACCOUNT_ID        Cloudflare account id
    R2_ACCESS_KEY_ID     R2 API token's access key id
    R2_SECRET_ACCESS_KEY R2 API token's secret access key
    R2_BUCKET            bucket name (default: kamelon-audio)

Usage:
    python3 upload-audio-to-r2.py [--dry-run] [--root assets] [--workers 8]

Defaults: source = ~/workspace/french/parlons-wt-ghpages, uploads every
*.mp3 under <source>/assets/ preserving its path relative to the tree
root (so `assets/pron/ll/etal.mp3` lands at key `assets/pron/ll/etal.mp3`).

Resume: before each PUT it HEADs the object and skips it when the remote
size equals the local size, so re-running after an interruption only
sends what is missing or different.
"""

import argparse
import hashlib
import hmac
import os
import sys
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

DEFAULT_SOURCE = os.path.expanduser("~/workspace/french/parlons-wt-ghpages")


def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def signing_key(secret, date, region, service):
    k = sign(("AWS4" + secret).encode("utf-8"), date)
    k = sign(k, region)
    k = sign(k, service)
    return sign(k, "aws4_request")


def request(method, url_host, path, access, secret, account_host, body=None,
            content_type=None):
    """One SigV4-signed request against the R2 endpoint. Returns (status, headers)."""
    now = datetime.now(timezone.utc)
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = now.strftime("%Y%m%d")
    region, service = "auto", "s3"
    payload_hash = hashlib.sha256(body if body is not None else b"").hexdigest()
    headers = {
        "host": account_host,
        "x-amz-content-sha256": payload_hash,
        "x-amz-date": amz_date,
    }
    if content_type:
        headers["content-type"] = content_type
    signed_headers = ";".join(sorted(headers))
    canonical = "\n".join([
        method, path, "",
        "".join(f"{k}:{headers[k]}\n" for k in sorted(headers)),
        signed_headers, payload_hash,
    ])
    scope = f"{date_stamp}/{region}/{service}/aws4_request"
    string_to_sign = "\n".join([
        "AWS4-HMAC-SHA256", amz_date, scope,
        hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
    ])
    signature = hmac.new(signing_key(secret, date_stamp, region, service),
                         string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
    headers["Authorization"] = (
        f"AWS4-HMAC-SHA256 Credential={access}/{scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )
    req = urllib.request.Request(url_host + path, data=body, method=method)
    for k, v in headers.items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.status, dict(resp.headers)
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=DEFAULT_SOURCE)
    ap.add_argument("--root", default="assets",
                    help="subdirectory of the tree to upload (default: assets)")
    ap.add_argument("--dry-run", action="store_true",
                    help="list what would be uploaded; no network calls")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    base = os.path.join(args.source, args.root)
    files = []
    for dirpath, _dirs, names in os.walk(base):
        for name in names:
            if name.lower().endswith(".mp3"):
                full = os.path.join(dirpath, name)
                key = os.path.relpath(full, args.source).replace(os.sep, "/")
                files.append((full, key))
    files.sort()
    total_mb = sum(os.path.getsize(f) for f, _ in files) / 1048576
    print(f"{len(files)} mp3 files, {total_mb:.1f} MB under {base}")

    if args.dry_run:
        for _full, key in files[:20]:
            print("  would upload:", key)
        if len(files) > 20:
            print(f"  … and {len(files) - 20} more")
        return 0

    account = os.environ.get("R2_ACCOUNT_ID")
    access = os.environ.get("R2_ACCESS_KEY_ID")
    secret = os.environ.get("R2_SECRET_ACCESS_KEY")
    bucket = os.environ.get("R2_BUCKET", "kamelon-audio")
    if not (account and access and secret):
        print("Missing R2_ACCOUNT_ID / R2_ACCESS_KEY_ID / R2_SECRET_ACCESS_KEY "
              "in the environment.", file=sys.stderr)
        return 2
    host = f"{account}.r2.cloudflarestorage.com"
    endpoint = f"https://{host}"

    def upload(item):
        full, key = item
        path = "/" + bucket + "/" + urllib.request.quote(key, safe="/")
        status, headers = request("HEAD", endpoint, path, access, secret, host)
        size = os.path.getsize(full)
        if status == 200 and int(headers.get("Content-Length", -1)) == size:
            return key, "skip"
        with open(full, "rb") as fh:
            body = fh.read()
        status, _ = request("PUT", endpoint, path, access, secret, host,
                            body=body, content_type="audio/mpeg")
        if status not in (200, 201):
            return key, f"FAIL http {status}"
        return key, "ok"

    done = {"ok": 0, "skip": 0, "FAIL": 0}
    failures = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(upload, item): item for item in files}
        for i, fut in enumerate(as_completed(futures), 1):
            key, result = fut.result()
            if result.startswith("FAIL"):
                done["FAIL"] += 1
                failures.append((key, result))
            else:
                done[result] += 1
            if i % 500 == 0:
                print(f"  {i}/{len(files)}  ok={done['ok']} skip={done['skip']} "
                      f"fail={done['FAIL']}")
    print(f"DONE ok={done['ok']} skip={done['skip']} fail={done['FAIL']}")
    for key, result in failures[:20]:
        print("  FAILED:", key, result)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
