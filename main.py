import pygame
import sys
import math
import pygame.gfxdraw
import numpy as np #MAKES IT SLOWER!!!
import time
import cProfile
import os

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *

# models
print("Importing models.... (Might take a while)")
from total_modles.model import MODLES
from total_modles.custom_model import BOB
from total_modles.random_gen import generate_model_after
print("DONE!")
# models

# My imports
import camera
from objects import threeDModles
import main_functions_math
import main_loop
import core_vars


def main():
    main_loop.main_loop()

if __name__ == "__main__":
    #cProfile.run("main()")
    main()

# DO THIS IF YOU GET ERRORS ABOUT OPENGL
# pip install PyOpenGL PyOpenGL_accelerate 