#!/usr/bin/env python3
"""Check whether a WebM file carries an alpha channel.

Uses ffprobe (ships with ffmpeg). Looks at the video stream's pixel format and
the `alpha_mode` tag, which Matroska/WebM sets to 1 when the file has alpha.

Usage:
    python check_webm_alpha.py path/to/file.webm

ffprobe is taken from the PATH, or from the FFPROBE environment variable.
"""
import os
import sys
import shutil
import subprocess


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python check_webm_alpha.py <file.webm>")
        return 2

    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f"file not found: {path}")
        return 2

    ffprobe = os.environ.get("FFPROBE") or shutil.which("ffprobe")
    if not ffprobe:
        print("ffprobe not found. Install ffmpeg (ffprobe ships with it), "
              "or set the FFPROBE environment variable to its path.")
        return 2

    try:
        out = subprocess.run(
            [ffprobe, "-v", "error", "-show_streams",
             "-of", "default=noprint_wrappers=1", path],
            capture_output=True, text=True, timeout=60,
        ).stdout
    except Exception as exc:  # noqa: BLE001 - report and exit, do not crash
        print(f"ffprobe failed: {exc}")
        return 1

    pix_fmt = ""
    alpha_mode = ""
    for line in out.splitlines():
        if line.startswith("pix_fmt="):
            pix_fmt = line.split("=", 1)[1].strip()
        if line.upper().startswith("TAG:ALPHA_MODE="):
            alpha_mode = line.split("=", 1)[1].strip()

    # alpha is present if the container tags it, or the pixel format is alpha-capable
    tagged = (alpha_mode == "1")
    planar_alpha = "a" in pix_fmt
    has_alpha = tagged or planar_alpha

    print(f"file:       {path}")
    print(f"pix_fmt:    {pix_fmt or '(unknown)'}")
    print(f"alpha_mode: {alpha_mode or '(not tagged)'}")

    if planar_alpha:
        print("verdict:    alpha plane present in the pixel format (yuva/rgba) — alpha kept.")
    elif tagged and not planar_alpha:
        print("verdict:    alpha tagged (alpha_mode=1). For a WebM exported by the tool "
              "this means the alpha is present; note a command-line re-encode can leave a "
              "stale alpha_mode=1 tag with no actual alpha plane, so confirm by rendering "
              "on a colored background.")
    else:
        print("verdict:    no alpha channel detected (transparency lost on render).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
