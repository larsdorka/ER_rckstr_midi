import pygame
import os


class DisplayRenderer:
    """class to render generated number to the screen"""

    def __init__(self, debug_log=dict()):
        """constructor
        :param debug_log: dictionary to write log entries into
        """
        self.debug_log = debug_log
        self.debug_log['display'] = ""
        self.full_screen = False
        self.render_zero = False
        self.display_buffer = None
        self.big_font = None
        self.medium_font = None
        self.small_font = None
        self.display_width = 0
        self.display_height = 0

    def open(self, full_screen=False, render_zero=False):
        """initializes the screen and render objects
        :param full_screen: True to use full screen, False to use window
        :param render_zero: True to render the number 0, False to render blank on 0
        """
        self.full_screen = full_screen
        self.render_zero = render_zero
        if self.full_screen:
            self.display_buffer = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.display_buffer = pygame.display.set_mode((1024, 768))
        self.display_width = self.display_buffer.get_width()
        self.display_height = self.display_buffer.get_height()
        self.big_font = pygame.font.Font('freesansbold.ttf', self.display_height // 5)
        self.medium_font = pygame.font.Font('freesansbold.ttf', self.display_height // 10)
        self.small_font = pygame.font.Font('freesansbold.ttf', 11)
        self.display_buffer.fill((0, 0, 0))

    def render_state(self):
        """renders connection and error messages as debug information"""
        display_text = self.small_font.render(self.debug_log['midi'], True, (255, 255, 255), (0, 0, 0))
        display_rect = display_text.get_rect()
        self.display_buffer.blit(display_text, display_rect)
        display_text = self.small_font.render("midi device connected: " + self.debug_log['midi_connected'], True,
                                              (255, 255, 255), (0, 0, 0))
        display_rect = display_text.get_rect()
        display_rect = display_rect.move(0, 11)
        self.display_buffer.blit(display_text, display_rect)
        display_text = self.small_font.render(self.debug_log['config_chord'], True, (255, 255, 255), (0, 0, 0))
        display_rect = display_text.get_rect()
        display_rect = display_rect.move(0, 22)
        self.display_buffer.blit(display_text, display_rect)
        display_text = self.small_font.render(self.debug_log['midi_message'], True, (255, 255, 255), (0, 0, 0))
        display_rect = display_text.get_rect()
        display_rect = display_rect.move(0, 33)
        self.display_buffer.blit(display_text, display_rect)
        display_text = self.small_font.render(self.debug_log['config'], True, (255, 255, 255), (0, 0, 0))
        display_rect = display_text.get_rect()
        display_rect = display_rect.move(0, 44)
        self.display_buffer.blit(display_text, display_rect)
        display_text = self.small_font.render(self.debug_log['display'], True, (255, 255, 255), (0, 0, 0))
        display_rect = display_text.get_rect()
        display_rect = display_rect.move(0, 55)
        self.display_buffer.blit(display_text, display_rect)

    def render_menu(self, menu_page=list()):
        """renders a single menu screen
        :param menu_page: the menu screen to render as a list of strings
        """
        for line in range(len(menu_page)):
            display_text = self.small_font.render(menu_page[line], True, (255, 255, 255), (0, 0, 0))
            display_rect = display_text.get_rect()
            display_rect = display_rect.move(0, 11 * line)
            self.display_buffer.blit(display_text, display_rect)

    def render_number(self, number, color=(255, 255, 255)):
        """renders a number in a large font in the center of the screen
        :param number: the number to render
        :param color: the color to render the number with
        """
        if number != 0 or self.render_zero is True:
            display_text = self.big_font.render(str(number).zfill(5), True, color, (0, 0, 0))
            display_rect = display_text.get_rect()
            display_rect.center = (self.display_width // 2, self.display_height // 2)
            self.display_buffer.blit(display_text, display_rect)

    def render_note_name(self, note_name, color=(255, 255, 255)):
        """renders a note name string in a medium font above the center of the screen
        :param note_name: the note name to render
        :param color: the color to render the note name with
        """
        render_string = ""
        if note_name == "INVALID":
            render_string = "FAAAAALSCH"
        elif note_name == "CORRECT":
            render_string = "GEWONNEN!"
        elif note_name != "":
            render_string = "Dies ist ein " + note_name
        if render_string != "":
            display_text = self.medium_font.render(render_string, True, color, (0, 0, 0))
            display_rect = display_text.get_rect()
            display_rect.center = (self.display_width // 2, self.display_height // 2)
            display_rect = display_rect.move(0, -150)
            self.display_buffer.blit(display_text, display_rect)

    def render_note_image(self, note_name, color=(255, 255, 255)):
        """renders an image below the center of the screen depending on the given note name
        :param note_name: the name of the note to determine the file name
        :param color: the color to render the image in (alpha channel)
        """
        if note_name != "" and note_name != "INVALID" and note_name != "CORRECT":
            display_image = None
            filepath = "data/" + note_name + ".PNG"
            try:
                display_image = pygame.image.load(os.path.normpath(filepath))
            except Exception as ex:
                self.debug_log['display'] = "error opening image " + filepath + ": " + str(ex)
            if display_image is not None:
                display_rect = display_image.get_rect()
                display_rect.center = (self.display_width // 2, self.display_height // 2)
                display_rect = display_rect.move(0, 200)
                display_image.set_alpha(color[0])
                self.display_buffer.blit(display_image, display_rect)

    def update(self):
        """updates the screen with the current buffer and clears the buffer"""
        pygame.display.update()
        self.display_buffer.fill((0, 0, 0))
