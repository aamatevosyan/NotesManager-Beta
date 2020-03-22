import pathlib
from enum import Enum

from PyQt5.QtGui import QIcon


class CategoryColor(Enum):
    AquamarineBlue = "AquamarineBlue"
    Black = "Black"
    Candlelight = "Candlelight"
    CatskillWhite = "CatskillWhite"
    ChaletGreen = "ChaletGreen"
    ChateauGreen = "ChateauGreen"
    ChelseaCucumber = "ChelseaCucumber"
    Cinnabar = "Cinnabar"
    Coral = "Coral"
    ElSalva = "ElSalva"
    Froly = "Froly"
    Heather = "Heather"
    MediumPurple = "MediumPurple"
    PinkSalmon = "PinkSalmon"
    Rajah = "Rajah"
    RoyalBlue = "RoyalBlue"
    SilverChalice = "SilverChalice"
    Squirrel = "Squirrel"
    SwissCoffee = "SwissCoffee"
    Victoria = "Victoria"

    def get_icon(self) -> QIcon:
        colors_path = pathlib.Path("notes/core/icons/colors")
        filename = pathlib.Path.joinpath(colors_path, self.name + ".png")

        return QIcon(str(filename))
