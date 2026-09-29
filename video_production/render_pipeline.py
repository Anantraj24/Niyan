import os
import glob
import time
import subprocess
from playwright.sync_api import sync_playwright

BASE_DIR = r"E:\Niyan\video_production"
SCENES_DIR = os.path.join(BASE_DIR, "scenes")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
CLIPS_DIR = os.path.join(BASE_DIR, "clips")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
MUSIC_FILE = r"E:\Niyan\.agents\skills\brag\assets\music\happy-beats-business-moves-vol-1-by-ende-dot-app.mp3"

os.makedirs(CLIPS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

CLIPS_SPEC = [
    {"id": i, "duration": 25.0 if i < 15 else 10.0} for i in range(1, 16)
]

def render_clip(clip_id, duration):
    scene_file = os.path.join(SCENES_DIR, f"scene_{clip_id:02d}.html")
    audio_file = os.path.join(AUDIO_DIR, f"clip_{clip_id:02d}_voiced.mp3")
    final_mp4 = os.path.join(CLIPS_DIR, f"clip_{clip_id:02d}.mp4")
    
    # Temp recording dir for playwright
    temp_rec_dir = os.path.join(CLIPS_DIR, f"temp_rec_{clip_id:02d}")
    os.makedirs(temp_rec_dir, exist_ok=True)
    
    print(f"\n[Clip {clip_id:02d}/15] Recording {duration}s visual at 1080p...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=temp_rec_dir,
            record_video_size={"width": 1920, "height": 1080}
        )
        page = context.new_page()
        page.goto(f"file:///{scene_file.replace(os.sep, '/')}")
        time.sleep(duration)
        page.close()
        context.close()
        browser.close()
        
    # Find recorded webm
    recorded_webms = glob.glob(os.path.join(temp_rec_dir, "*.webm"))
    if not recorded_webms:
        raise RuntimeError(f"No webm found in {temp_rec_dir}")
    raw_video = recorded_webms[0]
    
    print(f"[Clip {clip_id:02d}/15] Muxing video and narration with ffmpeg...")
    # Convert webm and mux with audio to exact target duration
    mux_cmd = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-i", audio_file,
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-t", str(duration),
        final_mp4
    ]
    subprocess.run(mux_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    
    # Cleanup temp webm
    try:
        os.remove(raw_video)
        os.rmdir(temp_rec_dir)
    except Exception:
        pass
        
    print(f"[Clip {clip_id:02d}/15] Complete -> {final_mp4}")
    return final_mp4

def assemble_master_presentation():
    concat_list_file = os.path.join(CLIPS_DIR, "concat_list.txt")
    with open(concat_list_file, "w") as f:
        for spec in CLIPS_SPEC:
            clip_path = os.path.join(CLIPS_DIR, f"clip_{spec['id']:02d}.mp4").replace("\\", "/")
            f.write(f"file '{clip_path}'\n")
            
    raw_concat_mp4 = os.path.join(OUTPUT_DIR, "raw_presentation.mp4")
    master_mp4 = os.path.join(OUTPUT_DIR, "NIYAM-X_6_Minute_Presentation.mp4")
    poster_jpg = os.path.join(OUTPUT_DIR, "NIYAM-X_Poster.jpg")
    
    print("\nConcatenating all 15 clips into single 6-minute stream...")
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_file,
        "-c", "copy",
        raw_concat_mp4
    ]
    subprocess.run(concat_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    
    print("\nMixing subtle background soundtrack (-24dB ducked)...")
    # Loop music for 360 seconds, volume at 0.08 (-24dB), mix with speech
    mix_cmd = [
        "ffmpeg", "-y",
        "-i", raw_concat_mp4,
        "-stream_loop", "-1",
        "-i", MUSIC_FILE,
        "-filter_complex", "[1:a]volume=0.07[bg];[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", "360",
        master_mp4
    ]
    subprocess.run(mix_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    
    print(f"\nExtracting high-resolution poster frame to {poster_jpg}...")
    poster_cmd = [
        "ffmpeg", "-y",
        "-ss", "00:00:02",
        "-i", master_mp4,
        "-vframes", "1",
        "-q:v", "2",
        poster_jpg
    ]
    subprocess.run(poster_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    
    print(f"\nSUCCESS! Master Presentation generated: {master_mp4}")

if __name__ == "__main__":
    for spec in CLIPS_SPEC:
        render_clip(spec["id"], spec["duration"])
    assemble_master_presentation()
