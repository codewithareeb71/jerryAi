from __future__ import annotations

import os
from pathlib import Path
from typing import List

try:
    from moviepy.editor import VideoFileClip, concatenate_videoclips
except Exception:
    # Fallback for moviepy installations without the editor convenience module
    try:
        from moviepy.video.io.VideoFileClip import VideoFileClip
    except Exception:
        VideoFileClip = None
    try:
        from moviepy.video.compositing.concatenate import concatenate_videoclips
    except Exception:
        concatenate_videoclips = None

try:
    from PyQt6.QtWidgets import QApplication, QFileDialog
except Exception:
    QApplication = None


def _ensure_out_path(path: str | Path | None, default_name: str) -> Path:
    if path:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        return p
    if QApplication and QApplication.instance() is not None:
        dlg = QFileDialog()
        dlg.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        fn, _ = dlg.getSaveFileName(None, "Save video", str(Path.home() / default_name))
        if fn:
            p = Path(fn)
            p.parent.mkdir(parents=True, exist_ok=True)
            return p
    p = Path.home() / default_name
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def trim_video(input_path: str, start: float, end: float, outfile: str | None = None) -> str:
    clip = VideoFileClip(input_path).subclip(start, end)
    outp = _ensure_out_path(outfile, "jerry_trim.mp4")
    clip.write_videofile(str(outp), codec="libx264", audio_codec="aac")
    clip.close()
    return str(outp)


def merge_videos(inputs: List[str], outfile: str | None = None) -> str:
    clips = [VideoFileClip(p) for p in inputs]
    final = concatenate_videoclips(clips, method="compose")
    outp = _ensure_out_path(outfile, "jerry_merged.mp4")
    final.write_videofile(str(outp), codec="libx264", audio_codec="aac")
    for c in clips:
        c.close()
    final.close()
    return str(outp)


def extract_frame(input_path: str, t: float = 1.0, outfile: str | None = None) -> str:
    clip = VideoFileClip(input_path)
    frame = clip.get_frame(t)
    from PIL import Image
    im = Image.fromarray(frame)
    outp = _ensure_out_path(outfile, "jerry_frame.png")
    im.save(outp)
    clip.close()
    return str(outp)


def create_thumbnail_from_video(input_path: str, t: float = 1.0, outfile: str | None = None, title: str | None = None) -> str:
    frame_path = extract_frame(input_path, t=t, outfile=None)
    # Use simple approach: call ai_graphics.create_thumbnail if available
    try:
        from actions.ai_graphics import create_thumbnail
        return create_thumbnail(frame_path, outfile=outfile, title=title)
    except Exception:
        return str(_ensure_out_path(outfile, "jerry_video_thumbnail.png"))
