#!/usr/bin/env python3
"""Build a new-template lesson (feliciter-style) into gh-pages and wire plan/next."""
from __future__ import annotations

import argparse
import html as html_lib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "lesson-a1-new-feliciter" / "index.html"


def esc(s: str) -> str:
    return html_lib.escape(s, quote=True)


def card(text: str) -> str:
    return f'<div class="card">{esc(text)}</div>'


def flashcard(term: str, meaning_en: str, example: str) -> str:
    return (
        '<div class="fcx" onclick="this.classList.toggle(\'fl\')"><div class="fcxi">'
        f'<div class="fcxf"><div style="font-size:16.5px;font-weight:800;color:#241f4e">{esc(term)}</div></div>'
        f'<div class="fcxf fcxb"><div style="font-size:13px;font-weight:700;color:#4a78e0">{esc(meaning_en)}</div>'
        f'<div style="font-size:13.5px;color:#333a5e;margin-top:5px;line-height:1.5">{esc(example)}</div></div>'
        "</div></div>"
    )


FC_STYLE = (
    '<style>.fcx{perspective:900px;cursor:pointer;margin-top:10px}.fcxi{position:relative;min-height:118px;'
    "transform-style:preserve-3d;transition:transform .5s}.fcx.fl .fcxi{transform:rotateY(180deg)}"
    ".fcxf{position:absolute;inset:0;backface-visibility:hidden;-webkit-backface-visibility:hidden;"
    "background:#fff;border:2px solid #e6e1f9;border-radius:16px;padding:14px;box-sizing:border-box;"
    "display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}"
    ".fcxb{transform:rotateY(180deg)}</style>"
)

MIC = (
    '<div class="nmic-wrap" style="margin-top:16px;text-align:center">'
    '<div class="nmic" role="button" aria-label="Hold to record your voice" style="width:84px;height:84px;margin:0 auto;'
    "border-radius:50%;background:linear-gradient(160deg,#7a5ff0,#4f7fe0);display:flex;align-items:center;"
    "justify-content:center;cursor:pointer;touch-action:none;user-select:none;-webkit-user-select:none;"
    'box-shadow:0 10px 22px rgba(90,70,180,.35)">'
    '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="2.5" width="6" height="11" rx="3"></rect>'
    '<path d="M5.5 11a6.5 6.5 0 0 0 13 0"></path><path d="M12 17.5V21"></path></svg></div>'
    '<div class="nmic-hint" style="margin-top:9px;font-size:12.5px;font-weight:800;color:#6a6580">'
    "Hold to record your voice</div><div class=\"nmic-play\" style=\"margin-top:10px\"></div></div>"
)


def step_shell(step: int, total: int, title: str, goal: str, body: str, last: bool = False) -> str:
    pct = int(round(100 * step / total)) if total else 0
    top = (
        f'<div class="top"><span class="x" data-x="1">×</span><div class="bar"><i style="width:{pct}%"></i></div>'
        f'<span style="font-size:12px;font-weight:800;color:#8a86a3">{step}/{total}</span></div>'
        f'<div class="goal">🎯 <b>{esc(title)}</b> · Goal: {esc(goal)}</div>'
    )
    last_attr = ' data-last="1"' if last else ""
    nav = (
        '<div class="nav"><button class="btn g" data-n="-1">Previous</button>'
        '<button class="btn" data-n="1">Next</button></div>'
    )
    if last:
        # completion uses its own nav
        return f'<div class="scr" data-step="{step}"{last_attr}><div class="fr">{body}</div></div>'
    return (
        f'<div class="scr" data-step="{step}"{last_attr}><div class="fr">{top}'
        f'<div class="pad">{body}</div>{nav}</div></div>'
    )


def grammar_html(heading: str, blurb: str, tiles: list[tuple[str, str]], examples: list[str], tip: str) -> str:
    tiles_html = "".join(
        f'<div style="background:#eef3ff;border-radius:10px;padding:7px 9px;font-size:13.5px">'
        f'<span style="color:#7a5af8;font-weight:800">{esc(a)}</span> <b>{esc(b)}</b></div>'
        for a, b in tiles
    )
    ex = "".join(f"<div style=\"margin:4px 0\">{esc(e)}</div>" for e in examples)
    return (
        f'<span class="tag">GRAMMAR</span>'
        f'<div style="font-family:Fredoka,Nunito,system-ui,sans-serif;font-size:20px;font-weight:600;color:#241f4e;'
        f'margin-top:8px;line-height:1.25">{esc(heading)}</div>'
        f'<div style="font-size:13.5px;color:#57536f;margin-top:3px;line-height:1.45">{esc(blurb)}</div>'
        f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:10px">{tiles_html}</div>'
        f'<div class="note" style="margin-top:10px"><b>Examples</b>{ex}</div>'
        f'<div class="note"><b>Good to know</b><br>{esc(tip)}</div>'
    )


def extract_template_scripts(template_html: str) -> tuple[str, str, str]:
    """Return (runtime_script, mic_script, empty) from feliciter — keep runtime+mic."""
    parts = []
    i = 0
    while True:
        a = template_html.find("<script>", i)
        if a < 0:
            break
        b = template_html.find("</script>", a)
        parts.append(template_html[a + 8 : b])
        i = b + 9
    # 0=LD+nav (we rebuild), 1=runtime, 2=mic, 3=D+PRON (we rebuild)
    return parts[1], parts[2]


def build_lesson(cfg: dict) -> None:
    tpl = TEMPLATE.read_text()
    runtime, mic = extract_template_scripts(tpl)
    head = tpl[: tpl.find("<body>")]
    head = re.sub(r"<title>[^<]*</title>", f"<title>{esc(cfg['title'])} · Camelon</title>", head)

    dir_name = cfg["dir"]
    audio_base = f"https://chichilang.com/assets/lesson-audio/{dir_name}"
    vocab1 = cfg["vocab1"]
    vocab2 = cfg["vocab2"]
    total = 9

    # --- screens ---
    opener = (
        f'<div class="scr" data-step="0"><div class="fr"><div class="pad"><div style="height:22px"></div>'
        f'<span class="tag">{esc(cfg["dossier_tag"])}</span><h1>{esc(cfg["title"])}</h1>'
        f'<div class="sub">{esc(cfg["goal"])}</div></div>'
        f'<div class="nav"><button class="btn" data-n="1">Start lesson</button></div></div></div>'
    )

    listen1 = step_shell(
        1,
        total,
        cfg["title"],
        cfg["goal"],
        f'<span class="tag">LISTENING</span><h1>Listen to the dialogue</h1>'
        f'<div class="card" style="padding:14px"><div style="font-weight:800;font-size:12px;color:#6b5bb5;margin-bottom:8px">'
        f'Dialogue</div><audio controls style="width:100%" src="{audio_base}/listening1.mp3"></audio></div>',
    )

    transcript = step_shell(
        2,
        total,
        cfg["title"],
        cfg["goal"],
        '<span class="tag">TRANSCRIPT</span><h1>Listen again, with the text</h1>'
        + "".join(card(line) for line in cfg["dialogue_lines"]),
    )

    preview = ", ".join(v["term"] for v in vocab1[:4])
    fc1 = step_shell(
        3,
        total,
        cfg["title"],
        cfg["goal"],
        f'<span class="tag">FLASHCARDS</span><h1>Learn the new words</h1>'
        f'<div class="card"><div style="font-weight:800">{esc(preview)}</div></div>'
        f'<span class="tag">FLASHCARDS</span>{FC_STYLE}'
        + "".join(flashcard(v["term"], v["en"], v["example"]) for v in vocab1),
    )

    grammar = step_shell(4, total, cfg["title"], cfg["goal"], grammar_html(**cfg["grammar"]))

    l2_body = (
        f'<span class="tag">REAL VOICE</span><h1>Listen again: real voice</h1>'
        f'<div class="card" style="padding:14px"><div style="font-weight:800;font-size:12px;color:#6b5bb5;margin-bottom:8px">'
        f'{esc(cfg.get("listening2_label", "Voice message"))}</div>'
        f'<audio controls style="width:100%" src="{audio_base}/listening2.mp3"></audio></div>'
        f'<div style="font-size:12px;font-weight:800;margin:10px 0 6px">TRANSCRIPT</div>'
        + "".join(card(line) for line in cfg["listening2_lines"])
    )
    listen2 = step_shell(5, total, cfg["title"], cfg["goal"], l2_body)

    reading_paras = "".join(f"<p style=\"margin:0 0 10px;line-height:1.45\">{esc(p)}</p>" for p in cfg["reading_paras"])
    reading = step_shell(
        6,
        total,
        cfg["title"],
        cfg["goal"],
        f'<span class="tag">READING</span><h1>{esc(cfg["reading_title"])}</h1>'
        f'<div class="card" style="padding:14px">{reading_paras}</div>',
    )

    fc2 = step_shell(
        7,
        total,
        cfg["title"],
        cfg["goal"],
        f'<span class="tag">FLASHCARDS</span><h1>More words</h1>{FC_STYLE}'
        + "".join(flashcard(v["term"], v["en"], v["example"]) for v in vocab2),
    )

    speaking = step_shell(
        8,
        total,
        cfg["title"],
        cfg["goal"],
        f'<span class="tag">SPEAKING</span><h1>Say it out loud</h1>'
        f'<div class="note" style="font-size:13.5px"><b>PROMPT</b><br>{esc(cfg["speaking_prompt"])}</div>'
        f'<div style="font-size:12px;font-weight:800;margin:10px 0 6px">MODEL ANSWER</div>'
        f'{card(cfg["speaking_model"])}{MIC}',
    )

    writing = step_shell(
        9,
        total,
        cfg["title"],
        cfg["goal"],
        f'<span class="tag">WRITING</span><h1>Write it down</h1>'
        f'<div class="note" style="font-size:13.5px"><b>PROMPT</b><br>{esc(cfg["writing_prompt"])}</div>'
        f'<textarea class="wta" rows="4" placeholder="Write your sentences here…" style="width:100%;box-sizing:border-box;'
        f'border:2px solid #e8e3f7;border-radius:18px;padding:12px;font-family:Nunito,system-ui,sans-serif;font-size:14px;'
        f'font-weight:700;color:#221d33;resize:vertical;margin:2px 0 8px"></textarea>'
        f'<div style="font-size:12px;font-weight:800;margin:10px 0 6px">MODEL TEXT</div>{card(cfg["writing_model"])}',
    )

    next_title = cfg["next"]["title"]
    complete = (
        f'<div class="scr" data-step="10" data-last="1"><div class="fr"><div class="pad">'
        f'<div class="big">🎁</div><h1 style="text-align:center">Lesson complete</h1>'
        f'<div class="sub" style="text-align:center">{esc(cfg["title"])}</div></div>'
        f'<div class="nav" style="flex-direction:column">'
        f'<button class="btn" data-next="1" style="flex:none;width:100%">Next: {esc(next_title)}</button>'
        f'<button class="btn g" data-home="1" style="flex:none;width:100%">Back to home</button>'
        f"</div></div></div>"
    )

    lid = cfg["id"]
    trk = {str(i): [["rc", f"v5:{lid}:s{i}"]] for i in range(11)}
    ld = {
        "id": lid,
        "level": cfg["level"],
        "n": cfg.get("lesson_n", 127),
        "dnum": cfg.get("dnum"),
        "dossier": cfg.get("dossier_id", lid),
        "title": cfg["title"],
        "goalFr": cfg["goal"],
        "vtitle": cfg["title"],
        "cover": cfg["cover_web"],
        "aud": {"1": f"{audio_base}/listening1.mp3", "5": f"{audio_base}/listening2.mp3"},
        "lastInDossier": True,
        "next": cfg["next"],
        "status": "COMPLETE",
        "trk": trk,
    }
    ld_js = "var LD=" + json.dumps(ld, ensure_ascii=False) + ";"
    nav_js = """
var NEXT=(LD.next&&LD.next.url)||"/";
var S=[].slice.call(document.querySelectorAll('.scr')),i=0;
if(innerWidth<500)document.body.classList.add('m');
function pget(){try{return JSON.parse(localStorage.getItem('cam_prog')||'{}')}catch(e){return{}}}function pset(o){try{localStorage.setItem('cam_prog',JSON.stringify(o))}catch(e){}}
function pres(){var p=pget();return p[LID]||(p[LID]={step:0,done:false,steps:{}})}
var LID=LD.id; function markStep(n){var p=pget();var r=p[LID]||(p[LID]={step:0,done:false,steps:{}});r.steps[n]=1;pset(p)} function stepOf(k){return +(S[k].getAttribute('data-step')||0)}
function show(n){var from=i;S.forEach(function(s,idx){s.classList.toggle('on',idx===n)});i=n;for(var s=from;s<n;s++){var a=stepOf(s),b=stepOf(s+1);if(b!==a)markStep(a)}if(n===S.length-1){markStep(stepOf(n));var rDone=pres();rDone.done=true;rDone.step=0;pset(function(){var p=pget();p[LID]=rDone;return p}())}else{var r=pres();r.step=n;pset(function(){var p=pget();p[LID]=r;return p}())}try{[].forEach.call(document.querySelectorAll('audio'),function(a){if(a.closest&&a.closest('.scr')&&!a.closest('.scr').classList.contains('on')){try{a.pause()}catch(x){}}})}catch(x){}window.scrollTo(0,0)}
document.addEventListener('click',function(e){
 var b=e.target.closest('button,[data-x]');if(!b)return;
 if(b.dataset.x){location.href='/';return}
 if(b.dataset.home){location.href='/';return}
 if(b.dataset.next){if(LD.next){try{var m=JSON.parse(localStorage.getItem('cam_lesson_choice')||'{}');m[LD.next.dossier]=LD.next.id;localStorage.setItem('cam_lesson_choice',JSON.stringify(m))}catch(x){}}if(NEXT)location.href=NEXT;return}
 if(b.dataset.n){var nx=i+parseInt(b.dataset.n,10);if(nx<0)return;if(nx>=S.length){return}show(nx);return}
});
show(pres().step||0);
"""

    # PRON + D
    pron = {}
    dobj = {}
    for v in vocab1 + vocab2:
        term = v["term"]
        slug = v["slug"]
        word_path = cfg["media_src"] / "words" / f"{slug}.mp3"
        if word_path.exists():
            pron[term] = f"{audio_base}/words/{slug}.mp3"
        dobj[term] = {
            "display": term,
            "en": v["en"],
            "fa": v["fa"],
            "es": v["es"],
            "ru": v["ru"],
            "hi": v["hi"],
            "ar": v["ar"],
            "kind": "word",
        }
    gloss_js = (
        "window.PRON=Object.assign(window.PRON||{},"
        + json.dumps(pron, ensure_ascii=False)
        + ");\n"
        "window.D=Object.assign(window.D||{},"
        + json.dumps(dobj, ensure_ascii=False)
        + ");"
    )

    body = (
        opener
        + listen1
        + transcript
        + fc1
        + grammar
        + listen2
        + reading
        + fc2
        + speaking
        + writing
        + complete
        + f"<script>{ld_js}{nav_js}</script>"
        + f"<script>{runtime}</script>"
        + f"<script>{mic}</script>"
        + f"<script>\n{gloss_js}\n</script>"
    )
    out_html = head + "<body>" + body + "</body></html>"

    # write lesson folder
    lesson_dir = ROOT / dir_name
    lesson_dir.mkdir(exist_ok=True)
    (lesson_dir / "index.html").write_text(out_html, encoding="utf-8")

    # copy media
    media_src: Path = cfg["media_src"]
    audio_dst = ROOT / "assets" / "lesson-audio" / dir_name
    words_dst = audio_dst / "words"
    words_dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(media_src / "listening1.mp3", audio_dst / "listening1.mp3")
    shutil.copy2(media_src / "listening2.mp3", audio_dst / "listening2.mp3")
    missing_audio = []
    for v in vocab1 + vocab2:
        src = media_src / "words" / f"{v['slug']}.mp3"
        if not src.exists():
            missing_audio.append(v["slug"])
            # Leave unwired per flashcard spec — do not invent TTS.
            continue
        shutil.copy2(src, words_dst / f"{v['slug']}.mp3")
    if missing_audio:
        print("WARNING: missing word audio (left unwired):", ", ".join(missing_audio))
    cover_dst = ROOT / "assets" / Path(cfg["cover_web"]).name
    shutil.copy2(media_src / "cover.jpg", cover_dst)

    print(f"Wrote {lesson_dir}/index.html")
    print(f"Audio → {audio_dst}")
    print(f"Cover → {cover_dst}")


def update_prev_next(prev_lesson_file: Path, new_next: dict) -> None:
    t = prev_lesson_file.read_text()
    m = re.search(r'"next"\s*:\s*\{[^}]+\}', t)
    if not m:
        raise SystemExit(f"no next in {prev_lesson_file}")
    new = '"next": ' + json.dumps(new_next, ensure_ascii=False)
    prev_lesson_file.write_text(t[: m.start()] + new + t[m.end() :], encoding="utf-8")
    print(f"Updated next in {prev_lesson_file}")


def insert_plan_entry(after_n: int, entry: dict) -> None:
    """Insert plan entry after the D item whose n == after_n (or index after_n if aligned)."""
    path = ROOT / "plan" / "index.html"
    html = path.read_text()
    start = html.index("const D=[")
    i = start + 8
    depth = 0
    end = None
    for j in range(i, len(html)):
        if html[j] == "[":
            depth += 1
        elif html[j] == "]":
            depth -= 1
            if depth == 0:
                end = j + 1
                break
    assert end
    raw = html[start + 8 : end]
    # Use node for safe parse/serialize to keep JS literals
    tmp_in = Path("/tmp/plan_D_in.js")
    tmp_out = Path("/tmp/plan_D_out.js")
    tmp_in.write_text("module.exports = " + raw + ";\n", encoding="utf-8")
    entry_json = json.dumps(entry, ensure_ascii=False)
    script = f"""
const D = require('{tmp_in}');
const entry = {entry_json};
let idx = D.findIndex(e => e.n === {after_n});
if (idx < 0) idx = {after_n}; // fall back to array index
D.splice(idx + 1, 0, entry);
const fs = require('fs');
fs.writeFileSync('{tmp_out}', JSON.stringify(D));
console.log('inserted at', idx + 1, 'len', D.length);
"""
    Path("/tmp/plan_insert.js").write_text(script, encoding="utf-8")
    import subprocess

    subprocess.check_call(["node", "/tmp/plan_insert.js"])
    new_D = tmp_out.read_text()
    # JSON is fine for plan D (already JSON-like)
    path.write_text(html[: start + 8] + new_D + html[end:], encoding="utf-8")
    print(f"Plan: inserted after n={after_n}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config_json")
    args = ap.parse_args()
    cfg = json.loads(Path(args.config_json).read_text())
    cfg["media_src"] = Path(cfg["media_src"])
    build_lesson(cfg)
    if cfg.get("prev_lesson_html"):
        update_prev_next(ROOT / cfg["prev_lesson_html"], cfg["self_as_next"])
    if cfg.get("after_plan_n") is not None:
        insert_plan_entry(cfg["after_plan_n"], cfg["plan_entry"])


if __name__ == "__main__":
    main()
