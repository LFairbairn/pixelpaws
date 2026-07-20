from pathlib import Path

from PIL import Image, ImageSequence

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

NATIVE_SPRITE_SIZE = 32

# REQ-NFR-002: scale 32x32 pixel art 3-4x with nearest-neighbour resampling
# so it renders crisply rather than blurred.
SCALE = 4
SCALED_SPRITE_SIZE = NATIVE_SPRITE_SIZE * SCALE


def load_frames(animation_name: str) -> list[tuple[Image.Image, int]]:
    """Load a GIF's frames, scaled up with nearest-neighbour resampling.

    Returns a list of (frame_image, duration_ms) tuples in playback order.
    """
    path = ASSETS_DIR / f"{animation_name}.gif"
    im = Image.open(path)
    frames = []
    for frame in ImageSequence.Iterator(im):
        frame = frame.convert("RGBA")
        scaled = frame.resize(
            (frame.width * SCALE, frame.height * SCALE), Image.Resampling.NEAREST
        )
        duration = frame.info.get("duration", 100)
        frames.append((scaled, duration))
    return frames
