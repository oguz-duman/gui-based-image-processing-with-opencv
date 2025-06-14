import json, os, sys

# Determine the correct path for the palette file
if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

palette_path = os.path.join(base_path, "dark_palette.json")

# Load palette from JSON
with open(palette_path, "r") as f:
    PALETTE_COLORS = json.load(f)

COMBO_ITEM_HOVER = "#383938"
COMBO_BACKGROUND = PALETTE_COLORS["Button"]     # Color from the palette is used to ensure consistency
COMBO_HOVER = "#8c8d8d"
COMBO_SELECTED = "#0078d7"