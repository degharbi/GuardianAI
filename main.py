from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from nudenet import NudeDetector
# from moviepy import VideoFileClip, concatenate_videoclips
from moviepy.editor import VideoFileClip, concatenate_videoclips

import tempfile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    temp_input_path = f"temp_{file.filename}"
    with open(temp_input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Nudity detection and scene removal
    detector = NudeDetector()
    clip = VideoFileClip(temp_input_path)
    duration = clip.duration
    fps = clip.fps
    scene_length = 1.0  # seconds per scene to check
    safe_segments = []
    t = 0
    last_end = 0
    # Labels to treat as unsafe (nudity or bikini/swimsuit)
    unsafe_labels = set([
        "FEMALE_BREAST_EXPOSED",
        "FEMALE_GENITALIA_EXPOSED",
        "MALE_GENITALIA_EXPOSED",
        "ANUS_EXPOSED",
        "BUTTOCKS_EXPOSED",
        "FEMALE_BREAST_COVERED",
        "FEMALE_GENITALIA_COVERED",
        "BUTTOCKS_COVERED",
        "BELLY_EXPOSED"
    ])
    while t < duration:
        subclip = clip.subclip(t, min(t + scene_length, duration))
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as frame_file:
            frame_path = frame_file.name
            subclip.save_frame(frame_path, t=0)
            detections = detector.detect(frame_path)
            os.remove(frame_path)
        # If any detection label is in unsafe_labels, mark segment as unsafe
        is_unsafe = False
        for det in detections:
            label = det.get('class') or det.get('label')
            if label in unsafe_labels:
                is_unsafe = True
                break
        if not detections or not is_unsafe:
            # No nudity or bikini detected in this segment
            if last_end < t:
                safe_segments.append(clip.subclip(last_end, t))
            last_end = t
        t += scene_length
    if last_end < duration:
        safe_segments.append(clip.subclip(last_end, duration))
    if safe_segments:
        final_clip = concatenate_videoclips(safe_segments)
        temp_output_path = f"processed_{file.filename}"
        final_clip.write_videofile(temp_output_path, codec="libx264", audio_codec="aac")
    else:
        temp_output_path = temp_input_path  # If all scenes are unsafe, return original
    os.remove(temp_input_path)
    return FileResponse(temp_output_path, media_type="video/mp4", filename=f"processed_{file.filename}")

@app.get("/", response_class=HTMLResponse)
def serve_ui():
    with open("ui.html", "r") as f:
        return f.read() 