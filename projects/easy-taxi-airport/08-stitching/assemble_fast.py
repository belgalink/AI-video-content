#!/usr/bin/env python3
"""Fast-paced assembler: tight cuts + endcard. Parameterized per clip window.
Usage: edit CLIPS windows, run. Produces a punchy ~14s 9:16 ad, ambient audio kept."""
import subprocess, os, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = "/home/user/AI-video-content/projects/easy-taxi-airport"
CL = f"{ROOT}/07-transition-videos/approved"
OUT = f"{ROOT}/09-final-output"
TMP = "/tmp/asm"; os.makedirs(TMP, exist_ok=True)

# (file, start_sec, dur_sec)  -- tight, punchy pacing
CLIPS = [
    (f"{CL}/shot1.mp4", 2.4, 2.0),
    (f"{CL}/shot2.mp4", 1.6, 1.8),
    (f"{CL}/shot3.mp4", 2.2, 1.8),
    (f"{CL}/shot4.mp4", 0.8, 1.6),
    (f"{CL}/shot5.mp4", 2.6, 1.8),
    (f"{CL}/shot6.mp4", 1.8, 2.4),
]
ENDCARD = f"{OUT}/attempts/endcard.png"
ENDCARD_DUR = 3.0
W, H, FPS = 1080, 1920, 30

def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

segs = []
for i,(f,ss,dur) in enumerate(CLIPS):
    o = f"{TMP}/seg{i}.mp4"
    vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p"
    run([FF,"-y","-ss",str(ss),"-t",str(dur),"-i",f,
         "-vf",vf,"-af","afade=t=in:st=0:d=0.06,afade=t=out:st=%.2f:d=0.06"%(dur-0.06),
         "-c:v","libx264","-preset","medium","-crf","18","-r",str(FPS),
         "-c:a","aac","-b:a","160k","-ar","48000","-ac","2",o])
    segs.append(o)

# endcard segment (silent)
eo = f"{TMP}/seg_end.mp4"
run([FF,"-y","-loop","1","-t",str(ENDCARD_DUR),"-i",ENDCARD,
     "-f","lavfi","-t",str(ENDCARD_DUR),"-i","anullsrc=r=48000:cl=stereo",
     "-vf",f"scale={W}:{H},fps={FPS},format=yuv420p",
     "-c:v","libx264","-preset","medium","-crf","18","-r",str(FPS),
     "-c:a","aac","-b:a","160k","-ar","48000","-ac","2","-shortest",eo])
segs.append(eo)

lst = f"{TMP}/list.txt"
with open(lst,"w") as fh:
    for s in segs: fh.write(f"file '{s}'\n")
out = f"{OUT}/easy-taxi-belgium-ad-9x16.mp4"
run([FF,"-y","-f","concat","-safe","0","-i",lst,"-c:v","libx264","-preset","medium",
     "-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-movflags","+faststart",out])
d = subprocess.run([FF,"-i",out],capture_output=True,text=True).stderr
import re; m=re.search(r"Duration: ([0-9:.]+)", d)
print("FINAL:", out, "duration", m.group(1) if m else "?")
