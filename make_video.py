# make_video.py
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, AudioFileClip
from gtts import gTTS
from config import VIDEO_DIR, VIDEO_WIDTH, VIDEO_HEIGHT, DURATION_SECONDS, THUMB_DIR
from pathlib import Path
import textwrap, time
from PIL import Image, ImageDraw

def _create_bg(path, w=VIDEO_WIDTH, h=VIDEO_HEIGHT):
    img = Image.new("RGB", (w, h), "#12121f")
    draw = ImageDraw.Draw(img)
    for i in range(h):
        r = int(18 + (i / h) * 60)
        g = int(18 + (i / h) * 20)
        b = int(31 + (i / h) * 90)
        draw.line([(0, i), (w, i)], fill=(r, g, b))
    img.save(path)


def _save_tts(text, out_mp3):
    tts = gTTS(text=text, lang="en")
    tts.save(out_mp3)


def make_video_from_quote(quote_text, filename_prefix="short"):
    stamp = int(time.time())
    video_filename = f"{filename_prefix}_{stamp}.mp4"
    video_path = str(Path(VIDEO_DIR) / video_filename)

    bg_path = str(Path(VIDEO_DIR) / f"bg_{stamp}.jpg")
    _create_bg(bg_path)

    audio_path = str(Path(VIDEO_DIR) / f"tts_{stamp}.mp3")
    _save_tts(quote_text, audio_path)

    wrapped = "\n".join(textwrap.wrap(quote_text, width=20))
    txtclip = TextClip(wrapped, fontsize=72, font='Amiri-Bold', align='Center', method='label')
    txtclip = txtclip.set_position('center').set_duration(DURATION_SECONDS)

    bg_clip = ImageClip(bg_path).set_duration(DURATION_SECONDS).resize((VIDEO_WIDTH, VIDEO_HEIGHT))
    audio_clip = AudioFileClip(audio_path)

    final = CompositeVideoClip([bg_clip, txtclip]).set_audio(audio_clip)
    final.write_videofile(video_path, fps=24, codec="libx264", audio_codec="aac", verbose=False, logger=None)

    thumb_path = str(Path(THUMB_DIR) / f"thumb_{stamp}.jpg")
    bg = Image.open(bg_path).resize((1280, 720))
    draw = ImageDraw.Draw(bg)
    draw.text((40, 40), quote_text[:80], fill=(255, 255, 255))
    bg.save(thumb_path, quality=85)

    return video_path, thumb_path
