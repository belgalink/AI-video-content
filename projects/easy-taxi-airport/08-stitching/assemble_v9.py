import subprocess, os, re, imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe()
ROOT="/home/user/AI-video-content/projects/easy-taxi-airport"
V6=f"{ROOT}/07-transition-videos/approved/kling-v6"
V8=f"{ROOT}/07-transition-videos/approved/kling-v8"
V9=f"{ROOT}/07-transition-videos/approved/kling-v9"   # new audio-driven Seedance dialogue clips
OUT=f"{ROOT}/09-final-output"
LOGO=f"{ROOT}/02-references/approved/brand/easytaxi-logo-rgba.png"
ENDCARD1=f"{OUT}/attempts/endcard_stacked.png"
ENDCARD2=f"{OUT}/attempts/endcard_routes.png"
TMP="/tmp/asmv9out"; os.makedirs(TMP,exist_ok=True)
W,H,FPS=1080,1920,30

def run(c): subprocess.run(c,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)

# Final dialogue reference mixes we already built (same audio used to DRIVE Seedance's lip motion)
DLG1=f"{ROOT}/../../../tmp/asmv9/scene1_dialogue_ref.wav" if False else "/tmp/asmv9/scene1_dialogue_ref.wav"
DLG5="/tmp/asmv9/scene5_dialogue_ref.wav"

def video_with_logo(src_video, ss, dur, out_video_only):
    fc=(f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}[b];"
        f"[1:v]scale=300:-2[lg];[b][lg]overlay=44:70,format=yuv420p[v]")
    run([FF,"-y","-ss",str(ss),"-t",str(dur),"-i",src_video,"-i",LOGO,"-filter_complex",fc,
         "-map","[v]","-an","-c:v","libx264","-preset","medium","-crf","18","-r",str(FPS),out_video_only])

# --- Build each scene's AUDIO at natural, matched levels (no per-segment fade-to-silence) ---
# Ambient beds: extracted from the corresponding real-sound clip, at a level close to native ambient
# (not whispered) so cutting into/out of dialogue scenes doesn't read as a volume drop.
bed_airport=f"{TMP}/bed_airport.wav"
bed_street=f"{TMP}/bed_street.wav"
run([FF,"-y","-i",f"{V8}/shot2.mp4","-t","4.9","-vn","-af","volume=0.55","-ar","44100","-ac","2",bed_airport])
run([FF,"-y","-i",f"{V6}/shot6.mp4","-t","4.0","-vn","-af","volume=0.55","-ar","44100","-ac","2",bed_street])

# Scene 1 audio = bed(airport) + the exact dialogue mix that drove the lip-sync
a0=f"{TMP}/a0.wav"
run([FF,"-y","-i",bed_airport,"-i",DLG1,"-filter_complex",
     "[0:a][1:a]amix=inputs=2:normalize=0:duration=first[aout]","-map","[aout]","-ar","44100","-ac","2",a0])

# Scene 5 audio = bed(street) + the exact dialogue mix that drove the lip-sync
a4=f"{TMP}/a4.wav"
run([FF,"-y","-i",bed_street,"-i",DLG5,"-filter_complex",
     "[0:a][1:a]amix=inputs=2:normalize=0:duration=first[aout]","-map","[aout]","-ar","44100","-ac","2",a4])

# Non-dialogue scenes: use their own native ambient audio, trimmed, level untouched (no fade to silence)
def native_audio(src, ss, dur, out):
    run([FF,"-y","-i",src,"-ss",str(ss),"-t",str(dur),"-vn","-ar","44100","-ac","2",out])

a1=f"{TMP}/a1.wav"; native_audio(f"{V8}/shot2.mp4",0.7,2.4,a1)
a2=f"{TMP}/a2.wav"; native_audio(f"{V8}/shot3.mp4",0.9,1.7,a2)
a3=f"{TMP}/a3.wav"; native_audio(f"{V6}/shot4.mp4",0.4,1.3,a3)
a5=f"{TMP}/a5.wav"; native_audio(f"{V6}/shot6.mp4",0.6,1.7,a5)

# --- Video segments (video-only, logo overlaid) ---
v0=f"{TMP}/v0.mp4"; video_with_logo(f"{V9}/scene1.mp4",0.0,4.9,v0)
v1=f"{TMP}/v1.mp4"; video_with_logo(f"{V8}/shot2.mp4",0.7,2.4,v1)
v2=f"{TMP}/v2.mp4"; video_with_logo(f"{V8}/shot3.mp4",0.9,1.7,v2)
v3=f"{TMP}/v3.mp4"; video_with_logo(f"{V6}/shot4.mp4",0.4,1.3,v3)
v4=f"{TMP}/v4.mp4"; video_with_logo(f"{V9}/scene5.mp4",0.0,4.0,v4)
v5=f"{TMP}/v5.mp4"; video_with_logo(f"{V6}/shot6.mp4",0.6,1.7,v5)

VIDEOS=[v0,v1,v2,v3,v4,v5]
AUDIOS=[a0,a1,a2,a3,a4,a5]
DURS  =[4.9,2.4,1.7,1.3,4.0,1.7]

# --- Concat all scene videos (video-only) ---
vlst=f"{TMP}/vlist.txt"; open(vlst,"w").write("".join(f"file '{v}'\n" for v in VIDEOS))
base_video=f"{TMP}/base_video.mp4"
run([FF,"-y","-f","concat","-safe","0","-i",vlst,"-c","copy",base_video])

# --- Build ONE continuous audio track with short crossfades between every consecutive scene ---
# Chain acrossfade progressively: ((a0 X a1) X a2) X a3 ... to avoid any hard-cut "seam".
XF=0.18  # 180ms crossfade
cur=AUDIOS[0]
for i in range(1,len(AUDIOS)):
    nxt=f"{TMP}/xf_{i}.wav"
    run([FF,"-y","-i",cur,"-i",AUDIOS[i],"-filter_complex",
         f"[0:a][1:a]acrossfade=d={XF}:c1=tri:c2=tri[aout]",
         "-map","[aout]","-ar","44100","-ac","2",nxt])
    cur=nxt
continuous_audio=cur

# --- Endcards (append after main audio, silent) ---
ED1=3.0
eo1v=f"{TMP}/end1.mp4"
run([FF,"-y","-loop","1","-t",str(ED1),"-i",ENDCARD1,"-f","lavfi","-t",str(ED1),"-i","anullsrc=r=44100:cl=stereo",
     "-vf",f"scale={W}:{H},fps={FPS},format=yuv420p","-c:v","libx264","-preset","medium","-crf","18",
     "-r",str(FPS),"-c:a","aac","-b:a","160k","-ar","48000","-ac","2","-shortest",eo1v])

ED2=3.5
eo2v=f"{TMP}/end2.mp4"
run([FF,"-y","-loop","1","-t",str(ED2),"-i",ENDCARD2,"-f","lavfi","-t",str(ED2),"-i","anullsrc=r=44100:cl=stereo",
     "-vf",f"scale={W}:{H},fps={FPS},format=yuv420p","-c:v","libx264","-preset","medium","-crf","18",
     "-r",str(FPS),"-c:a","aac","-b:a","160k","-ar","48000","-ac","2","-shortest",eo2v])

# Mux base_video + continuous_audio (trim audio to exact video duration, small crossfade shortens total a bit)
main_out=f"{TMP}/main.mp4"
run([FF,"-y","-i",base_video,"-i",continuous_audio,"-c:v","copy","-c:a","aac","-b:a","160k",
     "-ar","48000","-ac","2","-shortest",main_out])

# Final concat: main + endcard1 + endcard2 (re-encode to guarantee matching params)
lst=f"{TMP}/final_list.txt"
open(lst,"w").write(f"file '{main_out}'\nfile '{eo1v}'\nfile '{eo2v}'\n")
out=f"{OUT}/easy-taxi-belgium-ad-9x16.mp4"
run([FF,"-y","-f","concat","-safe","0","-i",lst,"-c:v","libx264","-preset","slow","-crf","18",
     "-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-movflags","+faststart",out])
d=subprocess.run([FF,"-i",out],capture_output=True,text=True).stderr
print("FINAL v9:",out,"dur",re.search(r"Duration: ([0-9:.]+)",d).group(1))
