import subprocess, os, re, imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe()
ROOT="/home/user/AI-video-content/projects/easy-taxi-airport"
CL=f"{ROOT}/07-transition-videos/approved/kling-v4"; OUT=f"{ROOT}/09-final-output"
LOGO=f"{ROOT}/02-references/approved/brand/easytaxi-logo-rgba.png"
TMP="/tmp/asmk4"; os.makedirs(TMP,exist_ok=True)
W,H,FPS=1080,1920,30
# order: approach, handle-handover, estate-boot, highway, handshake(villa), arrival(villa hero)
CLIPS=[(f"{CL}/shot1.mp4",0.9,1.6),(f"{CL}/shot2.mp4",0.7,1.9),(f"{CL}/shot3.mp4",0.9,1.7),
       (f"{CL}/shot4.mp4",0.4,1.3),(f"{CL}/shot5.mp4",0.9,1.9),(f"{CL}/shot6.mp4",0.6,1.6)]
# 4-language end card cycle
ENDCARDS=[f"{OUT}/attempts/endcard_nl.png",f"{OUT}/attempts/endcard_fr.png",
          f"{OUT}/attempts/endcard_en.png",f"{OUT}/attempts/endcard_tr.png"]
ED=1.2  # per language slide
def run(c): subprocess.run(c,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
segs=[]
# scene segments with small logo top-left
for i,(f,ss,dur) in enumerate(CLIPS):
    o=f"{TMP}/s{i}.mp4"
    fc=(f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p[b];"
        f"[1:v]scale=300:-1[lg];[b][lg]overlay=44:70[v]")
    run([FF,"-y","-ss",str(ss),"-t",str(dur),"-i",f,"-i",LOGO,
         "-filter_complex",fc,"-map","[v]","-map","0:a",
         "-af","afade=t=in:st=0:d=0.05,afade=t=out:st=%.2f:d=0.06"%(dur-0.06),
         "-c:v","libx264","-preset","medium","-crf","18","-r",str(FPS),
         "-c:a","aac","-b:a","160k","-ar","48000","-ac","2",o]); segs.append(o)
# end card language slides (silent, no small logo - big logo already present)
for j,ec in enumerate(ENDCARDS):
    o=f"{TMP}/e{j}.mp4"
    run([FF,"-y","-loop","1","-t",str(ED),"-i",ec,"-f","lavfi","-t",str(ED),"-i","anullsrc=r=48000:cl=stereo",
         "-vf",f"scale={W}:{H},fps={FPS},format=yuv420p","-c:v","libx264","-preset","medium","-crf","18",
         "-r",str(FPS),"-c:a","aac","-b:a","160k","-ar","48000","-ac","2","-shortest",o]); segs.append(o)
lst=f"{TMP}/l.txt"; open(lst,"w").write("".join(f"file '{s}'\n" for s in segs))
out=f"{OUT}/easy-taxi-belgium-ad-9x16.mp4"
run([FF,"-y","-f","concat","-safe","0","-i",lst,"-c:v","libx264","-preset","slow","-crf","18",
     "-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-movflags","+faststart",out])
d=subprocess.run([FF,"-i",out],capture_output=True,text=True).stderr
print("FINAL v4:",out,"dur",re.search(r"Duration: ([0-9:.]+)",d).group(1))
