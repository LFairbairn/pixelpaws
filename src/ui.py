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

# Random stretching (REQ-SM-009): fires a real Cat.trigger_stretch() state
# transition rather than a cosmetic-only animation swap.
STRETCH_MIN_DELAY_MS = 10000
STRETCH_MAX_DELAY_MS = 20000


class GameWindow:
    def __init__(self, root: tk.Tk, cat: Cat):
        self.root = root
        self.cat = cat
        self._job: str | None = None
        self._tick_job: str | None = None
        self._stretch_job: str | None = None
        self._last_state = None
        self._frames: list[tuple[ImageTk.PhotoImage, int]] = []
        self._frame_index = 0
        self._wandering = False
        self._wander_photos: list[tuple[ImageTk.PhotoImage, int]] = []
        # Bumped exactly once per real state change (_sync_animation) or
        # wander interruption. Every scheduled callback that ends up
        # touching the canvas — the normal per-state frame loop, a wander
        # leg, a deferred stretch retry — captures the generation active
        # when it was scheduled and checks it before acting. after_cancel()
        # cancels the *next* scheduled step, but a step Tcl has already
        # dispatched can still run its Python callback after a cancellation
        # lands; without this guard, an old chain (e.g. the idle loop) can
        # be silently orphaned and keep firing forever, fighting whatever
        # legitimately owns the canvas afterwards — this is what caused the
        # "stand/sit" flicker during wandering.
        self._gen = 0

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
        self._gen += 1
        self._cancel_job()
        self._cancel_stretch_schedule()
        if self._wandering:
            self._wandering = False
            self.canvas.coords(self.sprite, CENTER, CENTER)
        self._load_animation()
        if self.cat.state is CatState.IDLE:
            self._schedule_wander()
            self._schedule_stretch()

    def _load_animation(self) -> None:
        token = self._gen
        raw_frames = load_frames(self.cat.current_animation.name)
        self._frames = [
            (ImageTk.PhotoImage(image), duration) for image, duration in raw_frames
        ]
        self._frame_index = 0
        self._advance_frame(token)

    def _advance_frame(self, token: int) -> None:
        if token != self._gen:
            return
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

        self._job = self.root.after(duration, lambda: self._advance_frame(token))

    def _schedule_tick(self) -> None:
        self.cat.tick(TICK_INTERVAL_MS / 1000)
        self._sync_animation()
        self._tick_job = self.root.after(TICK_INTERVAL_MS, self._schedule_tick)

    # --- idle wandering ---
    #
    # Every callback in this chain takes the generation token active when
    # it was scheduled and checks it against self._gen before touching the
    # sprite — see the note by self._gen's declaration for why.

    def _schedule_wander(self) -> None:
        token = self._gen
        delay = random.randint(WANDER_MIN_DELAY_MS, WANDER_MAX_DELAY_MS)
        self._job = self.root.after(delay, lambda: self._start_wander(token))

    def _start_wander(self, token: int) -> None:
        if token != self._gen:
            return
        # Starting a wander doesn't change cat.state, so _sync_animation()
        # never runs and never bumps the generation on its own — bump it
        # here instead, right as canvas ownership passes from the idle
        # loop to the wander. Without this, the idle loop's own scheduled
        # callback (captured with the *old*, still-current-until-now token)
        # keeps passing its guard and firing throughout the whole wander,
        # fighting it for the canvas — this was the actual cause of the
        # "stand/sit" flicker.
        self._gen += 1
        token = self._gen
        self._wandering = True
        direction = random.choice((-1, 1))
        animation = "walking_left" if direction < 0 else "walking_right"
        self._play_wander_leg(
            animation, direction * WANDER_DISTANCE_PX, self._pause, token
        )

    def _pause(self, token: int) -> None:
        if token != self._gen:
            return
        self._play_wander_leg("stand_idle", 0, self._walk_back, token)

    def _walk_back(self, token: int) -> None:
        if token != self._gen:
            return
        x, _ = self.canvas.coords(self.sprite)
        animation = "walking_left" if x > CENTER else "walking_right"
        self._play_wander_leg(animation, CENTER - x, self._finish_wander, token)

    def _finish_wander(self, token: int) -> None:
        if token != self._gen:
            return
        self.canvas.coords(self.sprite, CENTER, CENTER)
        self._wandering = False
        self._load_animation()
        self._schedule_wander()

    def _play_wander_leg(
        self, animation_name: str, total_dx: float, on_done, token: int
    ) -> None:
        if token != self._gen:
            return
        raw_frames = load_frames(animation_name)
        photos = [
            (ImageTk.PhotoImage(image), duration) for image, duration in raw_frames
        ]
        # Keep a strong reference on self, not just the local variable —
        # PhotoImage deletes its underlying Tk image the instant its last
        # Python reference is dropped, even if a canvas item is still
        # displaying it by name. Without this, `photos` goes out of scope
        # the moment the last frame's on_done() is scheduled (it isn't
        # passed forward, since the next leg uses a different animation),
        # and the sprite goes blank for the gap until the next leg starts.
        self._wander_photos = photos
        step = total_dx / len(photos)
        self._advance_wander_frame(photos, 0, step, on_done, token)

    def _advance_wander_frame(self, photos, index, step, on_done, token: int) -> None:
        if token != self._gen:
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

    def _cancel_job(self) -> None:
        if self._job is not None:
            self.root.after_cancel(self._job)
            self._job = None

    # --- random stretching ---
    #
    # Deliberately *not* generation-guarded, unlike everything above: this
    # never touches the canvas directly, and both trigger_stretch() and
    # _sync_animation() are already safe no-ops if the state has moved on
    # since this was scheduled. A generation check here would be actively
    # wrong — _start_wander() bumps the generation on every wander, which
    # would wrongly invalidate a stretch check scheduled before that wander
    # began, breaking "stretch resumes once the wander finishes".

    def _schedule_stretch(self) -> None:
        delay = random.randint(STRETCH_MIN_DELAY_MS, STRETCH_MAX_DELAY_MS)
        self._stretch_job = self.root.after(delay, self._maybe_stretch)

    def _maybe_stretch(self) -> None:
        self._stretch_job = None
        if self._wandering:
            # Don't cut into a walk — check again shortly once it's done,
            # rather than firing mid-stride or waiting a full random cycle.
            self._stretch_job = self.root.after(500, self._maybe_stretch)
            return
        self.cat.trigger_stretch()
        self._sync_animation()

    def _cancel_stretch_schedule(self) -> None:
        if self._stretch_job is not None:
            self.root.after_cancel(self._stretch_job)
            self._stretch_job = None

    def _on_close(self) -> None:
        for job in (self._job, self._tick_job, self._stretch_job):
            if job is not None:
                self.root.after_cancel(job)
        self.root.destroy()
