import json

# Load the color palette from a JSON file 
with open("dark_palette.json", "r") as f:
    PALETTE_COLORS = json.load(f)


COMBO_ITEM_HOVER = "#383938"
COMBO_BACKGROUND = PALETTE_COLORS["Button"]     # Color from the palette is used to ensure consistency
COMBO_HOVER = "#8c8d8d"
COMBO_SELECTED = "#0078d7"