import tkinter as tk

from PIL import ImageTk

from src.cat import Cat
from src.sprite_loader import SCALED_SPRITE_SIZE, load_frames

TICK_INTERVAL_MS = 1000

# The canvas is bigger than the sprite itself — the sprite renders at its
# normal scaled size (see REQ-NFR-002), just centred in more surrounding
# space so the window has more visual presence.
CANVAS_SIZE = SCALED_SPRITE_SIZE * 2


class GameWindow:
    def __init__(self, root: tk.Tk, cat: Cat):
        self.root = root
        self.cat = cat
        self._animation_job: str | None = None
        self._tick_job: str | None = None
        self._last_state = None
        self._frames: list[tuple[ImageTk.PhotoImage, int]] = []
        self._frame_index = 0

        root.title("PixelPaws")
        root.protocol("WM_DELETE_WINDOW", self._on_close)

        self.name_label = tk.Label(root, text=cat.name, font=("Helvetica", 20, "bold"))
        self.name_label.pack(pady=(10, 0))

        self.canvas = tk.Canvas(
            root, width=CANVAS_SIZE, height=CANVAS_SIZE, highlightthickness=0
        )
        self.canvas.pack(pady=10)
        self.sprite = self.canvas.create_image(CANVAS_SIZE // 2, CANVAS_SIZE // 2)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=(0, 10))
        tk.Button(button_frame, text="🐟 Feed", state=tk.DISABLED).pack(
            side="left", padx=5
        )
        tk.Button(button_frame, text="🎾 Play", state=tk.DISABLED).pack(
            side="left", padx=5
        )
        tk.Button(button_frame, text="😴 Sleep", command=self._on_sleep_pressed).pack(
            side="left", padx=5
        )

        self._sync_animation()
        self._schedule_tick()

    def _on_sleep_pressed(self) -> None:
        self.cat.press_sleep()
        self._sync_animation()

    def _sync_animation(self) -> None:
        if self.cat.state == self._last_state:
            return
        self._last_state = self.cat.state
        if self._animation_job is not None:
            self.root.after_cancel(self._animation_job)
        raw_frames = load_frames(self.cat.current_animation.name)
        self._frames = [
            (ImageTk.PhotoImage(image), duration) for image, duration in raw_frames
        ]
        self._frame_index = 0
        self._advance_frame()

    def _advance_frame(self) -> None:
        photo, duration = self._frames[self._frame_index]
        self.canvas.itemconfig(self.sprite, image=photo)
        self._frame_index += 1

        if self._frame_index >= len(self._frames):
            if self.cat.current_animation.loop:
                self._frame_index = 0
            else:
                self.cat.on_animation_complete()
                self._sync_animation()
                return

        self._animation_job = self.root.after(duration, self._advance_frame)

    def _schedule_tick(self) -> None:
        self.cat.tick(TICK_INTERVAL_MS / 1000)
        self._sync_animation()
        self._tick_job = self.root.after(TICK_INTERVAL_MS, self._schedule_tick)

    def _on_close(self) -> None:
        for job in (self._animation_job, self._tick_job):
            if job is not None:
                self.root.after_cancel(job)
        self.root.destroy()
