import random
import tkinter as tk

from PIL import ImageTk

from src.cat import Cat
from src.cat_state import CatState
from src.sprite_loader import SCALED_SPRITE_SIZE, load_frames

TICK_INTERVAL_MS = 1000

# The canvas is bigger than the sprite itself — the sprite renders at its
# normal scaled size (see REQ-NFR-002), just centred in more surrounding
# space so the window has more visual presence.
CANVAS_SIZE = SCALED_SPRITE_SIZE * 2
CENTER = CANVAS_SIZE // 2

# Idle wandering (REQ-ANIM-011): purely cosmetic, never touches Cat/CatState
# — stat depletion is identical whether the cat is wandering or standing
# still. Only ever runs while cat.state is IDLE.
WANDER_MIN_DELAY_MS = 8000
WANDER_MAX_DELAY_MS = 15000
WANDER_DISTANCE_PX = 50


class GameWindow:
    def __init__(self, root: tk.Tk, cat: Cat):
        self.root = root
        self.cat = cat
        # Whichever timer is currently driving the canvas — the normal
        # per-state animation loop, or a step of the wander sequence.
        # Only one of those ever runs at a time.
        self._job: str | None = None
        self._tick_job: str | None = None
        self._last_state = None
        self._frames: list[tuple[ImageTk.PhotoImage, int]] = []
        self._frame_index = 0
        self._wandering = False
        # Incremented on every cancellation so in-flight wander callbacks
        # scheduled before it can recognise they're stale and no-op instead
        # of mutating the sprite after a newer state has taken over —
        # after_cancel() alone isn't reliable against this race.
        self._wander_token = 0

        root.title("PixelPaws")
        root.protocol("WM_DELETE_WINDOW", self._on_close)

        self.name_label = tk.Label(root, text=cat.name, font=("Helvetica", 20, "bold"))
        self.name_label.pack(pady=(10, 0))

        self.canvas = tk.Canvas(
            root, width=CANVAS_SIZE, height=CANVAS_SIZE, highlightthickness=0
        )
        self.canvas.pack(pady=10)
        self.sprite = self.canvas.create_image(CENTER, CENTER)

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
        self._end_wander_if_active()
        self._load_animation()
        if self.cat.state is CatState.IDLE:
            self._schedule_wander()

    def _load_animation(self) -> None:
        self._cancel_job()
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

        self._job = self.root.after(duration, self._advance_frame)

    def _schedule_tick(self) -> None:
        self.cat.tick(TICK_INTERVAL_MS / 1000)
        self._sync_animation()
        self._tick_job = self.root.after(TICK_INTERVAL_MS, self._schedule_tick)

    # --- idle wandering ---
    #
    # Every callback in this chain takes the generation token that was
    # active when it was scheduled and checks it against the current one
    # before touching the sprite. after_cancel() cancels the *next*
    # scheduled step, but a step already dispatched by Tcl can still run
    # its Python callback after a cancellation lands — the token guard
    # makes stale callbacks true no-ops instead of a sprite that jumps
    # after being "reset".

    def _schedule_wander(self) -> None:
        token = self._wander_token
        delay = random.randint(WANDER_MIN_DELAY_MS, WANDER_MAX_DELAY_MS)
        self._job = self.root.after(delay, lambda: self._start_wander(token))

    def _start_wander(self, token: int) -> None:
        if token != self._wander_token:
            return
        self._wandering = True
        direction = random.choice((-1, 1))
        animation = "walking_left" if direction < 0 else "walking_right"
        self._play_wander_leg(
            animation, direction * WANDER_DISTANCE_PX, self._pause, token
        )

    def _pause(self, token: int) -> None:
        if token != self._wander_token:
            return
        self._play_wander_leg("stand_idle", 0, self._walk_back, token)

    def _walk_back(self, token: int) -> None:
        if token != self._wander_token:
            return
        x, _ = self.canvas.coords(self.sprite)
        animation = "walking_left" if x > CENTER else "walking_right"
        self._play_wander_leg(animation, CENTER - x, self._finish_wander, token)

    def _finish_wander(self, token: int) -> None:
        if token != self._wander_token:
            return
        self.canvas.coords(self.sprite, CENTER, CENTER)
        self._wandering = False
        self._load_animation()
        self._schedule_wander()

    def _play_wander_leg(
        self, animation_name: str, total_dx: float, on_done, token: int
    ) -> None:
        if token != self._wander_token:
            return
        raw_frames = load_frames(animation_name)
        photos = [
            (ImageTk.PhotoImage(image), duration) for image, duration in raw_frames
        ]
        step = total_dx / len(photos)
        self._advance_wander_frame(photos, 0, step, on_done, token)

    def _advance_wander_frame(self, photos, index, step, on_done, token: int) -> None:
        if token != self._wander_token:
            return
        photo, duration = photos[index]
        self.canvas.itemconfig(self.sprite, image=photo)
        x, y = self.canvas.coords(self.sprite)
        self.canvas.coords(self.sprite, x + step, y)

        index += 1
        if index >= len(photos):
            self._job = self.root.after(duration, lambda: on_done(token))
        else:
            self._job = self.root.after(
                duration,
                lambda: self._advance_wander_frame(photos, index, step, on_done, token),
            )

    def _end_wander_if_active(self) -> None:
        self._cancel_job()
        self._wander_token += 1
        if self._wandering:
            self._wandering = False
            self.canvas.coords(self.sprite, CENTER, CENTER)

    def _cancel_job(self) -> None:
        if self._job is not None:
            self.root.after_cancel(self._job)
            self._job = None

    def _on_close(self) -> None:
        for job in (self._job, self._tick_job):
            if job is not None:
                self.root.after_cancel(job)
        self.root.destroy()
