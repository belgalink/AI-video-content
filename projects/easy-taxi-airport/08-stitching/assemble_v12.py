import subprocess, os, re, imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe()
ROOT="/home/user/AI-video-content/projects/easy-taxi-airport"
OUT=f"{ROOT}/09-final-output"
V12="/tmp/newscenes_v12"   # motion-transfer (video_references) lip-synced scenes: s1,s2,s5
V11="/tmp/newscenes_v11"   # cinematic (Cinema Studio 3.0) scenes, reused as-is: s3,s4,s6
TMP="/tmp/asm_v12"; os.makedirs(TMP,exist_ok=True)
AEXACT="/tmp/asm_exact"
PATCH="/tmp/plate_patch"
LOGO=f"{ROOT}/02-references/approved/brand/easytaxi-logo-rgba.png"
ENDCARD=f"{OUT}/attempts/endcard_stacked.png"
W,H,FPS=1080,1920,30

def run(c): subprocess.run(c,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)

# ============ VIDEO ============
# s1 and s5 came out of Seedance motion-transfer with the license plate having
# reverted to the ORIGINAL unedited texture (the video_reference apparently won
# out over the start_image for that detail) -- patch just those two scenes.
# s2 kept the corrected plate on its own. s3/s4/s6 are untouched cinematic clips
# from the previous round, already correct.
SCENES=[
    (f"{V12}/v1.mp4", 2.1667, f"{PATCH}/s1_v12.png", (815,1140)),
    (f"{V12}/v2.mp4", 1.9333, None, None),
    (f"{V11}/v3.mp4", 1.7333, None, None),
    (f"{V11}/v4.mp4", 1.3667, None, None),
    (f"{V12}/v5.mp4", 1.9333, f"{PATCH}/s5_v12.png", (380,1190)),
    (f"{V11}/v6.mp4", 1.7333, None, None),
]

def video_scaled(src, dur, out, patch=None, patch_xy=None):
    if patch:
        x,y=patch_xy
        # patch image coordinates were measured directly on the 1080x1920 Higgsfield output,
        # so the scale/crop below (a no-op for already-1080x1920 sources) keeps them valid.
        fc=(f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}[b];"
            f"[b][1:v]overlay={x}:{y},format=yuv420p[v]")
        run([FF,"-y","-t",str(dur),"-i",src,"-i",patch,"-filter_complex",fc,
             "-map","[v]","-an","-c:v","libx264","-preset","slow","-crf","16","-r",str(FPS),out])
    else:
        fc=(f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p[v]")
        run([FF,"-y","-t",str(dur),"-i",src,"-filter_complex",fc,
             "-map","[v]","-an","-c:v","libx264","-preset","slow","-crf","16","-r",str(FPS),out])

vids=[]
for i,(src,dur,patch,xy) in enumerate(SCENES):
    o=f"{TMP}/v{i}.mp4"; video_scaled(src,dur,o,patch,xy); vids.append(o)

vlst=f"{TMP}/vlist.txt"; open(vlst,"w").write("".join(f"file '{v}'\n" for v in vids))
base_video=f"{TMP}/base_video.mp4"
run([FF,"-y","-f","concat","-safe","0","-i",vlst,"-c","copy",base_video])

TOTAL_VIDEO_DUR=sum(d for _,d,_,_ in SCENES)  # 10.8667s

# ============ AUDIO: much softer synthesized bed (fixes "veel te harde ruis"), ============
# ============ ONE continuous bed with a single crossfade, dialogue mixed on top ============
def synth_bed(color, dur, lp, hp, gain, out):
    run([FF,"-y","-f","lavfi","-i",f"anoisesrc=color={color}:amplitude=1:r=44100","-t",str(dur),
         "-af",f"lowpass=f={lp},highpass=f={hp},volume={gain}","-ar","44100","-ac","2",out])

XF=0.2
boundary=7.2
clip1_len=boundary + XF/2
clip2_len=(TOTAL_VIDEO_DUR-boundary) + XF/2

bed1=f"{TMP}/bed1.wav"; synth_bed("brown", clip1_len, 250, 100, 0.14, bed1)   # airport, much softer
bed2=f"{TMP}/bed2.wav"; synth_bed("pink", clip2_len, 200, 80, 0.22, bed2)    # street, much softer

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

full_audio=f"{TMP}/full_audio.wav"
run([FF,"-y","-i",full_audio_raw,"-af",f"apad=whole_dur={TOTAL_VIDEO_DUR}s","-t",str(TOTAL_VIDEO_DUR),full_audio])

# ============ Logo overlay ============
video_with_logo=f"{TMP}/video_with_logo.mp4"
run([FF,"-y","-i",base_video,"-i",LOGO,"-filter_complex",
     f"[1:v]scale=300:-2[lg];[0:v][lg]overlay=44:70,format=yuv420p[v]",
     "-map","[v]","-an","-c:v","libx264","-preset","slow","-crf","16","-r",str(FPS),video_with_logo])

main_out=f"{TMP}/main.mp4"
run([FF,"-y","-i",video_with_logo,"-i",full_audio,"-c:v","copy","-c:a","aac","-b:a","160k",
     "-ar","48000","-ac","2","-shortest",main_out])

# ============ Endcard (silent) ============
ED=3.0
eo=f"{TMP}/end.mp4"
run([FF,"-y","-loop","1","-t",str(ED),"-i",ENDCARD,"-f","lavfi","-t",str(ED),"-i","anullsrc=r=48000:cl=stereo",
     "-vf",f"scale={W}:{H},fps={FPS},format=yuv420p","-c:v","libx264","-preset","medium","-crf","18",
     "-r",str(FPS),"-c:a","aac","-b:a","160k","-ar","48000","-ac","2","-shortest",eo])

lst=f"{TMP}/final_list.txt"
open(lst,"w").write(f"file '{main_out}'\nfile '{eo}'\n")
out=f"{OUT}/easy-taxi-belgium-ad-9x16-v12.mp4"
run([FF,"-y","-f","concat","-safe","0","-i",lst,"-c:v","libx264","-preset","slow","-crf","16",
     "-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-movflags","+faststart",out])

d=subprocess.run([FF,"-i",out],capture_output=True,text=True).stderr
print("FINAL v12:",out,"dur",re.search(r"Duration: ([0-9:.]+)",d).group(1))
