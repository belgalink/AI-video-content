import subprocess, os, re, imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe()
ROOT="/home/user/AI-video-content/projects/easy-taxi-airport"
CL=f"{ROOT}/07-transition-videos/approved/kling-v2"; OUT=f"{ROOT}/09-final-output"
TMP="/tmp/asmk3"; os.makedirs(TMP,exist_ok=True)
# New order: approach, handle-handover, trunk, highway, HANDSHAKE(house), ARRIVAL(hero). (file,start,dur)
CLIPS=[(f"{CL}/shot1.mp4",0.8,2.0),      # approach + greet
       (f"{CL}/shot2n.mp4",0.6,2.1),     # handover via extended handle
       (f"{CL}/shot3n.mp4",0.8,2.0),     # into normal trunk
       (f"{CL}/shot4.mp4",0.4,1.5),      # highway
       (f"{CL}/shot6n.mp4",0.8,2.3),     # handshake at house
       (f"{CL}/shot5.mp4",0.6,2.0)]      # arrival / parked hero
ENDCARD=f"{OUT}/attempts/endcard.png"; ED=3.0; W,H,FPS=1080,1920,30
def run(c): subprocess.run(c,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
segs=[]
for i,(f,ss,dur) in enumerate(CLIPS):
    o=f"{TMP}/s{i}.mp4"
    vf=f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p"
    run([FF,"-y","-ss",str(ss),"-t",str(dur),"-i",f,"-vf",vf,
         "-af","afade=t=in:st=0:d=0.05,afade=t=out:st=%.2f:d=0.06"%(dur-0.06),
         "-c:v","libx264","-preset","medium","-crf","18","-r",str(FPS),
         "-c:a","aac","-b:a","160k","-ar","48000","-ac","2",o]); segs.append(o)
eo=f"{TMP}/send.mp4"
run([FF,"-y","-loop","1","-t",str(ED),"-i",ENDCARD,"-f","lavfi","-t",str(ED),"-i","anullsrc=r=48000:cl=stereo",
     "-vf",f"scale={W}:{H},fps={FPS},format=yuv420p","-c:v","libx264","-preset","medium","-crf","18",
     "-r",str(FPS),"-c:a","aac","-b:a","160k","-ar","48000","-ac","2","-shortest",eo]); segs.append(eo)
lst=f"{TMP}/l.txt"; open(lst,"w").write("".join(f"file '{s}'\n" for s in segs))
out=f"{OUT}/easy-taxi-belgium-ad-9x16.mp4"
run([FF,"-y","-f","concat","-safe","0","-i",lst,"-c:v","libx264","-preset","slow","-crf","18",
     "-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-movflags","+faststart",out])
d=subprocess.run([FF,"-i",out],capture_output=True,text=True).stderr
print("FINAL v3:",out,"dur",re.search(r"Duration: ([0-9:.]+)",d).group(1))
