import subprocess, os, re, imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe()
ROOT="/home/user/AI-video-content/projects/easy-taxi-airport"
OUT=f"{ROOT}/09-final-output"
SRC="/root/.claude/uploads/e19830a3-95d2-503f-9d5c-09e339606126/12c4f2c7-easytaxibelgiumad9x16.mp4"
TMP="/tmp/asm_exact"; os.makedirs(TMP,exist_ok=True)
PATCH="/tmp/plate_patch"

def run(c): subprocess.run(c,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)

# ============ AUDIO ============
# Bed sources (already built): bed_airport_raw.wav (native, extracted from this exact video's
# own silent trunk window), bed_street_raw.wav (repo street ambient, boosted to match level).
bed_airport=f"{TMP}/bed_airport_raw.wav"   # 1.6s
bed_street=f"{TMP}/bed_street_raw.wav"     # 1.8s

# Tile beds up to the durations we need (simple concat with tiny crossfade to avoid a hard loop click)
def tile_bed(src, target_dur, out):
    # get source duration
    d=subprocess.run([FF,"-i",src],capture_output=True,text=True).stderr
    src_dur=float(re.search(r"Duration: (\d+):(\d+):([\d.]+)",d).groups()[2]) # seconds part only ok since <60s
    m=re.search(r"Duration: (\d+):(\d+):([\d.]+)",d)
    src_dur=int(m.group(1))*3600+int(m.group(2))*60+float(m.group(3))
    reps=int(target_dur//src_dur)+2
    lst=f"{out}.list.txt"; open(lst,"w").write((f"file '{src}'\n")*reps)
    run([FF,"-y","-f","concat","-safe","0","-i",lst,"-t",str(target_dur),"-c","copy",out+".tmp.wav"])
    run([FF,"-y","-i",out+".tmp.wav","-af",f"afade=t=in:st=0:d=0.05,afade=t=out:st={target_dur-0.08:.2f}:d=0.08","-t",str(target_dur),out])

bed_A=f"{TMP}/bed_A.wav"; tile_bed(bed_airport,4.1,bed_A)     # under greeting+handover 0-4.1s
bed_C=f"{TMP}/bed_C.wav"; tile_bed(bed_street,3.67,bed_C)     # under goodbye+arrival 7.2-10.87s

DRIVER1=f"{TMP}/driver1_new.wav"
DRIVER2=f"{TMP}/driver2_new.wav"
PASS1=f"{TMP}/pass1_new.wav"
PASS2=f"{TMP}/pass2_new.wav"

# Segment A: 0-4.1s = bed_A + driver1@0.3 + passenger1@2.9
segA=f"{TMP}/segA.wav"
run([FF,"-y","-i",bed_A,"-i",DRIVER1,"-i",PASS1,"-filter_complex",
     "[1:a]adelay=300|300[d1];[2:a]adelay=2900|2900[p1];[0:a][d1][p1]amix=inputs=3:normalize=0:duration=first[aout]",
     "-map","[aout]","-t","4.1","-ar","44100","-ac","2",segA])

# Segment B: 4.1-7.2s (trunk+highway) = untouched native ambient from the exact uploaded video
segB=f"{TMP}/segB.wav"
run([FF,"-y","-i",SRC,"-ss","4.1","-t","3.1","-vn","-ar","44100","-ac","2",segB])

# Segment C: 7.2-10.87s = bed_C + passenger2@0.3(rel) + driver2@1.3(rel)
segC=f"{TMP}/segC.wav"
run([FF,"-y","-i",bed_C,"-i",PASS2,"-i",DRIVER2,"-filter_complex",
     "[1:a]adelay=300|300[p2];[2:a]adelay=1300|1300[d2];[0:a][p2][d2]amix=inputs=3:normalize=0:duration=first[aout]",
     "-map","[aout]","-t","3.67","-ar","44100","-ac","2",segC])

# Segment D: endcard 10.87-13.87s, silent (matches every prior version)
segD=f"{TMP}/segD.wav"
run([FF,"-y","-f","lavfi","-t","3.0","-i","anullsrc=r=44100:cl=stereo",segD])

# Concat full new audio track (hard concat -- levels are already matched, no crossfade needed)
lst=f"{TMP}/audio_list.txt"
open(lst,"w").write("".join(f"file '{s}'\n" for s in [segA,segB,segC,segD]))
full_audio_raw=f"{TMP}/full_audio_raw.wav"
run([FF,"-y","-f","concat","-safe","0","-i",lst,"-ar","44100","-ac","2",full_audio_raw])

# Get the EXACT source video duration so the muxed output is never shorter than the original
# (concat of 4 separately-trimmed segments can lose a few ms to sample-boundary rounding).
src_dur_str=subprocess.run([FF,"-i",SRC],capture_output=True,text=True).stderr
m=re.search(r"Duration: (\d+):(\d+):([\d.]+)",src_dur_str)
src_dur=int(m.group(1))*3600+int(m.group(2))*60+float(m.group(3))
full_audio=f"{TMP}/full_audio.wav"
run([FF,"-y","-i",full_audio_raw,"-af",f"apad=whole_dur={src_dur}s","-t",str(src_dur),full_audio])

# ============ VIDEO: plate patch overlays, everything else pixel-identical ============
# (x, y, w, h, start, end) -- all in the original 1080x1920 frame
PLATE_WINDOWS=[
    ("s1", 885,1160,195,70, 0.0,   2.1667),
    ("s2", 668,1240,302,55, 2.1667,4.1),
    ("s3", 550,1325,235,65, 4.1,   5.8333),
    ("s4", 715,1048,225,37, 5.8333,7.2),
    ("s5", 385,1210,135,50, 7.2,   9.1333),
    ("s6", 695,1330,245,60, 9.1333,10.8667),
]

inputs=["-i",SRC]
filter_parts=[]
last="[0:v]"
for i,(name,x,y,w,h,st,en) in enumerate(PLATE_WINDOWS):
    inputs+=["-i",f"{PATCH}/{name}.png"]
    idx=i+1
    nxt=f"[v{i}]"
    filter_parts.append(f"{last}[{idx}:v]overlay={x}:{y}:enable='between(t,{st},{en})'{nxt}")
    last=nxt
filter_complex=";".join(filter_parts)

video_patched=f"{TMP}/video_patched.mp4"
run([FF,"-y",*inputs,"-filter_complex",filter_complex,"-map",last,"-an",
     "-c:v","libx264","-preset","slow","-crf","16","-pix_fmt","yuv420p",
     "-r","30",video_patched])

# Mux patched video (visuals otherwise 100% identical) with the new full audio track
out=f"{OUT}/easy-taxi-belgium-ad-9x16-audiofix.mp4"
run([FF,"-y","-i",video_patched,"-i",full_audio,"-c:v","copy","-c:a","aac","-b:a","160k",
     "-ar","48000","-ac","2","-shortest","-movflags","+faststart",out])

d=subprocess.run([FF,"-i",out],capture_output=True,text=True).stderr
print("FINAL exact-audio+plate:",out,"dur",re.search(r"Duration: ([0-9:.]+)",d).group(1))
