import subprocess, os, re, imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe()
ROOT="/home/user/AI-video-content/projects/easy-taxi-airport"
V6=f"{ROOT}/07-transition-videos/approved/kling-v6"
OUT=f"{ROOT}/09-final-output"
LOGO=f"{ROOT}/02-references/approved/brand/easytaxi-logo-rgba.png"
AUD=f"{ROOT}/06-video-prompts/audio"
ENDCARD=f"{OUT}/attempts/endcard_stacked.png"
TMP="/tmp/asmk6"; os.makedirs(TMP,exist_ok=True)
W,H,FPS=1080,1920,30
# (file, start, dur, has_ambient)
CLIPS=[(f"{V6}/shot1.mp4",0.0,5.0,False),  # scene1 greeting (VO only)
       (f"{V6}/shot2.mp4",0.7,2.4,True),   # handover
       (f"{V6}/shot3.mp4",0.9,1.7,True),   # estate boot
       (f"{V6}/shot4.mp4",0.4,1.3,True),   # highway
       (f"{V6}/shot5.mp4",0.0,5.0,False),  # goodbye (VO only)
       (f"{V6}/shot6.mp4",0.6,1.7,True)]   # arrival hero
ED=3.0
def run(c): subprocess.run(c,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
segs=[]
for i,(f,ss,dur,amb) in enumerate(CLIPS):
    o=f"{TMP}/s{i}.mp4"
    fc=(f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}[b];"
        f"[1:v]scale=300:-2[lg];[b][lg]overlay=44:70,format=yuv420p[v]")
    if amb:
        run([FF,"-y","-ss",str(ss),"-t",str(dur),"-i",f,"-i",LOGO,"-filter_complex",fc,
             "-map","[v]","-map","0:a","-af","afade=t=in:st=0:d=0.05,afade=t=out:st=%.2f:d=0.06"%(dur-0.06),
             "-c:v","libx264","-preset","medium","-crf","18","-r",str(FPS),
             "-c:a","aac","-b:a","160k","-ar","48000","-ac","2",o])
    else:  # silent scene: synth silent audio
        run([FF,"-y","-ss",str(ss),"-t",str(dur),"-i",f,"-i",LOGO,
             "-f","lavfi","-t",str(dur),"-i","anullsrc=r=48000:cl=stereo",
             "-filter_complex",fc,"-map","[v]","-map","2:a",
             "-c:v","libx264","-preset","medium","-crf","18","-r",str(FPS),
             "-c:a","aac","-b:a","160k","-ar","48000","-ac","2",o])
    segs.append(o)
# endcard silent
eo=f"{TMP}/end.mp4"
run([FF,"-y","-loop","1","-t",str(ED),"-i",ENDCARD,"-f","lavfi","-t",str(ED),"-i","anullsrc=r=48000:cl=stereo",
     "-vf",f"scale={W}:{H},fps={FPS},format=yuv420p","-c:v","libx264","-preset","medium","-crf","18",
     "-r",str(FPS),"-c:a","aac","-b:a","160k","-ar","48000","-ac","2","-shortest",eo]); segs.append(eo)
# concat base
lst=f"{TMP}/l.txt"; open(lst,"w").write("".join(f"file '{s}'\n" for s in segs))
base=f"{TMP}/base.mp4"
run([FF,"-y","-f","concat","-safe","0","-i",lst,"-c:v","libx264","-preset","medium","-crf","18",
     "-pix_fmt","yuv420p","-c:a","aac","-b:a","160k",base])
# overlay Flemish dialogue at timestamps, mixed with ambient
out=f"{OUT}/easy-taxi-belgium-ad-9x16.mp4"
# (wav, delay_ms)
VO=[(f"{AUD}/driver1.wav",600),(f"{AUD}/pass1.wav",4700),(f"{AUD}/pass2.wav",10700),(f"{AUD}/driver2.wav",12100)]
inputs=["-i",base]
for w,_ in VO: inputs+=["-i",w]
fc=["[0:a]volume=0.55[amb]"]
labels=["[amb]"]
for idx,(w,d) in enumerate(VO,start=1):
    fc.append(f"[{idx}:a]adelay={d}|{d},volume=1.2[v{idx}]"); labels.append(f"[v{idx}]")
fc.append("".join(labels)+f"amix=inputs={len(labels)}:normalize=0:duration=first[aout]")
run([FF,"-y",*inputs,"-filter_complex",";".join(fc),
     "-map","0:v","-map","[aout]","-c:v","copy","-c:a","aac","-b:a","160k","-movflags","+faststart",out])
d=subprocess.run([FF,"-i",out],capture_output=True,text=True).stderr
print("FINAL v6:",out,"dur",re.search(r"Duration: ([0-9:.]+)",d).group(1))
