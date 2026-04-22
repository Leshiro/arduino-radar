# imports
import pygame
import serial
import math

# local imports
from setup.config import *
from setup.visuals import *

# initial data
angle = INITIAL_ANGLE
distance = INITIAL_DISTANCE

# pygame start
pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption(WINDOW_TITLE)
clock = pygame.time.Clock() 
 
# start connection
ser = serial.Serial(PORT, BAUD, timeout=1)