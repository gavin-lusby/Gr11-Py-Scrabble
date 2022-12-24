import string

from PIL import ImageTk, Image

TileImage = {}
ModifierImage = {"tw": ImageTk.PhotoImage((Image.open("Tile Modifiers/TW.png")).resize((48, 48), Image.ANTIALIAS)),
                 "dw": ImageTk.PhotoImage((Image.open("Tile Modifiers/DW.png")).resize((48, 48), Image.ANTIALIAS)),
                 "tl": ImageTk.PhotoImage((Image.open("Tile Modifiers/TL.png")).resize((48, 48), Image.ANTIALIAS)),
                 "dl": ImageTk.PhotoImage((Image.open("Tile Modifiers/DL.png")).resize((48, 48), Image.ANTIALIAS)),
                 "center": ImageTk.PhotoImage(
                     (Image.open("Tile Modifiers/CENTER.png")).resize((48, 48), Image.ANTIALIAS)),
                 "default": ImageTk.PhotoImage(
                     (Image.open("Tile Modifiers/default.png")).resize((48, 48), Image.ANTIALIAS))}


SwapImage = ImageTk.PhotoImage((Image.open("Letter Tiles/SWAP_tile.png")).resize((120, 120), Image.ANTIALIAS))


def MakeLetter(letter, size):
    if size == "small":
        return ImageTk.PhotoImage(
            (Image.open("Letter Tiles/" + letter.upper() + "_tile.png")).resize((48, 48), Image.ANTIALIAS))
    elif size == "medium":
        return ImageTk.PhotoImage(
            (Image.open("Letter Tiles/" + letter.upper() + "_tile.png")).resize((120, 120), Image.ANTIALIAS))
    elif size == "large":
        return ImageTk.PhotoImage(
            (Image.open("Letter Tiles/" + letter.upper() + "_tile.png")).resize((400, 400), Image.ANTIALIAS))


for size in ["small", "medium", "large"]:
    TileImage[size] = {}
    for letter in string.ascii_lowercase:
        TileImage[size][letter] = MakeLetter(letter, size)
    TileImage[size]["blank"] = MakeLetter("blank", size)
