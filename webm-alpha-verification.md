# Verifying that a transparent WebM keeps its alpha channel

This note documents how we checked, with real commands, whether a transparent
WebM exported by the in-browser green-screen tool actually carries an alpha
channel — and where it gets lost.

Environment used for the measurements below:

- Chromium `MediaRecorder` with `video/webm;codecs=vp9` (what the tool uses).
- `ffmpeg` / `ffprobe` 9.0.1 (Gyan build).

## 1. Browser / player keeps alpha (verified)

A transparent WebM stores transparency in a separate alpha block inside the
Matroska/WebM container (the main video track reports `pix_fmt=yuv420p`; the
alpha is a second block, not an extra plane on the main track).

Two checks:

- **Visual:** render the exported `.webm` on a pure magenta (`#FF00FF`)
  background in a browser. If the magenta shows through where the subject was
  cut out, the alpha is intact. Result: the background shows through — alpha
  intact.
- **Container:** `ffprobe file.webm` reports `TAG:alpha_mode=1` on the video
  stream. Our exported sample (vp9, 2678 bytes) showed exactly that.

Verdict: in a browser or any WebM/VP9-capable player, the transparency is kept.

## 2. Default command-line decode drops alpha (verified)

`ffmpeg -i file.webm frame.png`

- Output: `pix_fmt=rgb24` — no alpha channel.
- The background corner pixel came out `[0, 0, 0]` = black.

So a default `ffmpeg` decode flattens the transparency to black. This is the
"command-line tools drop alpha" behavior.

## 3. Keeping alpha through ffmpeg (when you must re-encode)

Forcing the alpha-capable pixel format on re-encode carries `alpha_mode=1`
again:

`ffmpeg -i file.webm -vf format=yuva420p -c:v vp9 -pix_fmt yuva420p -auto-alt-ref 0 out.webm`

The output reported `TAG:ALPHA_MODE=1`. But note: the default decode path
(described in section 2) already discarded the alpha before you could re-encode,
so you must ask for it explicitly from the start.

## Practical guidance

For reliable transparency, play the file in a browser or a WebM/VP9-capable
player. If you must process it with ffmpeg, force `-pix_fmt yuva420p` and check
the result with `check_webm_alpha.py`.

## Commands (copy-paste)

```
ffprobe -v error -show_streams file.webm        # look for TAG:alpha_mode=1
ffmpeg  -i file.webm frame.png                  # default decode -> rgb24, black bg (alpha lost)
ffmpeg  -i file.webm -vf format=yuva420p -c:v vp9 -pix_fmt yuva420p -auto-alt-ref 0 out.webm
python check_webm_alpha.py file.webm            # this repo's checker
```
