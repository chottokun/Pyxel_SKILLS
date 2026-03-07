# Screen Constants
SCREEN_WIDTH = 200
SCREEN_HEIGHT = 150
HUD_HEIGHT = 20

# Track Constants
TRACK_SIZE = 128  # 128x128 tiles
TILE_SIZE = 8

# TILES Definition
TILES = {
    "ROAD": (0, 0),
    "GRASS": (1, 0),
    "WALL": (2, 0),
    "BOOST": (3, 0),
    "START": (4, 0),
}

# Physics Constants
MAX_SPEED = 8.0
ACCELERATION = 0.12
DECELERATION = 0.05
FRICTION = 0.03
REV_SPEED = -2.0
TURN_SPEED = 4.5

# Camera Constants (Extreme Mode 7)
CAM_DIST_BASE = 32
CAM_HEIGHT_BASE = 20
PITCH_BASE = 75
FOV_BASE = 90

# Mini-map Constants
MMAP_X = 160
MMAP_Y = 5
MMAP_SIZE = 32
MMAP_SCALE = TRACK_SIZE / MMAP_SIZE # 128 / 32 = 4

# Game States
STATE_TITLE = 0
STATE_COUNTDOWN = 1
STATE_RACING = 2
STATE_GOAL = 3
