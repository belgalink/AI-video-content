import subprocess, os, re, imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe()
ROOT="/home/user/AI-video-content/projects/easy-taxi-airport"
OUT=f"{ROOT}/09-final-output"
NEW="/tmp/newscenes"
TMP="/tmp/asm_v10"; os.makedirs(TMP,exist_ok=True)
AEXACT="/tmp/asm_exact"   # dialogue/bed assets built earlier this session
LOGO=f"{ROOT}/02-references/approved/brand/easytaxi-logo-rgba.png"
ENDCARD=f"{OUT}/attempts/endcard_stacked.png"
W,H,FPS=1080,1920,30

def run(c): subprocess.run(c,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)

# ============ VIDEO: regenerated scenes, plate baked in via real pixels ============
# (source_file, duration)
SCENES=[
    (f"{NEW}/v1.mp4", 2.1667),
    (f"{NEW}/v2.mp4", 1.9333),
    (f"{NEW}/v3.mp4", 1.7333),
    (f"{NEW}/v4.mp4", 1.3667),
    (f"{NEW}/v5.mp4", 1.9333),
    (f"{NEW}/v6.mp4", 1.7333),
]

def video_scaled(src, dur, out):
    fc=(f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p[v]")
    run([FF,"-y","-t",str(dur),"-i",src,"-filter_complex",fc,
         "-map","[v]","-an","-c:v","libx264","-preset","slow","-crf","16","-r",str(FPS),out])

vids=[]
for i,(src,dur) in enumerate(SCENES):
    o=f"{TMP}/v{i}.mp4"; video_scaled(src,dur,o); vids.append(o)

vlst=f"{TMP}/vlist.txt"; open(vlst,"w").write("".join(f"file '{v}'\n" for v in vids))
base_video=f"{TMP}/base_video.mp4"
run([FF,"-y","-f","concat","-safe","0","-i",vlst,"-c","copy",base_video])

TOTAL_VIDEO_DUR=sum(d for _,d in SCENES)  # 10.8667s

# ============ AUDIO: ONE continuous bed (single crossfade at the airport->street cut), ============
# ============ dialogue mixed on top at absolute timestamps -- no per-scene hard splices ============
bed_airport_raw=f"{AEXACT}/bed_airport_raw.wav"
bed_street_raw=f"{AEXACT}/bed_street_raw.wav"

def tile_bed(src, target_dur, out):
    d=subprocess.run([FF,"-i",src],capture_output=True,text=True).stderr
    m=re.search(r"Duration: (\d+):(\d+):([\d.]+)",d)
    src_dur=int(m.group(1))*3600+int(m.group(2))*60+float(m.group(3))
    reps=int(target_dur//src_dur)+2
    lst=f"{out}.list.txt"; open(lst,"w").write((f"file '{src}'\n")*reps)
    run([FF,"-y","-f","concat","-safe","0","-i",lst,"-t",str(target_dur),"-ar","44100","-ac","2",out])

XF=0.2
boundary=7.2  # airport -> street context change, matches the scene4/scene5 video cut
clip1_len=boundary + XF/2
clip2_len=(TOTAL_VIDEO_DUR-boundary) + XF/2

bed1=f"{TMP}/bed1.wav"; tile_bed(bed_airport_raw, clip1_len, bed1)
bed2=f"{TMP}/bed2.wav"; tile_bed(bed_street_raw, clip2_len, bed2)

continuous_bed=f"{TMP}/continuous_bed.wav"
run([FF,"-y","-i",bed1,"-i",bed2,"-filter_complex",
     f"[0:a][1:a]acrossfade=d={XF}:c1=tri:c2=tri[aout]",
     "-map","[aout]","-ar","44100","-ac","2",continuous_bed])

DRIVER1=f"{AEXACT}/driver1_new.wav"
DRIVER2=f"{AEXACT}/driver2_new.wav"
PASS1=f"{AEXACT}/pass1_new.wav"
PASS2=f"{AEXACT}/pass2_new.wav"

full_audio_raw=f"{TMP}/full_audio_raw.wav"
run([FF,"-y","-i",continuous_bed,"-i",DRIVER1,"-i",PASS1,"-i",PASS2,"-i",DRIVER2,"-filter_complex",
     "[1:a]adelay=300|300[d1];"
     "[2:a]adelay=2900|2900[p1];"
     "[3:a]adelay=7500|7500[p2];"
     "[4:a]adelay=8500|8500[d2];"
     "[0:a][d1][p1][p2][d2]amix=inputs=5:normalize=0:duration=first[aout]",
     "-map","[aout]","-t",str(TOTAL_VIDEO_DUR),"-ar","44100","-ac","2",full_audio_raw])

# pad/trim to guarantee exact match with base_video's duration
full_audio=f"{TMP}/full_audio.wav"
run([FF,"-y","-i",full_audio_raw,"-af",f"apad=whole_dur={TOTAL_VIDEO_DUR}s","-t",str(TOTAL_VIDEO_DUR),full_audio])

# ============ Logo overlay on the full base video ============
video_with_logo=f"{TMP}/video_with_logo.mp4"
fc_logo=(f"[0:v][1:v]overlay=44:70,format=yuv420p[v]")
run([FF,"-y","-i",base_video,"-i",LOGO,"-filter_complex",
     f"[1:v]scale=300:-2[lg];[0:v][lg]overlay=44:70,format=yuv420p[v]",
     "-map","[v]","-an","-c:v","libx264","-preset","slow","-crf","16","-r",str(FPS),video_with_logo])

# Mux video+audio
main_out=f"{TMP}/main.mp4"
run([FF,"-y","-i",video_with_logo,"-i",full_audio,"-c:v","copy","-c:a","aac","-b:a","160k",
     "-ar","48000","-ac","2","-shortest",main_out])

# ============ Endcard (silent, matches the single-endcard structure of the uploaded cut) ============
ED=3.0
eo=f"{TMP}/end.mp4"
run([FF,"-y","-loop","1","-t",str(ED),"-i",ENDCARD,"-f","lavfi","-t",str(ED),"-i","anullsrc=r=48000:cl=stereo",
     "-vf",f"scale={W}:{H},fps={FPS},format=yuv420p","-c:v","libx264","-preset","medium","-crf","18",
     "-r",str(FPS),"-c:a","aac","-b:a","160k","-ar","48000","-ac","2","-shortest",eo])

lst=f"{TMP}/final_list.txt"
open(lst,"w").write(f"file '{main_out}'\nfile '{eo}'\n")
out=f"{OUT}/easy-taxi-belgium-ad-9x16-v10.mp4"
run([FF,"-y","-f","concat","-safe","0","-i",lst,"-c:v","libx264","-preset","slow","-crf","16",
     "-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-movflags","+faststart",out])

d=subprocess.run([FF,"-i",out],capture_output=True,text=True).stderr
print("FINAL v10:",out,"dur",re.search(r"Duration: ([0-9:.]+)",d).group(1))
