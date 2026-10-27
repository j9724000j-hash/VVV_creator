#!/usr/bin/env python3
"""Scene renderer v2 — measured timeline, cohesive design system.
Design system: Sora ExtraBold titles (shipped cards) + drawn kickers same font;
Tech_Brand_Strip as recurring identity thread (s02-s06, small, top);
captions zone y~1310 kept clear; hard cuts on sentence boundaries;
dissolves only inside scenes. Timeline source: project/audio/timeline.json
Scenes (video clock): s01 0-3.598 | s02 -6.880 | s03 -13.896 | s04 -24.577
s05 -30.203 | s06 -36.842 | s07 -40.900 (incl. branded outro)"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FF = os.path.expanduser("~/.local/bin/ffmpeg")
A = os.path.join(ROOT, "extracted/assets")
SC = os.path.join(ROOT, "project/scenes")
TX = os.path.join(ROOT, "project/texts")
os.makedirs(SC, exist_ok=True)
FONT = os.path.join(A, "06_Fonts/Sora-ExtraBold.ttf")
STRIP = os.path.join(A, "02_Transparent_Elements/10_Tech_Brand_Strip.png")

def zoom_bg(idx, dur, mz):
    inc = (mz - 1.0) / (dur * 30)
    return (f"[{idx}]scale=2160:3840,zoompan=z='min(zoom+{inc:.7f},{mz})'"
            f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,setsar=1[bg];\n")

def strip_in(idx, tag, st, d=0.4):
    return (f"[{idx}]scale=620:-1,format=rgba,colorchannelmixer=aa=0.92,"
            f"fade=t=in:st={st}:d={d}:alpha=1[{tag}];\n")

def cap_in(idx, tag, st, d=0.4):
    return (f"[{idx}]format=rgba,fade=t=in:st={st}:d={d}:alpha=1[{tag}];\n")

def run(n):
    ins, F = [], ""
    O = []  # extra movie inputs handled via movie filter (strip)

    if n == 1:  # HOOK 0–3.598
        dur = 3.598
        ins = ["01_Backgrounds/01_Working_Website_Hidden_Risk.png",
               "03_Titles_PNG/01_Hook_First_Line.png",
               "03_Titles_PNG/02_Hook_Question.png",
               "02_Transparent_Elements/08_Red_Warning_Glow.png"]
        F = (zoom_bg(0, dur, 1.06)
             + "[1]format=rgba,fade=t=in:st=0:d=0.15:alpha=1,fade=t=out:st=2.90:d=0.15:alpha=1[t1];\n"
             + "[2]format=rgba,fade=t=in:st=3.05:d=0.10:alpha=1[t2];\n"
             + "[3]scale=700:700,gblur=sigma=45,format=rgba,colorchannelmixer=aa=0.85,"
               "fade=t=in:st=3.25:d=0.10:alpha=1,fade=t=out:st=3.44:d=0.15:alpha=1[gl];\n"
             + "[bg][t1]overlay=0:0[o1];\n"
             + "[o1][gl]overlay=190:-40[o2];\n"
             + "[o2][t2]overlay=0:0,format=yuv420p[v]")

    elif n == 2:  # TITLE 3.598–6.880 (dur 3.282) "Behind every page…"
        dur = 3.282
        ins = ["01_Backgrounds/01_Working_Website_Hidden_Risk.png",
               "01_Backgrounds/03_AI_Discovery.png",
               "02_Transparent_Elements/10_Tech_Brand_Strip.png",
               "02_Transparent_Elements/01_Readability_Shade.png"]
        F = ("[0]scale=1080:1920,setsar=1[b0];\n"
             + f"[1]scale=1215:2160,crop=1080:1920:67:'(ih-1920)*min(t/{dur:.3f},1)',setsar=1,"
               "format=rgba,fade=t=in:st=0:d=0.25:alpha=1[pan];\n"
             + "[b0][pan]overlay=0:0[bg];\n"
             + strip_in(2, "st", 0.45)
             + cap_in(3, "cap", 0.45)
             + "[bg][st]overlay=(W-w)/2:52[s1];\n"
             + "[s1][cap]overlay=0:0[s2];\n"
             + f"[s2]drawtext=fontfile={FONT}:textfile={TX}/kicker03.txt:fontsize=52:"
               "fontcolor=0xF6F8FA:x=(w-text_w)/2:y=205:shadowcolor=0x000000AA:shadowx=0:shadowy=3:"
               "alpha='if(lt(t,0.35),0,min((t-0.35)/0.30,1))',format=yuv420p[v]")

    elif n == 3:  # LAYERS 6.880–13.896 (dur 7.016) — c4 "article…" + c5 "when AI…"
        dur = 7.016
        ins = ["01_Backgrounds/04_Hidden_Runtime.png",
               "02_Transparent_Elements/03_Runtime_Layers.png",
               "02_Transparent_Elements/04_PHP_Badge.png",
               "02_Transparent_Elements/07_Cyan_Scan_Beam.png",
               "02_Transparent_Elements/10_Tech_Brand_Strip.png",
               "02_Transparent_Elements/01_Readability_Shade.png",
               "03_Titles_PNG/03_PHP2Shell_AI.png"]
        F = (zoom_bg(0, dur, 1.03)
             + "[1]scale=940:-1,format=rgba,fade=t=in:st=0.42:d=0.35:alpha=1[lr];\n"
             + "[bg][lr]overlay=x=70:y='if(lt(t,0.52),1990,if(lt(t,2.42),1990-(1990-620)*(t-0.52)/1.9,620))'[o1];\n"
             + "[2]scale=300:300,format=rgba,fade=t=in:st=2.15:d=0.25:alpha=1[badge];\n"
             + "[o1][badge]overlay=70:980[o2];\n"
             + "[3]format=rgba,fade=t=in:st=3.28:d=0.20:alpha=1,fade=t=out:st=5.10:d=0.35:alpha=1[beam];\n"
             + "[o2][beam]overlay=0:'150+(1550-150)*min((t-3.28)/1.60,1)'[o3];\n"
             + strip_in(4, "st", 0.35)
             + cap_in(5, "cap", 0.35)
             + "[o3][st]overlay=(W-w)/2:52[s4];\n"
             + "[s4][cap]overlay=0:0[s5];\n"
             + "[6]format=rgba,fade=t=in:st=0.15:d=0.30:alpha=1[t3];\n"
             + "[s5][t3]overlay=0:0,format=yuv420p[v]")

    elif n == 4:  # STAKES 13.896-20.478 (dur 6.582) - voice-aligned beats
        dur = 6.582
        ins = ["01_Backgrounds/02_Shield_Breach.png",
               "03_Titles_PNG/04_Discovery.png",
               "02_Transparent_Elements/08_Red_Warning_Glow.png",
               "01_Backgrounds/01_Working_Website_Hidden_Risk.png",
               "02_Transparent_Elements/02_Browser_HUD.png",
               "01_Backgrounds/04_Hidden_Runtime.png",
               "02_Transparent_Elements/03_Runtime_Layers.png",
               "02_Transparent_Elements/08_Red_Warning_Glow.png",
               "02_Transparent_Elements/10_Tech_Brand_Strip.png",
               "02_Transparent_Elements/01_Readability_Shade.png"]
        iA, iB, iC = 0.05 / (2.30 * 30), 0.03 / (1.65 * 30), 0.04 / (2.65 * 30)
        F = (
            f"[0]scale=2160:3840,zoompan=z='min(zoom+{iA:.7f},1.05)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            f":d=1:s=1080x1920:fps=30,setsar=1[bA];\n"
            + "[1]format=rgba,fade=t=in:st=0.85:d=0.28:alpha=1[t4];\n"
            + "[2]scale=1080:1080,gblur=sigma=60,format=rgba,colorchannelmixer=aa=0.9,"
              "fade=t=in:st=1.45:d=0.15:alpha=1,fade=t=out:st=1.95:d=0.28:alpha=1[redp];\n"
            + f"[3]scale=2160:3840,zoompan=z='min(zoom+{iB:.7f},1.03)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
              f":d=1:s=1080x1920:fps=30,setsar=1[bB];\n"
            + "[4]scale=920:-1,format=rgba,fade=t=in:st=2.55:d=0.28:alpha=1[hud];\n"
            + f"[5]scale=2160:3840,zoompan=z='min(zoom+{iC:.7f},1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
              f":d=1:s=1080x1920:fps=30,setsar=1[bC];\n"
            + "[6]scale=900:-1,format=rgba,fade=t=in:st=4.10:d=0.28:alpha=1[lr2];\n"
            + "[7]scale=900:900,gblur=sigma=55,format=rgba,colorchannelmixer=rr=1:gr=0.55:gg=0.32:bb=0:br=0:aa=0.9,"
              "fade=t=in:st=5.85:d=0.15:alpha=1,fade=t=out:st=6.13:d=0.28:alpha=1[amb];\n"
            + "[bA][t4]overlay=0:0[x1];\n"
            + "[x1][redp]overlay=0:460[x2];\n"
            + "[x2][bB]overlay=enable='gte(t,2.30)'[x3];\n"
            + "[x3][hud]overlay=x='60-26*min((t-2.55)/1.4,1)':y='640-40*min((t-2.55)/1.4,1)':"
              "enable='between(t,2.30,3.95)'[x4];\n"
            + "[x4][bC]overlay=enable='gte(t,3.95)'[x5];\n"
            + "[x5][lr2]overlay=x=90:y=640:enable='gte(t,3.95)'[x6];\n"
            + "[x6][amb]overlay=90:380:enable='between(t,5.80,6.45)'[x7];\n"
            + "[8]scale=620:-1,format=rgba,colorchannelmixer=aa=0.92,fade=t=in:st=0.30:d=0.4:alpha=1[st];\n"
            + "[x7][st]overlay=(W-w)/2:52[s1];\n"
            + "[9]format=rgba,fade=t=in:st=0.30:d=0.4:alpha=1[cap];\n"
            + "[s1][cap]overlay=0:0,format=yuv420p[v]")

    elif n == 5:  # LESSON 20.478-24.577 (dur 4.099)
        dur = 4.099
        ins = ["01_Backgrounds/05_Navy_Grid.png",
               "02_Transparent_Elements/04_PHP_Badge.png",
               "03_Titles_PNG/05_Check_PHP.png",
               "02_Transparent_Elements/10_Tech_Brand_Strip.png",
               "02_Transparent_Elements/01_Readability_Shade.png"]
        F = (zoom_bg(0, dur, 1.03)
             + "[1]scale=384:384,format=rgba,fade=t=in:st=0.35:d=0.25:alpha=1[badge];\n"
             + "[2]format=rgba,fade=t=in:st=1.15:d=0.28:alpha=1[t5];\n"
             + "[bg][badge]overlay=348:830[o1];\n"
             + "[o1][t5]overlay=0:0[o2];\n"
             + "[3]scale=620:-1,format=rgba,colorchannelmixer=aa=0.92,fade=t=in:st=0.35:d=0.4:alpha=1[st];\n"
             + "[o2][st]overlay=(W-w)/2:52[s3];\n"
             + "[4]format=rgba,fade=t=in:st=0.35:d=0.4:alpha=1[cap];\n"
             + "[s3][cap]overlay=0:0,format=yuv420p[v]")

    elif n == 6:  # QUESTION 24.577-29.953 (dur 5.376)
        dur = 5.376
        ins = ["01_Backgrounds/05_Navy_Grid.png",
               "02_Transparent_Elements/09_Neural_Network.png",
               "03_Titles_PNG/06_Question.png",
               "02_Transparent_Elements/10_Tech_Brand_Strip.png",
               "02_Transparent_Elements/01_Readability_Shade.png"]
        F = (zoom_bg(0, dur, 1.025)
             + "[1]format=rgba,fade=t=in:st=0.25:d=0.55:alpha=1[nn];\n"
             + "[2]format=rgba,fade=t=in:st=0.60:d=0.28:alpha=1[t6];\n"
             + "[bg][nn]overlay=x='-20*min(t/5.0,1)':y=0[o1];\n"
             + "[o1][t6]overlay=0:0[o2];\n"
             + "[3]scale=620:-1,format=rgba,colorchannelmixer=aa=0.92,fade=t=in:st=0.35:d=0.4:alpha=1[st];\n"
             + "[o2][st]overlay=(W-w)/2:52[s3];\n"
             + "[4]format=rgba,fade=t=in:st=0.35:d=0.4:alpha=1[cap];\n"
             + "[s3][cap]overlay=0:0,format=yuv420p[v]")

    elif n == 7:  # READ-CTA (light editorial) + FINAL LINE (comments card) + BRAND OUTRO
        dur = 10.947
        ins = ["01_Backgrounds/06_Light_Editorial.png",
               "02_Transparent_Elements/04_PHP_Badge.png",
               "01_Backgrounds/05_Navy_Grid.png",
               "02_Transparent_Elements/08_Red_Warning_Glow.png",
               "02_Transparent_Elements/08_Red_Warning_Glow.png",
               "02_Transparent_Elements/05_Comments_CTA.png",
               "02_Transparent_Elements/06_Down_Arrow.png",
               "03_Titles_PNG/08_Closing_Brand.png",
               "02_Transparent_Elements/10_Tech_Brand_Strip.png"]
        incL = 0.05 / (6.5 * 30)
        F = (
            f"[0]scale=2160:3840,zoompan=z='min(zoom+{incL:.7f},1.05)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            f":d=1:s=1080x1920:fps=30,setsar=1[light];\n"
            + "[1]scale=330:330,format=rgba,fade=t=in:st=0.85:d=0.28:alpha=1[badge];\n"
            + "[light][badge]overlay=(W-w)/2:830[la];\n"
            + "[8]scale=620:-1,format=rgba,colorchannelmixer=aa=0.92,fade=t=in:st=0.45:d=0.4:alpha=1[st];\n"
            + "[la][st]overlay=(W-w)/2:52[lb];\n"
            + "color=c=0x081320:s=1080x1920:d=11.2[base];\n"
            + "[3]scale=1600:1600,gblur=sigma=80,format=rgba,colorchannelmixer=rr=0:gr=0.30:gg=0.32:br=0.95:bb=1:aa=0.55[gbig];\n"
            + "[4]scale=850:850,gblur=sigma=65,format=rgba,colorchannelmixer=rr=0:gr=0.25:gg=0.35:br=0.90:bb=1:aa=0.32[gsm];\n"
            + "[base][gbig]overlay=x=-230:y=1020[g1];\n"
            + "[g1][gsm]overlay=x=460:y=-290[g2];\n"
            + "[2]scale=1080:1920,setsar=1[g3];\n"
            + "[g3][g2]overlay=0:0[gt];\n"
            + "[gt]format=rgba,fade=t=in:st=5.95:d=0.35:alpha=1[gin];\n"
            + "[lb][gin]overlay=0:0[bg];\n"
            + "[5]scale=760:-1,format=rgba,fade=t=in:st=6.75:d=0.25:alpha=1,"
              "fade=t=out:st=8.30:d=0.28:alpha=1[card];\n"
            + "[6]scale=228:380,format=rgba,fade=t=in:st=7.05:d=0.20:alpha=1,"
              "fade=t=out:st=8.32:d=0.25:alpha=1[arw];\n"
            + "[7]scale=1080:1920,format=rgba,crop=1080:1840:0:0,fade=t=in:st=8.60:d=0.35:alpha=1[t8];\n"
            + "[bg][card]overlay=x=160:'1150+8*sin(6*(t-6.75))':enable='between(t,6.75,8.62)'[o1];\n"
            + "[o1][arw]overlay=x=426:'1408+14*abs(sin(2*PI*(t-7.05)/0.9))':enable='between(t,7.05,8.62)'[o2];\n"
            + "[o2][t8]overlay=0:80,format=yuv420p[v]")

    else:
        raise SystemExit("scene 1..7 only")

    cmd = [FF, "-y", "-nostdin", "-hide_banner", "-loglevel", "error"]
    for p in ins:
        cmd += ["-loop", "1", "-framerate", "30", "-t", f"{dur + 0.1:.3f}", "-i", os.path.join(A, p)]
    out = os.path.join(SC, f"Scene_{n:02d}.mp4")
    cmd += ["-filter_complex", F, "-map", "[v]", "-t", f"{dur:.3f}",
            "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "17", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stderr[-2500:] if r.returncode else f"OK Scene_{n:02d}.mp4 ({dur}s)")
    return r.returncode

if __name__ == "__main__":
    sys.exit(run(int(sys.argv[1])))
