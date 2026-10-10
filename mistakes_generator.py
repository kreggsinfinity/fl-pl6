"""
Common English Mistakes Fixer - Video Generator (9:16 Vertical Reel)
"90% of Learners Make This Mistake! Stop Saying THIS, Say THAT!"
"""
import os, sys, json, subprocess, random, requests, re, asyncio
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from dotenv import load_dotenv
import edge_tts

load_dotenv()

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

WIDTH = 1080
HEIGHT = 1920
FPS = 30

BG_DARK = (20, 16, 26)
ALERT_RED = (239, 68, 68)
SUCCESS_GREEN = (16, 185, 129)
WARNING_YELLOW = (250, 204, 21)
WHITE = (255, 255, 255)
CARD_BG = (32, 26, 42)

VOICE_NATIVE = "en-US-AvaNeural"

MISTAKES = [
    {
        "wrong": "I am agree with you.",
        "right": "I agree with you.",
        "rule": "'Agree' is already a verb, not an adjective! Never say 'I am agree'.",
        "repeat": "Repeat after me: I AGREE with you. Perfect!",
        "script": [
            "Ninety percent of English learners make this mistake! Stop saying: I am agree with you.",
            "Instead, always say: I AGREE with you! Agree is already an action verb, so you do not need 'am'.",
            "Repeat after me: I agree with you. Perfect! Save this reel so you never make this mistake again!"
        ]
    },
    {
        "wrong": "I lost the bus this morning.",
        "right": "I MISSED the bus this morning.",
        "rule": "Use 'lose' for items you can't find (keys, wallet). Use 'miss' for transport (bus, train, flight)!",
        "repeat": "Repeat after me: I MISSED the bus.",
        "script": [
            "Stop saying 'I lost the bus'! Unless the bus disappeared into thin air, that is incorrect.",
            "You LOSE your keys or wallet, but for transportation, you always say: I MISSED the bus!",
            "Repeat after me: I missed the bus! Follow for daily grammar fixes!"
        ]
    }
]

def load_font(size, bold=True):
    fonts_to_try = [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in fonts_to_try:
        if Path(p).exists():
            try: return ImageFont.truetype(p, size)
            except: continue
    return ImageFont.load_default()

def render_mistake_frame(item, step_idx, total_steps, out_path):
    canvas = Image.new("RGBA", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(canvas)

    # Gradient background
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(20 + ratio * 15)
        g = int(16 + ratio * 10)
        b = int(26 + ratio * 25)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b, 255))

    # Top Alert Badge
    draw.rounded_rectangle([(70, 90), (WIDTH - 70, 180)], radius=22, fill=(45, 20, 25), outline=ALERT_RED, width=3)
    f_hdr = load_font(32, bold=True)
    draw.text((WIDTH // 2, 135), "⚠️ COMMON ENGLISH MISTAKE ALERT", fill=WARNING_YELLOW, font=f_hdr, anchor="mm")

    # Main Headline Hook
    f_hook = load_font(52, bold=True)
    draw.text((WIDTH // 2, 260), "STOP SAYING THIS!", fill=WHITE, font=f_hook, anchor="mm")

    # 1. WRONG CARD (Red)
    draw.rounded_rectangle([(70, 330), (WIDTH - 70, 580)], radius=28, fill=(45, 18, 25), outline=ALERT_RED, width=4)
    f_tag = load_font(26, bold=True)
    draw.rounded_rectangle([(110, 355), (380, 405)], radius=12, fill=ALERT_RED)
    draw.text((245, 380), "❌ INCORRECT", fill=WHITE, font=f_tag, anchor="mm")

    f_wrong = load_font(55, bold=True)
    draw.text((WIDTH // 2, 480), f'"{item["wrong"]}"', fill=(255, 180, 180), font=f_wrong, anchor="mm")

    # Arrow Down
    f_arrow = load_font(46, bold=True)
    draw.text((WIDTH // 2, 640), "⬇️ SAY THIS INSTEAD ⬇️", fill=WARNING_YELLOW, font=f_arrow, anchor="mm")

    # 2. CORRECT CARD (Green)
    draw.rounded_rectangle([(70, 710), (WIDTH - 70, 990)], radius=28, fill=(15, 45, 35), outline=SUCCESS_GREEN, width=5)
    draw.rounded_rectangle([(110, 735), (420, 785)], radius=12, fill=SUCCESS_GREEN)
    draw.text((265, 760), "✅ 100% CORRECT", fill=WHITE, font=f_tag, anchor="mm")

    f_right = load_font(68, bold=True)
    draw.text((WIDTH // 2, 870), f'"{item["right"]}"', fill=WHITE, font=f_right, anchor="mm")

    # 3. THE GOLDEN RULE CARD
    draw.rounded_rectangle([(70, 1060), (WIDTH - 70, 1380)], radius=28, fill=CARD_BG, outline=WARNING_YELLOW, width=3)
    f_rule_lbl = load_font(30, bold=True)
    draw.text((110, 1105), "💡 WHY? THE GRAMMAR RULE:", fill=WARNING_YELLOW, font=f_rule_lbl, anchor="lm")

    f_rule_txt = load_font(38, bold=False)
    rwords = item["rule"].split()
    rlines = []
    cr = []
    for rw in rwords:
        tb = draw.textbbox((0, 0), " ".join(cr + [rw]), font=f_rule_txt)
        if tb[2] - tb[0] > (WIDTH - 240):
            rlines.append(" ".join(cr))
            cr = [rw]
        else:
            cr = [rw]
    if cr: rlines.append(" ".join(cr))
    for rl_idx, rl in enumerate(rlines):
        draw.text((110, 1175 + rl_idx * 55), rl, fill=WHITE, font=f_rule_txt, anchor="lm")

    # 4. PRONUNCIATION / REPEAT CARD
    draw.rounded_rectangle([(70, 1440), (WIDTH - 70, 1690)], radius=25, fill=(25, 35, 60), outline=(59, 130, 246), width=3)
    f_rep_lbl = load_font(28, bold=True)
    draw.text((110, 1485), "🗣️ SPEAKING & PRONUNCIATION PRACTICE:", fill=(96, 165, 250), font=f_rep_lbl, anchor="lm")
    f_rep_txt = load_font(42, bold=True)
    draw.text((WIDTH // 2, 1585), item["repeat"], fill=WARNING_YELLOW, font=f_rep_txt, anchor="mm")

    # Footer
    f_cta = load_font(32, bold=True)
    draw.text((WIDTH // 2, 1780), "❤️ Double tap & Save so you never forget!", fill=WARNING_YELLOW, font=f_cta, anchor="mm")
    f_sub = load_font(26, bold=False)
    draw.text((WIDTH // 2, 1835), "Follow Common Mistakes Fixer for daily tips!", fill=(156, 163, 175), font=f_sub, anchor="mm")

    canvas.convert("RGB").save(out_path, quality=95)

async def assemble_mistake_reel(item, run_dir):
    frames_dir = run_dir / "frames"
    clips_dir = run_dir / "clips"
    audio_dir = run_dir / "audio"
    for d in [frames_dir, clips_dir, audio_dir]:
        d.mkdir(parents=True, exist_ok=True)

    clips = []
    total_steps = len(item["script"])

    for s_idx, text in enumerate(item["script"]):
        mp3_p = audio_dir / f"step_{s_idx}.mp3"
        await edge_tts.Communicate(text, VOICE_NATIVE, rate="-10%").save(str(mp3_p))

        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(mp3_p)],
            capture_output=True, text=True, check=True
        )
        dur = float(r.stdout.strip())

        frame_p = frames_dir / f"frame_{s_idx}.png"
        render_mistake_frame(item, s_idx, total_steps, str(frame_p))

        clip_p = clips_dir / f"clip_{s_idx}.mp4"
        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-i", str(frame_p), "-i", str(mp3_p),
            "-vf", f"scale={WIDTH}:{HEIGHT},fps={FPS}",
            "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p", "-preset", "fast", "-t", f"{dur:.3f}", str(clip_p)
        ], check=True, capture_output=True)

        clips.append(clip_p)

    concat_txt = run_dir / "concat.txt"
    with open(concat_txt, "w") as f:
        for c in clips:
            f.write(f"file '{c.resolve().as_posix()}'\n")

    final_v = run_dir / "common_mistakes_reel.mp4"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(final_v)], check=True, capture_output=True)
    return final_v

async def run_mistakes_generation(idx=0):
    item = MISTAKES[idx % len(MISTAKES)]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = OUTPUT_DIR / f"run_{ts}"
    run_dir.mkdir(parents=True, exist_ok=True)

    print(f"[Common Mistakes] Generating Reel for: '{item['wrong']}' -> '{item['right']}'...")
    final_v = await assemble_mistake_reel(item, run_dir)

    meta = {
        "title": f"Stop saying '{item['wrong']}'! ⚠️ Say '{item['right']}' instead!",
        "description": f"90% of English learners make this mistake! Learn why '{item['wrong']}' is incorrect and how to say '{item['right']}'. Rule: {item['rule']} Follow for daily fixes! 🌟",
        "wrong": item["wrong"],
        "right": item["right"]
    }
    with open(run_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"[Common Mistakes] Video ready: {final_v}")
    return final_v, meta
