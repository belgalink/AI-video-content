import subprocess, os, re, imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe()
ROOT="/home/user/AI-video-content/projects/easy-taxi-airport"
V5=f"{ROOT}/07-transition-videos/approved/kling-v5"
V4=f"{ROOT}/07-transition-videos/approved/kling-v4"
OUT=f"{ROOT}/09-final-output"
LOGO=f"{ROOT}/02-references/approved/brand/easytaxi-logo-rgba.png"
TMP="/tmp/asmk5"; os.makedirs(TMP,exist_ok=True)
W,H,FPS=1080,1920,30
# order: approach(car still), handle-handover(soft smile), estate-boot(v4), highway(v4), handshake(new decor), arrival(new decor)
CLIPS=[(f"{V5}/shot1.mp4",0.8,1.9),(f"{V5}/shot2.mp4",0.7,1.9),(f"{V4}/shot3.mp4",0.9,1.7),
       (f"{V4}/shot4.mp4",0.4,1.3),(f"{V5}/shot5.mp4",0.9,1.9),(f"{V5}/shot6.mp4",0.6,1.7)]
ENDCARD=f"{OUT}/attempts/endcard_stacked.png"; ED=3.0
def run(c): subprocess.run(c,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
segs=[]
for i,(f,ss,dur) in enumerate(CLIPS):
    o=f"{TMP}/s{i}.mp4"
    fc=(f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}[b];"
        f"[1:v]scale=300:-2[lg];[b][lg]overlay=44:70,format=yuv420p[v]")
    run([FF,"-y","-ss",str(ss),"-t",str(dur),"-i",f,"-i",LOGO,"-filter_complex",fc,
         "-map","[v]","-map","0:a","-af","afade=t=in:st=0:d=0.05,afade=t=out:st=%.2f:d=0.06"%(dur-0.06),
         "-c:v","libx264","-preset","medium","-crf","18","-r",str(FPS),
         "-c:a","aac","-b:a","160k","-ar","48000","-ac","2",o]); segs.append(o)
# single stacked endcard, silent
eo=f"{TMP}/end.mp4"
run([FF,"-y","-loop","1","-t",str(ED),"-i",ENDCARD,"-f","lavfi","-t",str(ED),"-i","anullsrc=r=48000:cl=stereo",
     "-vf",f"scale={W}:{H},fps={FPS},format=yuv420p","-c:v","libx264","-preset","medium","-crf","18",
     "-r",str(FPS),"-c:a","aac","-b:a","160k","-ar","48000","-ac","2","-shortest",eo]); segs.append(eo)
lst=f"{TMP}/l.txt"; open(lst,"w").write("".join(f"file '{s}'\n" for s in segs))
out=f"{OUT}/easy-taxi-belgium-ad-9x16.mp4"
run([FF,"-y","-f","concat","-safe","0","-i",lst,"-c:v","libx264","-preset","slow","-crf","18",
     "-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-movflags","+faststart",out])
d=subprocess.run([FF,"-i",out],capture_output=True,text=True).stderr
print("FINAL v5:",out,"dur",re.search(r"Duration: ([0-9:.]+)",d).group(1))
