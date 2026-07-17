#!/usr/bin/env python3
"""Clean a YouTube auto-caption VTT into readable, de-duplicated text with periodic timestamps.

Usage: python3 clean_vtt.py <path-to.vtt>
Writes <path-to.clean.txt> next to the input and prints cleaned_words / cleaned_chars.
"""
import re, sys

path = sys.argv[1]
raw = open(path, encoding="utf-8").read()

cues = []  # (start_seconds, text)
def to_sec(ts):
    h, m, s = ts.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)

blocks = raw.split("\n\n")
ts_re = re.compile(r"(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->")
tag_re = re.compile(r"<[^>]+>")
for b in blocks:
    lines = b.strip().split("\n")
    start = None
    texts = []
    for ln in lines:
        m = ts_re.search(ln)
        if m:
            start = to_sec(m.group(1))
            continue
        if ln.startswith("WEBVTT") or ln.startswith("Kind:") or ln.startswith("Language:") or ln.startswith("NOTE"):
            continue
        clean = tag_re.sub("", ln)
        clean = re.sub(r"\s+", " ", clean).strip()
        if clean:
            texts.append(clean)
    if start is not None and texts:
        # take the fullest line in the cue (rolling caption's final state)
        cues.append((start, max(texts, key=len)))

# Prefix-aware de-dup: rolling captions expand a growing line; keep the growth, drop the redundancy
final = []
for start, txt in cues:
    if final:
        prev_start, prev = final[-1]
        if txt == prev:
            continue
        if prev and txt.startswith(prev):
            final[-1] = (prev_start, txt)   # extended same line
            continue
        if prev and prev.startswith(txt):
            continue
    final.append((start, txt))

# Emit paragraphs with a timestamp every ~90s
out = []
last_stamp = -999
buf = []
def hms(sec):
    h = int(sec // 3600); m = int((sec % 3600) // 60); s = int(sec % 60)
    return f"[{h:d}:{m:02d}:{s:02d}]"
for start, txt in final:
    if start - last_stamp >= 90:
        if buf:
            out.append(" ".join(buf)); buf = []
        out.append("\n" + hms(start))
        last_stamp = start
    buf.append(txt)
if buf:
    out.append(" ".join(buf))

text = "\n".join(out)
text = re.sub(r"\n{3,}", "\n\n", text)
open(path.replace(".vtt", ".clean.txt"), "w", encoding="utf-8").write(text)
words = len(text.split())
print(f"cleaned_words={words}")
print(f"cleaned_chars={len(text)}")
