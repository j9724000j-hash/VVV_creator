#!/usr/bin/env python3
"""Scene renderer — one scene per invocation: python3 render.py <N>
Timeline source of truth: PROGRESS.md FINAL COMPRESSED TIMELINE v2 (38.90 s total)."""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FF = os.environ.get("FFMPEG_OVERRIDE", os.path.expanduser("~/.local/bin/ffmpeg"))
A = os.path.join(ROOT, "extracted/assets")
SC = os.path.join(ROOT, "project/scenes")
TX = os.path.join(ROOT, "project/texts")
os.makedirs(SC, exist_ok=True)
FONT_XB = os.path.join(A, "06_Fonts/Sora-ExtraBold.ttf")

def zoom_bg(idx, dur, max_zoom):
    inc = (max_zoom - 1.0) / (dur * 30)
    return (f"[{idx}]scale=2160:3840,zoompan=z='min(zoom+{inc:.7f},{max_zoom})'"
            f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,setsar=1[bg];\n")

def pan_bg(idx, dur):
    return (f"[{idx}]scale=1215:2160,crop=1080:1920:67:'(ih-1920)*min(t/{dur:.3f},1)',setsar=1[bg];\n")

def run(n):
    # ---------- inputs ----------
    ins, F = [], ""

    if n == 1:  # HOOK 0.000–3.598 (dur 3.598)
        dur = 3.598
        ins = ["01_Backgrounds/01_Working_Website_Hidden_Risk.png",
               "03_Titles_PNG/01_Hook_First_Line.png",
               "03_Titles_PNG/02_Hook_Question.png",
               "02_Transparent_Elements/08_Red_Warning_Glow.png"]
        F = (zoom_bg(0, dur, 1.06)
             + "[1]format=rgba,fade=t=in:st=0:d=0.15:alpha=1[t1];\n"
             + "[2]format=rgba,fade=t=in:st=2.75:d=0.10:alpha=1[t2];\n"
             + "[3]scale=700:700,gblur=sigma=45,format=rgba,colorchannelmixer=aa=0.85,"
               "fade=t=in:st=3.22:d=0.10:alpha=1,fade=t=out:st=3.42:d=0.16:alpha=1[gl];\n"
             + "[bg][t1]overlay=0:0[o1];\n"
             + "[o1][gl]overlay=190:-40[o2];\n"
             + "[o2][t2]overlay=0:0,format=yuv420p[v]")

    elif n == 2:  # TITLE 3.598–6.881 (dur 3.283)
        dur = 3.283
        ins = ["01_Backgrounds/01_Working_Website_Hidden_Risk.png",
               "01_Backgrounds/03_AI_Discovery.png",
               "03_Titles_PNG/03_PHP2Shell_AI.png"]
        F = ("[0]scale=1080:1920,setsar=1[b0];\n"
             + pan_bg(1, dur)
             + "[b0][bg]xfade=transition=fade:duration=0.25:offset=0[dx];\n"
             + "[2]format=rgba,fade=t=in:st=0.70:d=0.30:alpha=1[t];\n"
             + "[dx][t]overlay=0:0,format=yuv420p[v]")

    elif n == 3:  # HIDDEN CODE 6.881–13.646 (dur 6.765)
        dur = 6.765
        ins = ["01_Backgrounds/04_Hidden_Runtime.png",
               "02_Transparent_Elements/03_Runtime_Layers.png",
               "02_Transparent_Elements/04_PHP_Badge.png",
               "02_Transparent_Elements/07_Cyan_Scan_Beam.png"]
        F = (zoom_bg(0, dur, 1.03)
             + "[1]scale=940:-1,format=rgba,fade=t=in:st=0.45:d=0.35:alpha=1[lr];\n"
             + "[bg][lr]overlay=x=70:y='if(lt(t,0.55),1990,if(lt(t,2.45),1990-(1990-620)*(t-0.55)/1.9,620))'[o1];\n"
             + "[2]scale=300:300,format=rgba,fade=t=in:st=2.60:d=0.25:alpha=1[badge];\n"
             + "[o1][badge]overlay=70:980[o2];\n"
             + "[3]format=rgba,fade=t=in:st=3.30:d=0.20:alpha=1,fade=t=out:st=4.90:d=0.30:alpha=1[beam];\n"
             + "[o2][beam]overlay=0:'150+(1550-150)*min((t-3.30)/1.60,1)'[o3];\n"
             + f"[o3]drawtext=fontfile={FONT_XB}:textfile={TX}/kicker03.txt:fontsize=52:"
               "fontcolor=0xF6F8FA:x=(w-text_w)/2:y=205:shadowcolor=0x000000AA:shadowx=0:shadowy=3,format=yuv420p[v]")

    elif n == 4:  # STAKES 13.646–24.577 (dur 10.931) — 04a/04b/04c
        dur = 10.931
        ins = ["01_Backgrounds/02_Shield_Breach.png",
               "03_Titles_PNG/04_Discovery.png",
               "02_Transparent_Elements/08_Red_Warning_Glow.png",
               "01_Backgrounds/01_Working_Website_Hidden_Risk.png",
               "02_Transparent_Elements/02_Browser_HUD.png",
               "01_Backgrounds/04_Hidden_Runtime.png",
               "02_Transparent_Elements/03_Runtime_Layers.png",
               "02_Transparent_Elements/08_Red_Warning_Glow.png"]
        incA = 0.05 / (2.554 * 30)
        incB = 0.04 / (4.528 * 30)
        incC = 0.04 / (3.849 * 30)
        F = (
            # 04a shield 0–2.554
            f"[0]scale=2160:3840,zoompan=z='min(zoom+{incA:.7f},1.05)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            f":d=1:s=1080x1920:fps=30,setsar=1[bA];\n"
            + "[1]format=rgba,fade=t=in:st=0.95:d=0.30:alpha=1[t4];\n"
            + "[2]scale=1080:1080,gblur=sigma=60,format=rgba,colorchannelmixer=aa=0.9,"
              "fade=t=in:st=1.80:d=0.15:alpha=1,fade=t=out:st=1.98:d=0.24:alpha=1[redp];\n"
            # 04b normal website 2.554–7.082
            + f"[3]scale=2160:3840,zoompan=z='min(zoom+{incB:.7f},1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
              f":d=1:s=1080x1920:fps=30,setsar=1[bB];\n"
            + "[4]scale=880:-1,format=rgba,fade=t=in:st=2.85:d=0.30:alpha=1[hud];\n"
            # 04c runtime 7.082–10.931
            + f"[5]scale=2160:3840,zoompan=z='min(zoom+{incC:.7f},1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
              f":d=1:s=1080x1920:fps=30,setsar=1[bC];\n"
            + "[6]scale=900:-1,format=rgba,fade=t=in:st=7.35:d=0.30:alpha=1[lr2];\n"
            + "[7]scale=900:900,gblur=sigma=55,format=rgba,colorchannelmixer=rr=1:gr=0.55:gg=0.32:bb=0:br=0:aa=0.9,"
              "fade=t=in:st=9.60:d=0.15:alpha=1,fade=t=out:st=9.78:d=0.25:alpha=1[amb];\n"
            # composite
            + "[bA][t4]overlay=0:0[x1];\n"
            + "[x1][redp]overlay=0:460[x2];\n"
            + "[x2][bB]overlay=enable='gte(t,2.554)'[x3];\n"
            + "[x3][hud]overlay=x='40-25*min((t-2.85)/4.0,1)':y='660-40*min((t-2.85)/4.0,1)':"
              "enable='between(t,2.554,7.082)'[x4];\n"
            + "[x4][bC]overlay=enable='gte(t,7.082)'[x5];\n"
            + "[x5][lr2]overlay=x=90:y=640:enable='gte(t,7.082)'[x6];\n"
            + "[x6][amb]overlay=90:380:enable='between(t,9.55,10.10)',format=yuv420p[v]")

    elif n == 5:  # LESSON 24.577–29.953 (dur 5.376)
        dur = 5.376
        ins = ["01_Backgrounds/05_Navy_Grid.png",
               "02_Transparent_Elements/04_PHP_Badge.png",
               "03_Titles_PNG/05_Check_PHP.png"]
        F = (zoom_bg(0, dur, 1.03)
             + "[1]scale=384:384,format=rgba,fade=t=in:st=0.80:d=0.25:alpha=1[badge];\n"
             + "[2]format=rgba,fade=t=in:st=1.07:d=0.30:alpha=1[t5];\n"
             + "[bg][badge]overlay=348:820[o1];\n"
             + f"[o1][t5]overlay=0:0[o2];\n"
             + f"[o2]drawtext=fontfile={FONT_XB}:textfile={TX}/line05.txt:fontsize=46:"
               "fontcolor=0xF6F8FA:x=(w-text_w)/2:y=1276:shadowcolor=0x000000AA:shadowx=0:shadowy=3:"
               "alpha='if(lt(t,3.27),0,min((t-3.27)/0.30,1))',format=yuv420p[v]")

    elif n == 6:  # CURIOSITY 29.953–36.287 (dur 6.334)
        dur = 6.334
        ins = ["01_Backgrounds/05_Navy_Grid.png",
               "02_Transparent_Elements/09_Neural_Network.png",
               "03_Titles_PNG/06_Question.png"]
        F = (zoom_bg(0, dur, 1.025)
             + "[1]format=rgba,fade=t=in:st=0.30:d=0.60:alpha=1[nn];\n"
             + "[2]format=rgba,fade=t=in:st=0.55:d=0.30:alpha=1[t6];\n"
             + "[bg][nn]overlay=x='-20*min(t/6.0,1)':y=0[o1];\n"
             + "[o1][t6]overlay=0:0,format=yuv420p[v]")

    elif n == 7:  # CTA 36.287–38.900 (dur 2.613)
        dur = 2.613
        ins = ["01_Backgrounds/05_Navy_Grid.png",
               "02_Transparent_Elements/08_Red_Warning_Glow.png",
               "02_Transparent_Elements/08_Red_Warning_Glow.png",
               "03_Titles_PNG/07_CTA.png",
               "02_Transparent_Elements/06_Down_Arrow.png",
               "03_Titles_PNG/08_Closing_Brand.png"]
        F = ("[0]scale=1080:1920,setsar=1[b0];\n"
             # brand gradient: navy base + blue glows, faded in over the grid bg (no xfade)
             + "color=c=0x081320:s=1080x1920:d=" + f"{dur + 0.2:.3f}" + "[base];\n"
             + "[1]scale=1500:1500,gblur=sigma=70,format=rgba,colorchannelmixer=rr=0:gr=0.30:gg=0.32:br=0.95:bb=1:aa=0.50[gbig];\n"
             + "[2]scale=800:800,gblur=sigma=60,format=rgba,colorchannelmixer=rr=0:gr=0.25:gg=0.35:br=0.90:bb=1:aa=0.30[gsm];\n"
             + "[base][gbig]overlay=x=-210:y=980[g1];\n"
             + "[g1][gsm]overlay=x=420:y=-260[g2];\n"
             + "[g2]format=rgba,fade=t=in:st=0:d=0.30:alpha=1[gin];\n"
             + "[b0][gin]overlay=0:0[bg];\n"
             + "[3]format=rgba,fade=t=in:st=0.66:d=0.25:alpha=1,fade=t=out:st=1.82:d=0.22:alpha=1[t7];\n"
             + "[4]scale=180:300,format=rgba,fade=t=in:st=1.06:d=0.20:alpha=1[arw];\n"
             + "[5]format=rgba,fade=t=in:st=1.87:d=0.28:alpha=1[t8];\n"
             + "[bg][t7]overlay=0:0[o1];\n"
             + "[o1][arw]overlay=x=450:y='560+14*abs(sin(2*PI*(t-1.06)/0.9))':enable='gte(t,1.06)'[o2];\n"
             + "[o2][t8]overlay=0:0,format=yuv420p[v]")
    else:
        raise SystemExit("scene 1..7 only")

    cmd = [FF, "-y", "-nostdin", "-hide_banner", "-loglevel", "error"]
    for p in ins:
        cmd += ["-loop", "1", "-framerate", "30", "-t", f"{dur + 0.1:.3f}", "-i", os.path.join(A, p)]
    out = os.path.join(SC, f"Scene_{n:02d}.mp4")
    cmd += ["-filter_complex", F, "-map", "[v]", "-t", f"{dur:.3f}",
            "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "17", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stderr[-3000:] if r.returncode else f"OK Scene_{n:02d}.mp4 ({dur}s)")
    return r.returncode

if __name__ == "__main__":
    sys.exit(run(int(sys.argv[1])))
