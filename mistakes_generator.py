"""
ENGLISH MISTAKES CLINIC PODCAST - 16:9 FULL HD (1920x1080) VIDEO GENERATOR
Theme: Linguistics Clinic / Dark Audio Lab
Visuals: Side-by-Side Mistake vs Fix Board + Dual Cantilever Mics + 26-Bar Dot-Matrix Equalizer + Single-Line Highlighted Subtitles
"""
import os, sys, json, math, subprocess, random, requests, re, asyncio
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from dotenv import load_dotenv
import edge_tts

if sys.platform == 'win32':
    try: sys.stdout.reconfigure(encoding='utf-8')
    except Exception: pass

load_dotenv()

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
SUBFRAMES_PER_SEC = 2

ALERT_RED = (239, 68, 68)
FIX_GREEN = (16, 185, 129)
ACCENT_TEAL = (20, 184, 166)
GOLD_ACCENT = (250, 204, 21)
WHITE = (255, 255, 255)
DARK_BG = (15, 18, 26)
CARD_BG = (22, 28, 40)
CARD_BORDER = (45, 58, 80)
MUTED_TEXT = (160, 175, 195)

EMMA_VOICE = "en-US-AvaNeural"
ANDREW_VOICE = "en-US-AndrewNeural"
VOICE_RATE = "-15%"

TOPICS = [
    {
        "topic": "Why 'I Am Agree' Is Wrong and How To Say It Correctly",
        "wrong": "I AM AGREE",
        "right": "I AGREE WITH YOU",
        "keyword": "AGREE",
        "sub": "STOP CONFUSING VERBS AND ADJECTIVES"
    },
    {
        "topic": "Did You Lose or Miss The Bus? Transport Traps Explained",
        "wrong": "I LOST THE BUS",
        "right": "I MISSED THE BUS",
        "keyword": "MISSED",
        "sub": "LOSE VS MISS IN DAILY ENGLISH"
    },
    {
        "topic": "Stop Saying 'I Have 25 Years'! Age Expressions in English",
        "wrong": "I HAVE 25 YEARS",
        "right": "I AM 25 YEARS OLD",
        "keyword": "YEARS",
        "sub": "STATING YOUR AGE NATURALLY"
    }
]

def load_font(size, bold=True):
    fonts_to_try = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/trebucbd.ttf" if bold else "C:/Windows/Fonts/trebuc.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in fonts_to_try:
        if Path(p).exists():
            try: return ImageFont.truetype(p, size)
            except: continue
    return ImageFont.load_default()

def clean_text(text):
    text = re.sub(r'\b(mm+|um+|uh+|ah+)\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def generate_script_ai(topic_item, target_turns=6):
    prompt = f"""Write {target_turns} turns of a slow, clear English podcast between Emma and Andrew.
Topic: {topic_item['topic']}
Mistake to avoid: {topic_item['wrong']}
Correct native phrasing: {topic_item['right']}

RULES:
- Dialogue alternating between Host1 (Emma) and Host2 (Andrew)
- Each turn MUST be 2-3 short, clear sentences (18-28 words)
- Explain why non-native speakers make this mistake, why it sounds unnatural, and drill the correct phrasing
- Wrap exactly 1 key learning word per turn in **asterisks**
- Return as clean JSON array only:
[{{"speaker":"Host1","text":"..."}},{{"speaker":"Host2","text":"..."}}]"""

    key = os.getenv("POLLINATIONS_API_KEY")
    if key:
        try:
            resp = requests.post("https://gen.pollinations.ai/v1/chat/completions", json={
                "model": "gemini-fast",
                "messages": [
                    {"role": "system", "content": "You write educational, natural English mistakes and pronunciation clinic podcast dialogue. Wrap 1 key word per turn in **asterisks**."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.8
            }, headers={"Authorization": f"Bearer {key}"}, timeout=60)
            if resp.status_code == 200:
                raw = resp.json()["choices"][0]["message"]["content"].strip()
                if "```json" in raw: raw = raw.split("```json")[1].split("```")[0].strip()
                elif "```" in raw: raw = raw.split("```")[1].split("```")[0].strip()
                script = json.loads(raw)
                if isinstance(script, list) and len(script) > 0:
                    for i, turn in enumerate(script):
                        turn["speaker"] = "Host1" if i % 2 == 0 else "Host2"
                        turn["text"] = clean_text(turn["text"])
                        if "**" not in turn["text"]:
                            words = turn["text"].split()
                            if len(words) > 2:
                                idx = len(words) // 2
                                words[idx] = f"**{words[idx]}**"
                                turn["text"] = " ".join(words)
                    return script[:target_turns]
        except Exception as e:
            print(f"[script] AI note: {e}, using curated fallback.")

    return [
        {"speaker": "Host1", "text": f"Welcome back to the clinic! Today we are tackling a huge mistake: saying **{topic_item['wrong']}**."},
        {"speaker": "Host2", "text": f"Many learners translate directly from their native language, but in English, you simply say **{topic_item['right']}**."},
        {"speaker": "Host1", "text": f"That is because agree is an action verb on its own, so adding 'am' is grammatically **redundant**."},
        {"speaker": "Host2", "text": f"Practice saying {topic_item['right']} five times today and you will never make that **mistake** again!"}
    ][:target_turns]

async def generate_audio_files(turns, run_dir):
    audio_dir = run_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    audio_list = []
    for i, turn in enumerate(turns):
        mp3_p = audio_dir / f"turn_{i:03d}.mp3"
        spoken = re.sub(r'\*\*(.*?)\*\*', r'\1', turn["text"])
        voice = EMMA_VOICE if turn["speaker"] == "Host1" else ANDREW_VOICE
        comm = edge_tts.Communicate(spoken, voice, rate=VOICE_RATE)
        await comm.save(str(mp3_p))

        try:
            r = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", str(mp3_p)],
                capture_output=True, text=True, check=True
            )
            duration = float(r.stdout.strip())
        except:
            duration = 5.0
        audio_list.append({"path": str(mp3_p), "duration": duration, "speaker": turn["speaker"]})
    return audio_list

def draw_lab_mic(draw, center_x, center_y, is_active, host_label):
    # Desk mount base
    ring_c = FIX_GREEN if is_active else (50, 65, 85)
    draw.ellipse([(center_x - 65, center_y + 115), (center_x + 65, center_y + 135)], fill=(20, 26, 36), outline=ring_c, width=3)
    # Articulated boom arm
    draw.line([(center_x, center_y + 120), (center_x - 20, center_y + 40)], fill=(60, 75, 100), width=6)
    draw.line([(center_x - 20, center_y + 40), (center_x, center_y - 15)], fill=(60, 75, 100), width=6)

    # Status LED Ring
    led_c = FIX_GREEN if is_active else (30, 70, 50)
    draw.ellipse([(center_x - 16, center_y - 25), (center_x + 16, center_y - 5)], fill=led_c)

    # Microphone capsule
    mic_c = (25, 34, 48) if not is_active else (35, 52, 70)
    draw.rounded_rectangle([(center_x - 32, center_y - 95), (center_x + 32, center_y - 25)], radius=16, fill=mic_c, outline=FIX_GREEN if is_active else CARD_BORDER, width=3)
    for gy in range(center_y - 85, center_y - 35, 10):
        draw.line([(center_x - 24, gy), (center_x + 24, gy)], fill=ACCENT_TEAL if is_active else (55, 70, 95), width=2)

    # Host Label
    f_p = load_font(22, bold=True)
    box_c = (22, 32, 46) if not is_active else (16, 75, 55)
    draw.rounded_rectangle([(center_x - 85, center_y + 145), (center_x + 85, center_y + 180)], radius=8, fill=box_c, outline=FIX_GREEN, width=2)
    tag = f"🎙️ {host_label}" + (" (SPEAKER)" if is_active else "")
    draw.text((center_x, center_y + 162), tag, fill=WHITE if is_active else MUTED_TEXT, font=f_p, anchor="mm")

def draw_dotmatrix_equalizer(draw, center_x, center_y, width, height, sub_idx, is_speaking):
    num_bars = 26
    bar_w = 8
    gap = (width - (num_bars * bar_w)) // (num_bars - 1)

    draw.rounded_rectangle([(center_x - width//2 - 18, center_y - height//2 - 12),
                            (center_x + width//2 + 18, center_y + height//2 + 12)],
                           radius=16, fill=(18, 22, 34), outline=ACCENT_TEAL, width=2)

    f_hud = load_font(18, bold=True)
    draw.text((center_x, center_y - height//2 - 1), "• LINGUISTICS AUDIO FREQUENCY ANALYZER •", fill=ACCENT_TEAL, font=f_hud, anchor="mm")

    start_x = center_x - width//2
    for b in range(num_bars):
        if is_speaking:
            phase = sub_idx * 0.88 + b * 0.4
            wave = abs(math.sin(phase)) * 0.72 + abs(math.cos(phase * 1.4)) * 0.28
            bar_h = int(12 + wave * (height - 28))
        else:
            bar_h = 8

        bx = start_x + b * (bar_w + gap)
        by = center_y + height//2 - 8 - bar_h

        # Segmented dot-matrix look
        fill_c = FIX_GREEN if b % 2 == 0 else ACCENT_TEAL
        draw.rounded_rectangle([(bx, by), (bx + bar_w, center_y + height//2 - 8)], radius=3, fill=fill_c)

def render_podcast_subframe(topic_item, turn, turn_idx, sub_idx, total_subframes, elapsed, total_dur, out_path):
    canvas = Image.new("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT), DARK_BG)
    draw = ImageDraw.Draw(canvas)

    # Modern Audio Clinic gradient background
    for y in range(VIDEO_HEIGHT):
        ratio = y / VIDEO_HEIGHT
        r = int(15 + ratio * 10)
        g = int(20 + ratio * 15)
        b = int(28 + ratio * 20)
        draw.line([(0, y), (VIDEO_WIDTH, y)], fill=(r, g, b, 255))

    # Acoustic wall diffuser vertical slats
    for sx in range(120, VIDEO_WIDTH, 140):
        draw.line([(sx, 120), (sx, 650)], fill=(25, 34, 48), width=2)

    # Top Header Deck
    # Left: Channel badge
    draw.rounded_rectangle([(60, 36), (560, 106)], radius=16, fill=CARD_BG, outline=ACCENT_TEAL, width=2)
    f_brand = load_font(28, bold=True)
    draw.text((310, 71), "🔬 MISTAKES CLINIC", fill=WHITE, font=f_brand, anchor="mm")

    # Center: Focus Topic
    draw.rounded_rectangle([(590, 36), (1450, 106)], radius=16, fill=(20, 32, 46), outline=FIX_GREEN, width=2)
    f_scen = load_font(26, bold=True)
    draw.text((1020, 71), f"⚠️ DIAGNOSIS: {topic_item['sub']}", fill=GOLD_ACCENT, font=f_scen, anchor="mm")

    # Right: Live Pill
    draw.rounded_rectangle([(1480, 36), (1860, 106)], radius=16, fill=(35, 18, 26), outline=ALERT_RED, width=3)
    f_air = load_font(26, bold=True)
    dot_color = ALERT_RED if (sub_idx % 2 == 0) else (100, 20, 20)
    draw.ellipse([(1515, 61), (1535, 81)], fill=dot_color)
    draw.text((1685, 71), "AUDIO LAB LIVE", fill=WHITE, font=f_air, anchor="mm")

    # Visual Studio Centerpiece: Mistake vs Fix Side-by-Side Screen & Analyzer
    is_emma = (turn["speaker"] == "Host1")
    is_andrew = not is_emma

    # Left Mic: Emma
    draw_lab_mic(draw, center_x=320, center_y=370, is_active=is_emma, host_label="EMMA")

    # Center Screen: Dual Correction Comparison Cards
    # Left Box: Wrong (Red)
    draw.rounded_rectangle([(520, 160), (930, 350)], radius=18, fill=(45, 18, 22), outline=ALERT_RED, width=3)
    f_h = load_font(22, bold=True)
    draw.text((725, 195), "❌ COMMON ERROR (AVOID)", fill=ALERT_RED, font=f_h, anchor="mm")
    f_w = load_font(34, bold=True)
    draw.text((725, 270), f"\"{topic_item['wrong']}\"", fill=WHITE, font=f_w, anchor="mm")

    # Right Box: Correct (Green)
    draw.rounded_rectangle([(990, 160), (1400, 350)], radius=18, fill=(18, 48, 36), outline=FIX_GREEN, width=3)
    draw.text((1195, 195), "✅ NATIVE UPGRADE (USE)", fill=FIX_GREEN, font=f_h, anchor="mm")
    f_r = load_font(34, bold=True)
    draw.text((1195, 270), f"\"{topic_item['right']}\"", fill=GOLD_ACCENT, font=f_r, anchor="mm")

    # Center Equalizer Deck (Below comparison cards)
    draw_dotmatrix_equalizer(draw, center_x=960, center_y=480, width=540, height=130, sub_idx=sub_idx, is_speaking=True)

    # Right Mic: Andrew
    draw_lab_mic(draw, center_x=1600, center_y=370, is_active=is_andrew, host_label="ANDREW")

    # LOWER THIRD: SLEEK SINGLE-LINE SUBTITLE DISPLAY WITH WORD-BY-WORD HIGHLIGHTING
    draw.rounded_rectangle([(100, 680), (1820, 930)], radius=24, fill=(16, 22, 34, 240), outline=ACCENT_TEAL, width=3)

    # Speaker Tag Pill
    active_name = "EMMA (Host)" if is_emma else "ANDREW (Host)"
    draw.rounded_rectangle([(140, 650), (450, 705)], radius=12, fill=ACCENT_TEAL)
    f_spk = load_font(26, bold=True)
    draw.text((295, 677), f"🎙️ {active_name}", fill=(10, 20, 30), font=f_spk, anchor="mm")

    # Sentence & Spoken Word Highlighting
    raw_text = turn["text"]
    words_clean = [re.sub(r'[\*\*\.]', '', w).strip() for w in raw_text.split() if w.strip()]
    if not words_clean:
        words_clean = ["Listen", "carefully"]

    active_word_idx = min(len(words_clean) - 1, int((sub_idx / max(1, total_subframes)) * len(words_clean)))

    f_sub = load_font(42, bold=True)
    rendered_words = raw_text.split()

    line_words = []
    lines = []
    max_w = 1600
    curr_w = 0

    for w_i, w in enumerate(rendered_words):
        clean_w = re.sub(r'\*\*(.*?)\*\*', r'\1', w)
        wb = draw.textbbox((0, 0), clean_w + " ", font=f_sub)
        w_len = wb[2] - wb[0]
        if curr_w + w_len > max_w and line_words:
            lines.append(line_words)
            line_words = [(w_i, w, clean_w, w_len)]
            curr_w = w_len
        else:
            line_words.append((w_i, w, clean_w, w_len))
            curr_w += w_len
    if line_words:
        lines.append(line_words)

    y_start = 740 if len(lines) == 1 else 725
    line_h = 55
    for l_idx, line in enumerate(lines[:2]):
        total_line_w = sum(item[3] for item in line)
        start_x = 960 - total_line_w // 2
        curr_x = start_x
        y_pos = y_start + l_idx * line_h

        for (w_i, raw_w, clean_w, w_len) in line:
            is_active_word = (w_i == active_word_idx)
            is_key_word = ("**" in raw_w)

            if is_active_word:
                # Emerald Green active karaoke pill
                draw.rounded_rectangle([(curr_x - 4, y_pos - 6), (curr_x + w_len - 2, y_pos + 46)], radius=8, fill=FIX_GREEN)
                draw.text((curr_x, y_pos), clean_w, fill=(10, 20, 16), font=f_sub)
            elif is_key_word:
                draw.text((curr_x, y_pos), clean_w, fill=GOLD_ACCENT, font=f_sub)
            else:
                draw.text((curr_x, y_pos), clean_w, fill=WHITE, font=f_sub)
            curr_x += w_len

    # Tip Ribbon inside the Lower Third
    f_tip = load_font(22, bold=False)
    draw.text((960, 885), "💡 Clinical Tip: Say the correct phrase aloud 3 times immediately to rewire your muscle memory!", fill=MUTED_TEXT, font=f_tip, anchor="mm")

    # Bottom Progress Deck
    draw.line([(0, 1020), (VIDEO_WIDTH, 1020)], fill=(32, 45, 65), width=3)
    ratio = min(1.0, elapsed / max(1.0, total_dur))
    draw.line([(0, 1020), (int(VIDEO_WIDTH * ratio), 1020)], fill=FIX_GREEN, width=6)

    f_bot = load_font(24, bold=False)
    draw.text((70, 1050), "Mistakes Clinic • Native Pronunciation & Grammar • Stop Sounding Unnatural", fill=MUTED_TEXT, font=f_bot, anchor="lm")
    time_str = f"{int(elapsed // 60):02d}:{int(elapsed % 60):02d} / {int(total_dur // 60):02d}:{int(total_dur % 60):02d}"
    draw.text((1850, 1050), time_str, fill=FIX_GREEN, font=f_bot, anchor="rm")

    canvas.convert("RGB").save(out_path, quality=90)

def assemble_video(topic_item, turns, audio_list, run_dir):
    frames_dir = run_dir / "frames"
    clips_dir = run_dir / "clips"
    frames_dir.mkdir(parents=True, exist_ok=True)
    clips_dir.mkdir(parents=True, exist_ok=True)

    total_dur = sum(a["duration"] for a in audio_list)
    elapsed = 0.0
    clips = []

    for i, (turn, audio) in enumerate(zip(turns, audio_list)):
        dur = audio["duration"]
        subframes_count = max(8, int(dur * SUBFRAMES_PER_SEC))

        turn_frames_dir = frames_dir / f"turn_{i:03d}"
        turn_frames_dir.mkdir(parents=True, exist_ok=True)

        for s_idx in range(subframes_count):
            frame_p = turn_frames_dir / f"frame_{s_idx:04d}.png"
            sub_elapsed = elapsed + (s_idx / subframes_count) * dur
            render_podcast_subframe(
                topic_item, turn, i, s_idx, subframes_count,
                sub_elapsed, total_dur, str(frame_p)
            )

        clip_p = clips_dir / f"clip_{i:03d}.mp4"
        input_pattern = str(turn_frames_dir / "frame_%04d.png")

        cmd = [
            "ffmpeg", "-y",
            "-framerate", str(SUBFRAMES_PER_SEC),
            "-i", input_pattern,
            "-i", audio["path"],
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            "-preset", "veryfast",
            str(clip_p)
        ]
        subprocess.run(cmd, check=True, capture_output=True)

        clips.append(clip_p)
        elapsed += dur

    concat_txt = run_dir / "concat.txt"
    with open(concat_txt, "w") as f:
        for c in clips:
            f.write(f"file '{c.resolve().as_posix()}'\n")

    final_video = run_dir / "common_mistakes_podcast_final.mp4"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(final_video)], check=True, capture_output=True)
    return final_video, total_dur

async def run_mistakes_generation(topic_idx=0, turns_count=4):
    topic_item = TOPICS[topic_idx % len(TOPICS)]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = OUTPUT_DIR / f"run_{ts}"
    run_dir.mkdir(parents=True, exist_ok=True)

    print(f"[Mistakes Podcast] Generating 16:9 Linguistics Lab: '{topic_item['wrong']}' vs '{topic_item['right']}' ({turns_count} turns)...")
    turns = generate_script_ai(topic_item, target_turns=turns_count)
    audio_list = await generate_audio_files(turns, run_dir)
    video_p, dur = assemble_video(topic_item, turns, audio_list, run_dir)

    meta = {
        "title": f"Fix Common English Mistake: Stop Saying '{topic_item['wrong']}' 🎙️ Slow English Podcast",
        "description": f"Stop saying '{topic_item['wrong']}'! Learn the natural native alternative '{topic_item['right']}' with Emma & Andrew! ⚠️✅",
        "mistake": topic_item["wrong"],
        "duration_seconds": dur
    }
    with open(run_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"[Mistakes Podcast] Video ready: {video_p}")
    return video_p, meta

if __name__ == "__main__":
    asyncio.run(run_mistakes_generation(topic_idx=0, turns_count=2))
