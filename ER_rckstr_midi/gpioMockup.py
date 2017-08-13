"""mockup file for RPi.GPIO to develop on windows without Raspberry Pi I/O hardware"""

BOARD = 0
OUT = 0
IN = 0
LOW = 0
HIGH = 0
BOTH = 0
PUD_DOWN = 0


def setmode(mode):
    pass


def setup(channel, direction, initial=0, pull_up_down=0):
    pass


def add_event_detect(channel, state, callback=0, bouncetime=0):
    pass


def input(channel):
    return LOW


def output(channel, state):
    pass


def cleanup(channel):
    pass
