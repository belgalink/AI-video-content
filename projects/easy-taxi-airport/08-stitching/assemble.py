#!/usr/bin/env python3
"""Assemble the Easy-Taxi Belgium ad from the 6 Seedance clips + end card.
Scales to 1080x1920, trims to tight pacing, keeps ambient audio, adds end card.
"""
import subprocess, os, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
BASE = "/home/user/AI-video-content/projects/easy-taxi-airport"
CLIPS = f"{BASE}/07-transition-videos/attempts"
OUT = f"{BASE}/09-final-output"
WORK = f"{BASE}/08-stitching/work"
os.makedirs(WORK, exist_ok=True)

# (file, start, duration) -> keep the meaningful beat of each clip
SEGMENTS = [
    ("shot1.mp4", 2.0, 3.0),   # loopt aan + begroeting
    ("shot2.mp4", 1.0, 3.0),   # valies afgeven
    ("shot3.mp4", 2.0, 3.0),   # kofferbak in
    ("shot4.mp4", 0.8, 2.5),   # snelweg
    ("shot5.mp4", 2.0, 3.0),   # aankomst Leuven
    ("shot6.mp4", 1.5, 3.5),   # thuis overhandigen
]
VF = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p"

parts = []
for i,(f,ss,dur) in enumerate(SEGMENTS):
    src = f"{CLIPS}/{f}"
    dst = f"{WORK}/seg{i:02d}.mp4"
    af = f"afade=t=in:st=0:d=0.08,afade=t=out:st={dur-0.12:.2f}:d=0.12"
    subprocess.run([FF,"-y","-loglevel","error","-ss",str(ss),"-t",str(dur),"-i",src,
        "-vf",VF,"-af",af,
        "-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p",
        "-c:a","aac","-b:a","160k","-ar","48000","-ac","2","-r","30",dst],check=True)
    parts.append(dst)

# end card: 3.0s static image with silent audio
endcard_img = f"{OUT}/attempts/endcard.png"
endcard = f"{WORK}/seg_end.mp4"
subprocess.run([FF,"-y","-loglevel","error","-loop","1","-t","3.0","-i",endcard_img,
    "-f","lavfi","-t","3.0","-i","anullsrc=channel_layout=stereo:sample_rate=48000",
    "-vf",VF,"-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p",
    "-c:a","aac","-b:a","160k","-ar","48000","-ac","2","-r","30","-shortest",endcard],check=True)
parts.append(endcard)

# concat
listfile = f"{WORK}/concat.txt"
with open(listfile,"w") as fh:
    for p in parts: fh.write(f"file '{p}'\n")
final = f"{OUT}/easy-taxi-belgium-ad-9x16.mp4"
subprocess.run([FF,"-y","-loglevel","error","-f","concat","-safe","0","-i",listfile,
    "-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p",
    "-c:a","aac","-b:a","160k","-ar","48000","-ac","2","-movflags","+faststart",final],check=True)
# report duration
out = subprocess.run([FF,"-i",final],capture_output=True,text=True).stderr
import re
m = re.search(r"Duration: ([0-9:.]+)", out)
print("FINAL:", final, "duration", m.group(1) if m else "?")
