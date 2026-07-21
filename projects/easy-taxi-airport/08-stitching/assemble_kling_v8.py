import subprocess, os, re, imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe()
ROOT="/home/user/AI-video-content/projects/easy-taxi-airport"
V6=f"{ROOT}/07-transition-videos/approved/kling-v6"
V8=f"{ROOT}/07-transition-videos/approved/kling-v8"
OUT=f"{ROOT}/09-final-output"
LOGO=f"{ROOT}/02-references/approved/brand/easytaxi-logo-rgba.png"
AUD=f"{ROOT}/06-video-prompts/audio"
ENDCARD1=f"{OUT}/attempts/endcard_stacked.png"
ENDCARD2=f"{OUT}/attempts/endcard_routes.png"
TMP="/tmp/asmk8"; os.makedirs(TMP,exist_ok=True)
W,H,FPS=1080,1920,30

def run(c): subprocess.run(c,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)

DRIVER1=f"{AUD}/elevenlabs-test/1-driver-goededag.mp3"
PASS1  =f"{AUD}/bram-passenger/pass1-pitched.wav"
PASS2  =f"{AUD}/bram-passenger/pass2-pitched.wav"
DRIVER2=f"{AUD}/elevenlabs-test/4-driver-graaggedaan.mp3"

DIALOG_FX = "highpass=f=110,equalizer=f=7000:t=h:width=2000:g=-3,aecho=0.75:0.6:35|55:0.22|0.14,volume=1.0"

def process_dialog(src, out):
    run([FF,"-y","-i",src,"-af",DIALOG_FX,"-ar","44100","-ac","2",out])

d1=f"{TMP}/d1.wav"; p1=f"{TMP}/p1.wav"; p2=f"{TMP}/p2.wav"; d2=f"{TMP}/d2.wav"
process_dialog(DRIVER1,d1); process_dialog(PASS1,p1); process_dialog(PASS2,p2); process_dialog(DRIVER2,d2)

# Ambient beds: airport bed now pulled from the NEW env-consistent scene2 (kling-v8), street bed from v6 scene6
bed_airport=f"{TMP}/bed_airport.wav"
bed_street=f"{TMP}/bed_street.wav"
run([FF,"-y","-i",f"{V8}/shot2.mp4","-t","5.0","-vn","-af","volume=0.16","-ar","44100","-ac","2",bed_airport])
run([FF,"-y","-i",f"{V6}/shot6.mp4","-t","5.0","-vn","-af","volume=0.16","-ar","44100","-ac","2",bed_street])

def video_with_logo(src_video, ss, dur, out_video_only):
    fc=(f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}[b];"
        f"[1:v]scale=300:-2[lg];[b][lg]overlay=44:70,format=yuv420p[v]")
    run([FF,"-y","-ss",str(ss),"-t",str(dur),"-i",src_video,"-i",LOGO,"-filter_complex",fc,
         "-map","[v]","-an","-c:v","libx264","-preset","medium","-crf","18","-r",str(FPS),out_video_only])

def mux(video_only, audio_wav, out, dur):
    run([FF,"-y","-i",video_only,"-i",audio_wav,"-t",str(dur),
         "-c:v","copy","-c:a","aac","-b:a","160k","-ar","48000","-ac","2","-shortest",out])

segs=[]

# Scene 1: greeting at airport curb (env-consistent), 0-4.9s
v0=f"{TMP}/v0.mp4"; video_with_logo(f"{V8}/shot1.mp4",0.0,4.9,v0)
a0=f"{TMP}/a0.wav"
run([FF,"-y","-i",bed_airport,"-i",d1,"-i",p1,"-filter_complex",
     "[1:a]adelay=300|300[d1];[2:a]adelay=3000|3000[p1];[0:a][d1][p1]amix=inputs=3:normalize=0:duration=first[aout]",
     "-map","[aout]","-ar","44100","-ac","2",a0])
s0=f"{TMP}/seg0.mp4"; mux(v0,a0,s0,4.9); segs.append(s0)

# Scene 2: handle handover at SAME airport curb (env-consistent, different angle)
v1=f"{TMP}/v1.mp4"; video_with_logo(f"{V8}/shot2.mp4",0.7,2.4,v1)
run([FF,"-y","-i",f"{V8}/shot2.mp4","-ss","0.7","-t","2.4","-vn","-af",
     "afade=t=in:st=0:d=0.05,afade=t=out:st=2.34:d=0.06","-c:a","aac","-b:a","160k","-ar","48000","-ac","2",f"{TMP}/a1.aac"])
s1=f"{TMP}/seg1.mp4"; run([FF,"-y","-i",v1,"-i",f"{TMP}/a1.aac","-c:v","copy","-c:a","copy","-shortest",s1]); segs.append(s1)

# Scene 3: estate boot at SAME airport curb (env-consistent, different angle)
v2=f"{TMP}/v2.mp4"; video_with_logo(f"{V8}/shot3.mp4",0.9,1.7,v2)
run([FF,"-y","-i",f"{V8}/shot3.mp4","-ss","0.9","-t","1.7","-vn","-af",
     "afade=t=in:st=0:d=0.05,afade=t=out:st=1.64:d=0.06","-c:a","aac","-b:a","160k","-ar","48000","-ac","2",f"{TMP}/a2.aac"])
s2=f"{TMP}/seg2.mp4"; run([FF,"-y","-i",v2,"-i",f"{TMP}/a2.aac","-c:v","copy","-c:a","copy","-shortest",s2]); segs.append(s2)

# Scene 4: highway (unchanged, from v6)
v3=f"{TMP}/v3.mp4"; video_with_logo(f"{V6}/shot4.mp4",0.4,1.3,v3)
run([FF,"-y","-i",f"{V6}/shot4.mp4","-ss","0.4","-t","1.3","-vn","-af",
     "afade=t=in:st=0:d=0.05,afade=t=out:st=1.24:d=0.06","-c:a","aac","-b:a","160k","-ar","48000","-ac","2",f"{TMP}/a3.aac"])
s3=f"{TMP}/seg3.mp4"; run([FF,"-y","-i",v3,"-i",f"{TMP}/a3.aac","-c:v","copy","-c:a","copy","-shortest",s3]); segs.append(s3)

# Scene 5: goodbye (unchanged, from v6), 0-4.0s
v4=f"{TMP}/v4.mp4"; video_with_logo(f"{V6}/shot5.mp4",0.0,4.0,v4)
a4=f"{TMP}/a4.wav"
run([FF,"-y","-i",bed_street,"-i",p2,"-i",d2,"-filter_complex",
     "[1:a]adelay=400|400[p2];[2:a]adelay=1700|1700[d2];[0:a][p2][d2]amix=inputs=3:normalize=0:duration=first[aout]",
     "-map","[aout]","-ar","44100","-ac","2",a4])
s4=f"{TMP}/seg4.mp4"; mux(v4,a4,s4,4.0); segs.append(s4)

# Scene 6: arrival hero (unchanged, from v6)
v5=f"{TMP}/v5.mp4"; video_with_logo(f"{V6}/shot6.mp4",0.6,1.7,v5)
run([FF,"-y","-i",f"{V6}/shot6.mp4","-ss","0.6","-t","1.7","-vn","-af",
     "afade=t=in:st=0:d=0.05,afade=t=out:st=1.64:d=0.06","-c:a","aac","-b:a","160k","-ar","48000","-ac","2",f"{TMP}/a5.aac"])
s5=f"{TMP}/seg5.mp4"; run([FF,"-y","-i",v5,"-i",f"{TMP}/a5.aac","-c:v","copy","-c:a","copy","-shortest",s5]); segs.append(s5)

# Endcard 1 (silent, stacked 4-language)
ED=3.0
eo1=f"{TMP}/end1.mp4"
run([FF,"-y","-loop","1","-t",str(ED),"-i",ENDCARD1,"-f","lavfi","-t",str(ED),"-i","anullsrc=r=48000:cl=stereo",
     "-vf",f"scale={W}:{H},fps={FPS},format=yuv420p","-c:v","libx264","-preset","medium","-crf","18",
     "-r",str(FPS),"-c:a","aac","-b:a","160k","-ar","48000","-ac","2","-shortest",eo1]); segs.append(eo1)

# Endcard 2 (silent, routes/services)
ED2=3.5
eo2=f"{TMP}/end2.mp4"
run([FF,"-y","-loop","1","-t",str(ED2),"-i",ENDCARD2,"-f","lavfi","-t",str(ED2),"-i","anullsrc=r=48000:cl=stereo",
     "-vf",f"scale={W}:{H},fps={FPS},format=yuv420p","-c:v","libx264","-preset","medium","-crf","18",
     "-r",str(FPS),"-c:a","aac","-b:a","160k","-ar","48000","-ac","2","-shortest",eo2]); segs.append(eo2)

lst=f"{TMP}/l.txt"; open(lst,"w").write("".join(f"file '{s}'\n" for s in segs))
out=f"{OUT}/easy-taxi-belgium-ad-9x16.mp4"
run([FF,"-y","-f","concat","-safe","0","-i",lst,"-c:v","libx264","-preset","slow","-crf","18",
     "-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-movflags","+faststart",out])
d=subprocess.run([FF,"-i",out],capture_output=True,text=True).stderr
print("FINAL v8:",out,"dur",re.search(r"Duration: ([0-9:.]+)",d).group(1))
