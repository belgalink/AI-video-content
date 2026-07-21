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
DLG1="/tmp/asmv9/scene1_dialogue_ref.wav"
DLG5="/tmp/asmv9/scene5_dialogue_ref.wav"

def video_with_logo(src_video, ss, dur, out_video_only):
    fc=(f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}[b];"
        f"[1:v]scale=300:-2[lg];[b][lg]overlay=44:70,format=yuv420p[v]")
    run([FF,"-y","-ss",str(ss),"-t",str(dur),"-i",src_video,"-i",LOGO,"-filter_complex",fc,
         "-map","[v]","-an","-c:v","libx264","-preset","medium","-crf","18","-r",str(FPS),out_video_only])

def mux(video_only, audio_wav, out, dur):
    run([FF,"-y","-i",video_only,"-i",audio_wav,"-t",str(dur),
         "-c:v","copy","-c:a","aac","-b:a","160k","-ar","48000","-ac","2","-shortest",out])

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

# Non-dialogue scenes: use their own native ambient audio, trimmed, with only tiny anti-click fades
# (NOT loudness crossfades) so hard cuts between scenes don't pop.
# NOTE: trim + afade MUST be two separate ffmpeg passes -- combining -ss/-t and afade in one
# filter graph triggered a ffmpeg quirk that silently crushed the mean level by >10dB on some
# clips (reproduced on shot3/shot6 1.7s windows), which is very likely the real cause of the
# "dead air between scenes" complaint, not just a perceptual loudness-mismatch issue.
def native_audio(src, ss, dur, out, extra_gain_db=0.0):
    trimmed=out+".trim.wav"
    run([FF,"-y","-i",src,"-ss",str(ss),"-t",str(dur),"-vn","-ar","44100","-ac","2",trimmed])
    fade_out_st = max(0.0, dur-0.06)
    af=f"afade=t=in:st=0:d=0.05,afade=t=out:st={fade_out_st:.2f}:d=0.06"
    if extra_gain_db: af=f"volume={extra_gain_db}dB,"+af
    run([FF,"-y","-i",trimmed,"-af",af,out])

a1=f"{TMP}/a1.wav"; native_audio(f"{V8}/shot2.mp4",0.7,2.4,a1)
a2=f"{TMP}/a2.wav"; native_audio(f"{V8}/shot3.mp4",0.9,1.7,a2)
a3=f"{TMP}/a3.wav"; native_audio(f"{V6}/shot4.mp4",0.4,1.3,a3)
a5=f"{TMP}/a5.wav"; native_audio(f"{V6}/shot6.mp4",0.6,1.7,a5,extra_gain_db=27.0)  # source is inherently near-silent

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

# --- Mux each scene's video+audio, then hard-concat all segments (proven-reliable approach) ---
segs=[]
for i,(v,a,d) in enumerate(zip(VIDEOS,AUDIOS,DURS)):
    s=f"{TMP}/seg{i}.mp4"; mux(v,a,s,d); segs.append(s)

# --- Endcards (silent) ---
ED1=3.0
eo1=f"{TMP}/end1.mp4"
run([FF,"-y","-loop","1","-t",str(ED1),"-i",ENDCARD1,"-f","lavfi","-t",str(ED1),"-i","anullsrc=r=48000:cl=stereo",
     "-vf",f"scale={W}:{H},fps={FPS},format=yuv420p","-c:v","libx264","-preset","medium","-crf","18",
     "-r",str(FPS),"-c:a","aac","-b:a","160k","-ar","48000","-ac","2","-shortest",eo1]); segs.append(eo1)

ED2=3.5
eo2=f"{TMP}/end2.mp4"
run([FF,"-y","-loop","1","-t",str(ED2),"-i",ENDCARD2,"-f","lavfi","-t",str(ED2),"-i","anullsrc=r=48000:cl=stereo",
     "-vf",f"scale={W}:{H},fps={FPS},format=yuv420p","-c:v","libx264","-preset","medium","-crf","18",
     "-r",str(FPS),"-c:a","aac","-b:a","160k","-ar","48000","-ac","2","-shortest",eo2]); segs.append(eo2)

# --- Final concat: all 6 scenes + 2 endcards (re-encode to guarantee matching params) ---
lst=f"{TMP}/final_list.txt"
open(lst,"w").write("".join(f"file '{s}'\n" for s in segs))
out=f"{OUT}/easy-taxi-belgium-ad-9x16.mp4"
run([FF,"-y","-f","concat","-safe","0","-i",lst,"-c:v","libx264","-preset","slow","-crf","18",
     "-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-movflags","+faststart",out])
d=subprocess.run([FF,"-i",out],capture_output=True,text=True).stderr
print("FINAL v9:",out,"dur",re.search(r"Duration: ([0-9:.]+)",d).group(1))
