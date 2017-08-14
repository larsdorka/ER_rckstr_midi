import platform

if platform.system() == "Windows":
    import gpioMockup as GPIO
else:
    import RPi.GPIO as GPIO


class InputReader:
    """"""

    def __init__(self, debug_log=dict()):
        """"""
        self.debug_log = debug_log
        self.input_player_switch = 0
        self.state_player_switch = False
        # self.output_channel = 11

    def setup_pins(self, player_switch=29):
        """"""
        self.input_player_switch = player_switch
        GPIO.setmode(GPIO.BOARD)
        # GPIO.setup(self.output_channel, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.input_player_switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.input_player_switch, GPIO.BOTH, callback=self.input_edge_callback, bouncetime=100)

    def input_edge_callback(self, pin):
        """callback to handle detected input edges
        :param pin: the number of the physical pin with detected edge
        """
        if pin == self.input_player_switch:
            self.state_player_switch = GPIO.input(pin) == GPIO.HIGH
