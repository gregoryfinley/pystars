#!/usr/bin/env python
#coding=utf-8

import math
import time

import tcod

import orbit
import stars

SCREEN_WIDTH = 90
SCREEN_HEIGHT = 45
FPS_LIMIT = 30
FIXED_STEP = 1.0 / FPS_LIMIT
DAYS_PER_YEAR = 365.2422
OBLIQUITY = math.radians(23.43928)

class GameData():
    quit = False
    running = True
    top = False
    time = 0.0
    time_scale = 30.0

    def __init__(self):
        # TODO: load the scene from a file
        self.stars = stars.generate_stars(500)
        self.stars.sort(key=lambda star: star.radial, reverse=True)
        self.orbits = {}
        self.orbits['Mercury'] = orbit.Orbit(0.205630, 0.387098, 7.005, 48.331, 29.124, 174.796, degrees=True)
        self.orbits['Venus'] = orbit.Orbit(0.006772, 0.723332, 3.39458, 76.68, 54.884, 50.115, degrees=True)
        self.orbits['Earth'] = orbit.Orbit(0.0167086, 1.00000102, 0.00005, -11.26064, 114.20783, 358.617, degrees=True)
        self.orbits['Mars'] = orbit.Orbit(0.0934, 1.523679, 1.850, 49.558, 286.502, 19.373, degrees=True)
        self.orbits['Ceres'] = orbit.Orbit(0.075823, 2.7675, 10.593, 80.3293, 72.5220, 95.9891, degrees=True)
        self.orbits['Jupiter'] = orbit.Orbit(0.048498, 5.2026, 1.303, 100.464, 273.867, 20.020, degrees=True)
        self.orbits['Saturn'] = orbit.Orbit(0.05555, 9.5549, 2.48524, 113.665, 339.392, 317.02, degrees=True)
        self.orbits['Uranus'] = orbit.Orbit(0.046, 19.2184, 0.773, 74.006, 96.998857, 142.2386, degrees=True)
        self.orbits['Neptune'] = orbit.Orbit(0.009456, 30.110387, 1.767975, 131.784, 276.336, 256.228, degrees=True)
        self.orbits['Pluto'] = orbit.Orbit(0.2488, 39.48, 17.16, 110.299, 113.834, 14.53, degrees=True)
        self.orbits['Eris'] = orbit.Orbit(0.44068, 67.781, 44.0445, 35.9531, 150.977, 204.16, degrees=True)
        self.planet_colors = {}
        self.planet_colors['Mercury'] = tcod.light_gray
        self.planet_colors['Venus'] = tcod.lightest_yellow
        self.planet_colors['Earth'] = tcod.blue
        self.planet_colors['Mars'] = tcod.red
        self.planet_colors['Ceres'] = tcod.gray
        self.planet_colors['Jupiter'] = tcod.lighter_sepia
        self.planet_colors['Saturn'] = tcod.light_amber
        self.planet_colors['Uranus'] = tcod.cyan
        self.planet_colors['Neptune'] = tcod.dark_azure
        self.planet_colors['Pluto'] = tcod.brass
        self.planet_colors['Eris'] = tcod.lightest_gray
        self.planet_symbols = {}
        self.planet_symbols['Mercury'] = chr(10)
        self.planet_symbols['Venus'] = chr(9)
        self.planet_symbols['Earth'] = chr(9)
        self.planet_symbols['Mars'] = chr(10)
        self.planet_symbols['Ceres'] = chr(15)
        self.planet_symbols['Jupiter'] = chr(9)
        self.planet_symbols['Saturn'] = chr(10)
        self.planet_symbols['Uranus'] = chr(11)
        self.planet_symbols['Neptune'] = chr(11)
        self.planet_symbols['Pluto'] = chr(13)
        self.planet_symbols['Eris'] = chr(13)

        #unused
        self.camera_x = 0.0
        self.camera_y = 0.0
        self.camera_z = 0.0
        self.camera_rot_z = 0.0
        self.camera_rot_x = 0.0
        self.camera_sensitivity = 1.0 / 12.0

def update(game, dt):
    if game.running:
        game.time = game.time + game.time_scale * dt
    #game.camera_x, game.camera_y, game.camera_z = game.orbits['Earth'].position(game.time / DAYS_PER_YEAR)


def draw(game, console):
    if game.top:
        draw_top(game, console)
    else:
        draw_side(game, console)

def draw_top(game, console):
    console.clear()

    center_y = SCREEN_HEIGHT / 2.0 + 0.5
    center_x = SCREEN_WIDTH / 2.0 + 0.5

    for name, body in game.orbits.items():
        planet_x, planet_y, planet_z = body.position(game.time / DAYS_PER_YEAR)
        planet_x = planet_x * 4.0
        planet_y = planet_y * 4.0
        planet_z = planet_z * 4.0
        tcod.console_put_char_ex(console, int(center_x + planet_x), int(center_y - planet_y), game.planet_symbols[name], game.planet_colors[name], tcod.black)

    # Draw Sun
    # TODO: refactor this so the sun isn't special
    tcod.console_put_char_ex(console, int(center_x), int(center_y), chr(42), tcod.yellow, tcod.black)

    info = 'Day: {t:.2f} @ {ts:.2f} d/s'.format(t = game.time, ts = game.time_scale)
    console.print(0, SCREEN_HEIGHT-1, info, fg=tcod.constants.white, bg=tcod.constants.black)

def draw_side(game, console):
    console.clear()

    # TODO: fix and use background texture code from stars_etc.py

    # Draw stars
    for star in game.stars:
        x = SCREEN_WIDTH * (0.5 - star.right_ascension / 360.0) % SCREEN_WIDTH
        y = SCREEN_HEIGHT * (0.5 - star.declination / 180.0)
        apmag = int(math.floor(1.0 - star.radial * 256))
        tcod.console_put_char_ex(console, int(x), int(y), chr(15), tcod.Color(apmag, apmag, apmag), tcod.black)

    # Draw orbiting bodies
    earth_xecl, earth_yecl, earth_zecl = game.orbits['Earth'].position(game.time / DAYS_PER_YEAR)
    earth_xeq = earth_xecl
    earth_yeq = earth_yecl * math.cos(OBLIQUITY) + earth_zecl * math.sin(OBLIQUITY)
    earth_zeq = -earth_yecl * math.sin(OBLIQUITY) + earth_zecl * math.cos(OBLIQUITY)

    for name, body in game.orbits.items():
        if name == 'Earth':
            continue
        xecl, yecl, zecl = body.position(game.time / DAYS_PER_YEAR)
        xeq = xecl - earth_xecl
        yeq = (yecl - earth_yecl) * math.cos(OBLIQUITY) + (zecl - earth_zecl) * math.sin(OBLIQUITY)
        zeq = -(yecl - earth_yecl) * math.sin(OBLIQUITY) + (zecl - earth_zecl) * math.cos(OBLIQUITY)
        screen_x = math.floor(SCREEN_WIDTH * (0.5 - orbit.right_ascension(xeq, yeq) / 360.0) % SCREEN_WIDTH)
        screen_y = math.floor(SCREEN_HEIGHT * (0.5 - orbit.declination(xeq, yeq, zeq) / 180.0))
        tcod.console_put_char_ex(console, int(screen_x), int(screen_y), game.planet_symbols[name], game.planet_colors[name], tcod.black)

    # Draw sun
    # TODO: refactor this so the sun isn't special
    xecl, yecl, zecl = 0, 0, 0
    xeq = xecl - earth_xecl
    yeq = (yecl - earth_yecl) * math.cos(OBLIQUITY) + (zecl - earth_zecl) * math.sin(OBLIQUITY)
    zeq = -(yecl - earth_yecl) * math.sin(OBLIQUITY) + (zecl - earth_zecl) * math.cos(OBLIQUITY)
    screen_x = math.floor(SCREEN_WIDTH * (0.5 - orbit.right_ascension(xeq, yeq) / 360.0) % SCREEN_WIDTH)
    screen_y = math.floor(SCREEN_HEIGHT * (0.5 - orbit.declination(xeq, yeq, zeq) / 180.0))
    tcod.console_put_char_ex(console, int(screen_x), int(screen_y), chr(42), tcod.yellow, tcod.black)

    # TODO: Earth's moon
    # TODO: camera stuff
    # info = 'Day: {t:.2f} @ {ts:.2f} d/s; Camera: ({x:.3f}, {z:.3f})\n'.format(t = game.time, ts = game.time_scale, x=game.camera_rot_x, z=game.camera_rot_z)
    info = 'Day: {t:.2f} @ {ts:.2f} d/s)'.format(t = game.time, ts = game.time_scale)
    console.print(0, SCREEN_HEIGHT-1, info, fg=tcod.constants.white, bg=tcod.constants.black)


def run():
    # TODO: create own font and stop using URR's
    tcod.console_set_custom_font('urr12x12.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_ASCII_INROW, 16, 48)
    root_console = tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'PyStars Test', renderer=2)
    tcod.sys_set_fps(FPS_LIMIT)
    key = tcod.Key()
    mouse = tcod.Mouse()
    game = GameData()
    tcod.console_flush()
    dt = 0.0
    while tcod.console_is_window_closed() == 0:
        dt += tcod.sys_get_last_frame_length()
        while tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse) > 0:
            if key.vk == tcod.KEY_SPACE:
                game.time = 0.0
                game.time_scale = 360.0
            elif key.vk == tcod.KEY_TAB:
                game.top = not game.top
            elif key.vk == tcod.KEY_PAUSE:
                game.running = not game.running
            elif key.vk == tcod.KEY_UP:
                game.time_scale = game.time_scale + 30
            elif key.vk == tcod.KEY_DOWN:
                game.time_scale = game.time_scale - 30
            if mouse.rbutton:
                game.camera_rot_x -= math.radians(mouse.dx * game.camera_sensitivity)
                game.camera_rot_z -= math.radians(mouse.dy * game.camera_sensitivity)
        while dt >= FIXED_STEP:
            update(game, FIXED_STEP)
            dt = dt - FIXED_STEP
        draw(game, root_console)
        tcod.console_flush()
        time.sleep(0.001)
