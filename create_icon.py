from pathlib import Path

from PIL import Image, ImageDraw


icon = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
draw = ImageDraw.Draw(icon)
draw.rounded_rectangle((12, 12, 244, 244), radius=52, fill="#0F766E")
draw.rounded_rectangle((53, 69, 204, 187), radius=20, outline="white", width=16)
draw.rounded_rectangle((204, 103, 232, 153), radius=8, fill="white")
draw.rounded_rectangle((73, 89, 143, 167), radius=10, fill="white")
icon.save(
    Path(__file__).with_name("battery_alert.ico"),
    format="ICO",
    sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
)
