import sys
import time

import pygame
from pygame.locals import *

from modules import *

MENU_STRUCTURE = [
    ["main menu",
     "",
     "1 - select midi input device: {}",
     "2 - display fullscreen: {}",
     "3 - show debug info: {}",
     "S - save configuration",
     "",
     "P - small group: {}",
     "R - reset game state",
     "X - exit application",
     "",
     "space - close menu"],
    ["select midi input device",
     "",
     "",
     "space - back to main menu"],
]


def terminate():
    """terminate the program"""
    midi.close()
    pygame.quit()
    sys.exit()


def check_for_input():
    """process termination request"""
    result = ""
    for _ in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            result = "menu"
        elif event.key == K_SPACE:
            result = "menu"
        elif event.key == K_x:
            result = "X"
        elif event.key == K_s:
            result = "S"
        elif event.key == K_r:
            result = "R"
        elif event.key == K_p:
            result = "P"
        elif event.key == K_1:
            result = "1"
        elif event.key == K_2:
            result = "2"
        elif event.key == K_3:
            result = "3"
        elif event.key == K_4:
            result = "4"
        elif event.key == K_5:
            result = "5"
        elif event.key == K_6:
            result = "6"
        elif event.key == K_7:
            result = "7"
        elif event.key == K_8:
            result = "8"
        elif event.key == K_9:
            result = "9"
    return result


def format_main_menu(config):
    menu = list()
    menu.append(MENU_STRUCTURE[0][0])
    menu.append(MENU_STRUCTURE[0][1])
    menu.append(MENU_STRUCTURE[0][2].format(str(config.get_config('MIDI_DEVICE_ID'))))
    menu.append(MENU_STRUCTURE[0][3].format(str(config.get_config('FULL_SCREEN'))))
    menu.append(MENU_STRUCTURE[0][4].format(str(config.get_config('SHOW_DEBUG'))))
    menu.append(MENU_STRUCTURE[0][5])
    menu.append(MENU_STRUCTURE[0][6])
    menu.append(MENU_STRUCTURE[0][7].format(str(config.get_config('SMALL_GROUP'))))
    menu.append(MENU_STRUCTURE[0][8])
    menu.append(MENU_STRUCTURE[0][9])
    menu.append(MENU_STRUCTURE[0][10])
    menu.append(MENU_STRUCTURE[0][11])
    return menu


def format_midi_menu(device_list):
    menu = list()
    menu.append(MENU_STRUCTURE[1][0])
    menu.append(MENU_STRUCTURE[1][1])
    for index in range(len(device_list)):
        if device_list[index][2] == 1:
            menu.append(str(index) + " - " + str(device_list[index][1]))
    menu.append(MENU_STRUCTURE[1][2])
    menu.append(MENU_STRUCTURE[1][3])
    return menu


# main application
if __name__ == '__main__':

    # initialization
    pygame.init()
    debug_log = dict()
    config = configuration.Configuration(debug_log)
    config.load("config.json")
    display = displayRenderer.DisplayRenderer(debug_log)
    fullscreen = config.get_config('FULL_SCREEN')
    show_debug = config.get_config('SHOW_DEBUG')
    chord = config.get_config('CHORD')
    show_menu = False
    menu_select = 0
    menu_page = format_main_menu(config)
    display.open(config.get_config('FULL_SCREEN'))
    midi = midiInput.MidiInput(debug_log)
    midi.open(config.get_config('MIDI_DEVICE_ID'))
    codeGen = codeGenerator.CodeGenerator()
    dio = inputReader.InputReader(debug_log)
    dio.setup_pins(player_switch=29)
    outlets = switchRequestor.SwitchRequestor(debug_log)
    outlets.open(url=config.get_config('OUTLET_URL'), password=config.get_config('OUTLET_PW'))
    outlets.login()
    # state variables
    login_timer = time.time()
    send_timer = time.time()
    success = False
    number = 0
    note_name = ""
    color = None

    # application loop
    while True:
        time.sleep(0.1)
        input_value = check_for_input()

        # menu handling
        if not show_menu:
            if input_value == "menu":
                input_value = ""
                menu_select = 0
                show_menu = True
                menu_page = format_main_menu(config)
        if show_menu:
            if menu_select == 0:
                if input_value == "menu":
                    show_menu = False
                elif input_value == "1":
                    menu_select = 1
                    menu_page = format_midi_menu(midi.midi_device_list)
                elif input_value == "2":
                    config.set_config('FULL_SCREEN', not config.get_config('FULL_SCREEN'))
                    display.open(config.get_config('FULL_SCREEN'))
                    menu_page = format_main_menu(config)
                elif input_value == "3":
                    config.set_config('SHOW_DEBUG', not config.get_config('SHOW_DEBUG'))
                    menu_page = format_main_menu(config)
                elif input_value == "P":
                    config.set_config('SMALL_GROUP', not config.get_config('SMALL_GROUP'))
                    menu_page = format_main_menu(config)
                elif input_value == "R":
                    success = False
                elif input_value == "S":
                    config.save()
                elif input_value == "X":
                    outlets.logout()
                    terminate()
            elif menu_select == 1:
                if input_value == "menu":
                    menu_select = 0
                    menu_page = format_main_menu(config)
                elif input_value in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    index = int(input_value)
                    if midi.midi_device_list[index][2] == 1:
                        config.set_config('MIDI_DEVICE_ID', index)
                        midi.open(index)
            display.render_menu(menu_page)
        elif config.get_config('SHOW_DEBUG'):
            debug_log['midi_connected'] = str(midi.connected)
            display.render_state()

        if time.time() - login_timer > 60:
            login_timer = time.time()
            outlets.login()

        # midi data handling
        # if not (not dio.state_player_switch and success):
        if not (config.get_config('SMALL_GROUP') and success):
            if midi.connected:
                midi.read_data()
            note_name = codeGen.calc_note_name(midi.get_flat_midi_data(), config.get_config('CHORD'))
            success = codeGen.verify_chord(midi.get_flat_midi_data(), config.get_config('CHORD'))
            if note_name == "CORRECT":
                number = config.get_config('LOCK_CODE')
                outlets.switch_on(1, prepare=True)
            else:
                number = 0
                outlets.switch_off(1, prepare=True)
            # color = codeGen.calc_color(midi.midi_data)
            color = 255, 255, 255
            display.render_number(number, color)
            display.render_note_name(note_name, color)
            display.render_note_image(note_name, color)
        else:
            display.render_number(number, color)
            display.render_note_name(note_name, color)

        # render display and send outlets
        display.update()
        if outlets.prepared:
            if time.time() - send_timer > 1:
                send_timer = time.time()
                outlets.send_switches()
