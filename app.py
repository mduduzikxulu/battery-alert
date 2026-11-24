"""
Battery Alert - modern, always-on-top, non-blocking pop-ups.
Requires: pip install -r requirements.txt
Run:      pythonw app.py
Preview:  python app.py --test
"""
import argparse
import tkinter as tk
import psutil
import pystray
from PIL import Image, ImageDraw

try:
    import winsound
except ImportError:
    winsound = None

# ---- Settings ----------------------------------------------------------
LOW_LEVELS = [20, 15, 10]    # alerts while on battery
HIGH_LEVELS = [80, 90]       # alerts while charging
CHECK_EVERY_SECONDS = 5
# ------------------------------------------------------------------------

# What each level says: (title, headline, explanation, accent colour)
LOW_MESSAGES = {
    20: ("Battery getting low", "Time to plug in",
         "Draining below 20% puts extra strain on the battery. "
         "Charging now keeps it healthy for longer.",
         "#B7791F"),
    15: ("Battery low", "Please plug in soon",
         "Deep discharges wear the cell faster. "
         "Plug in now to avoid dropping into the danger zone.",
         "#C05621"),
    10: ("Battery critical", "Plug in now",
         "Your laptop could shut down at any moment and unsaved work "
         "could be lost. Deep discharge also damages the battery.",
         "#B42318"),
}

HIGH_MESSAGES = {
    80: ("Battery at 80%", "You can unplug now",
         "80% is the sweet spot for battery health. Charging beyond it "
         "adds wear, and you already have plenty of power.",
         "#0F766E"),
    90: ("Battery at 90%", "Unplug to protect your battery",
         "Staying at a high charge adds heat and stress to the cell, "
         "which speeds up ageing. Unplugging now protects its lifespan.",
         "#0F766E"),
}

BG = "#FFFFFF"
FG = "#17212B"
MUTED = "#667085"
BORDER = "#E4E7EC"
HOVER = "#F2F4F7"

low_fired = set()
high_fired = set()

root = tk.Tk()
root.withdraw()


def beep(urgent):
    if winsound:
        try:
            winsound.MessageBeep(
                winsound.MB_ICONHAND if urgent else winsound.MB_ICONASTERISK
            )
        except Exception:
            pass


def show_popup(title, headline, detail, accent, pct):
    win = tk.Toplevel(root)
    win.overrideredirect(True)
    win.attributes("-topmost", True)
    win.configure(bg=BORDER)

    card = tk.Frame(win, bg=BG)
    card.pack(padx=1, pady=1, fill="both", expand=True)

    tk.Frame(card, bg=accent, width=4).pack(side="left", fill="y")

    body = tk.Frame(card, bg=BG)
    body.pack(side="left", fill="both", expand=True, padx=18, pady=15)

    header = tk.Frame(body, bg=BG)
    header.pack(fill="x")
    tk.Label(header, text=title, font=("Segoe UI", 9, "bold"),
             bg=BG, fg=MUTED).pack(side="left")
    close = tk.Label(header, text="×", font=("Segoe UI", 14),
                     bg=BG, fg=MUTED, cursor="hand2")
    close.pack(side="right")
    close.bind("<Button-1>", lambda e: win.destroy())
    close.bind("<Enter>", lambda e: close.config(fg=FG))
    close.bind("<Leave>", lambda e: close.config(fg=MUTED))

    row = tk.Frame(body, bg=BG)
    row.pack(fill="x", pady=(9, 6))
    tk.Label(row, text=f"{pct}%", font=("Segoe UI", 28, "bold"),
             bg=BG, fg=FG).pack(side="left")
    tk.Label(row, text=headline, font=("Segoe UI", 12, "bold"),
             bg=BG, fg=FG, wraplength=220, justify="left", anchor="w"
             ).pack(side="left", padx=(14, 0), fill="x", expand=True)

    tk.Label(body, text=detail, font=("Segoe UI", 9), bg=BG, fg=MUTED,
             wraplength=330, justify="left").pack(anchor="w", pady=(0, 9))

    btn = tk.Button(
        body,
        text="Dismiss",
        command=win.destroy,
        font=("Segoe UI", 9, "bold"),
        bg=BG,
        fg=accent,
        activebackground=HOVER,
        activeforeground=accent,
        relief="flat",
        bd=0,
        highlightthickness=0,
        cursor="hand2",
        padx=10,
        pady=5,
    )
    btn.pack(anchor="e")
    btn.bind("<Enter>", lambda e: btn.config(bg=HOVER))
    btn.bind("<Leave>", lambda e: btn.config(bg=BG))

    # Bottom-right corner, above the taskbar
    win.update_idletasks()
    w, h = win.winfo_width(), win.winfo_height()
    x = max(12, win.winfo_screenwidth() - w - 24)
    y = max(12, win.winfo_screenheight() - h - 70)
    win.geometry(f"+{x}+{y}")

    # Stay on top without stealing keyboard focus
    def keep_on_top():
        if win.winfo_exists():
            win.lift()
            win.attributes("-topmost", True)
            win.after(2000, keep_on_top)

    keep_on_top()


def check_battery():
    b = psutil.sensors_battery()
    if b is not None:
        pct = int(b.percent)

        for t in list(low_fired):
            if pct > t:
                low_fired.discard(t)
        for t in list(high_fired):
            if pct < t:
                high_fired.discard(t)

        if not b.power_plugged:
            due = [t for t in LOW_LEVELS if pct <= t and t not in low_fired]
            if due:
                low_fired.update(t for t in LOW_LEVELS if pct <= t)
                level = min(due)  # most urgent level crossed
                title, headline, detail, accent = LOW_MESSAGES.get(
                    level,
                    (
                        f"Battery low at {level}%",
                        "Please plug in soon",
                        f"You've reached your configured low-battery alert at {level}%.",
                        "#C05621",
                    ),
                )
                show_popup(title, headline, detail, accent, pct)
                beep(level <= 10)
        else:
            due = [t for t in HIGH_LEVELS if pct >= t and t not in high_fired]
            if due:
                high_fired.update(t for t in HIGH_LEVELS if pct >= t)
                level = max(due)
                title, headline, detail, accent = HIGH_MESSAGES.get(
                    level,
                    (
                        f"Battery at {level}%",
                        "You can unplug now",
                        f"You've reached your configured charge alert at {level}%.",
                        "#0F766E",
                    ),
                )
                show_popup(title, headline, detail, accent, pct)
                beep(False)

    root.after(CHECK_EVERY_SECONDS * 1000, check_battery)


def show_test_popup():
    show_popup(
        "Battery alert test",
        "This is a preview",
        "Your battery alert pop-ups are working.",
        "#0F766E",
        75,
    )


def exit_app(icon, item):
    def close():
        icon.stop()
        root.destroy()

    root.after(0, close)


def start_tray_icon():
    image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((9, 14, 50, 51), radius=7, fill="#FFFFFF")
    draw.rounded_rectangle((14, 20, 45, 45), radius=4, outline="#0F766E", width=4)
    draw.rectangle((46, 27, 54, 38), fill="#0F766E")
    draw.rounded_rectangle((19, 25, 30, 40), radius=2, fill="#0F766E")

    icon = pystray.Icon(
        "BatteryAlert",
        image,
        "Battery Alert",
        menu=pystray.Menu(
            pystray.MenuItem(
                "Test notification",
                lambda icon, item: root.after(0, show_test_popup),
            ),
            pystray.MenuItem("Exit", exit_app),
        ),
    )
    icon.run_detached()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Battery level alert pop-ups")
    parser.add_argument(
        "--test",
        action="store_true",
        help="show a sample pop-up without checking the battery",
    )
    args = parser.parse_args()

    if args.test:
        show_test_popup()
    else:
        check_battery()

    start_tray_icon()
    root.mainloop()