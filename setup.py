import sys
from cx_Freeze import setup, Executable

includefiles = ["classes.py","coin.png","greencheck.png","highscores.txt","Intro.png","kanin1.png","kanin2.png","kanin2.png","kanin3.png","kanin4.png","lock.png","planet1.png","planet2.png","planet3.png","planet4.png","planet5.png","Purchases.txt","shop.png","space.jpg"]
includes = []


setup(
    name='FlyRabit',
    options = {"build.exe" : {"packages" : ["pygame", "random","time" ], 'includes':includes,'include_files':includefiles}},
    version='1.0',
    author = "Sjur Brekke Espedal",
    executables = [Executable("FlyRabbit.py")])
