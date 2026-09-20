# Transparent Export Format Reference

Reference notes on which export formats keep transparency (an alpha channel),
based on the free in-browser green-screen tool. All claims here are either
stated on the tool's page or verified with real commands (ffprobe / ffmpeg).

## What's in this repo

- `transparency-format-matrix.csv` — which image and video formats preserve
  transparency, and how each claim was verified.
- `webm-alpha-verification.md` — how we checked that a transparent WebM keeps
  its alpha in a browser/player, and why a default command-line decode drops it.
- `check_webm_alpha.py` — a small script that uses ffprobe to report whether a
  WebM file carries an alpha channel.

## How to use

1. Read `transparency-format-matrix.csv` for the format summary.
2. See `webm-alpha-verification.md` for the verification method and commands.
3. Run `python check_webm_alpha.py your_file.webm` (needs ffprobe on PATH) to
   check any WebM.

## License

MIT — use and adapt freely.

These notes are based on the export behavior of the free browser tool at
https://greenscreencut.com/transparent-background.
