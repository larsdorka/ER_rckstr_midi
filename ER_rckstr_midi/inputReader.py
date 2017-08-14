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
        self.input_channel = 29
        self.input_state = False
        self.output_channel = 11

    def setup_pins(self):
        """"""
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.output_channel, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.input_channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.input_channel, GPIO.BOTH, callback=self.input_edge_callback, bouncetime=100)

    def input_edge_callback(self, pin):
        """callback to handle detected input edges
        :param pin: the number of the physical pin with detected edge
        """
        self.input_state = GPIO.input(pin) == GPIO.HIGH
        if self.input_state is True:
            GPIO.output(self.output_channel, GPIO.HIGH)
        elif self.input_state is False:
            GPIO.output(self.output_channel, GPIO.LOW)
