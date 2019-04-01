# !!!!!!! this file is a dumping ground for old (possibly broken) code; it probably won't do anything right

# m-by-n matrix (rows x cols) as a list comprehension:
# [[0 for col in range(n)] for row in range(m)]


def rotate(x, y, z, phi, theta, psi):
    a11 = math.cos(psi) * math.cos(phi) - math.cos(theta) * math.sin(phi) * math.sin(psi)
    a12 = -math.sin(psi) * math.cos(phi) - math.cos(theta) * math.sin(phi) * math.cos(psi)
    a13 = math.sin(theta) * math.sin(phi)
    a21 = math.cos(psi) * math.sin(phi) + math.cos(theta) * math.cos(phi) * math.sin(psi)
    a22 = -math.sin(psi) * math.sin(phi) + math.cos(theta) * math.cos(phi) * math.cos(psi)
    a23 = -math.sin(theta) * math.cos(phi)
    a31 = math.sin(psi) * math.sin(theta)
    a32 = math.cos(psi) * math.sin(theta)
    a33 = math.cos(theta)
    x = x * a11 + y * a12 + z * a13
    y = x * a21 + y * a22 + z * a23
    z = x * a31 + y * a32 + z * a33
    return x, y, z


def rotate_x(x, y, z, angle):
    y2 = y * math.cos(angle) - z * math.sin(angle)
    z2 = y * math.sin(angle) + z * math.cos(angle)
    return x, y2, z2


def rotate_z(x, y, z, angle):
    x2 = x * math.cos(angle) - y * math.sin(angle)
    y2 = x * math.sin(angle) + y * math.cos(angle)
    return x2, y2, z


x, y, z = rotate_z(x0, y0, z0, self.arg_peri)
x, y, z = rotate_x(x, y, z, self.inclination)
X, Y, Z = rotate_z(x, y, z, self.ascending_node)

        #BAK
        
        # z rotation - ascending node
        x1 = x0 * math.cos(self.ascending_node) - y0 * math.sin(self.ascending_node)
        y1 = x0 * math.sin(self.ascending_node) + y0 * math.cos(self.ascending_node)
        z1 = z0

        # x rotation - inclination
        x2 = x1
        y2 = y1 * math.cos(self.inclination) - z1 * math.sin(self.inclination)
        z2 = y1 * math.sin(self.inclination) + z1 * math.cos(self.inclination)

        # z rotation - argument of periapsis
        x3 = x2 * math.cos(self.arg_peri) - y2 * math.sin(self.arg_peri)
        y3 = x2 * math.sin(self.arg_peri) + y2 * math.cos(self.arg_peri)
        z3 = z2


        x0 = r * math.cos(v)
        y0 = r * math.sin(v)
        z0 = 0.0

        # z rotation - ascending node
        x1 = r * math.cos(self.ascending_node + v)
        y1 = r * math.sin(self.ascending_node + v)
        z1 = 0.0

        # x rotation - inclination
        x2 = r * math.cos(self.ascending_node + v)
        y2 = r * math.sin(self.ascending_node + v) * math.cos(self.inclination)
        z2 = r * math.sin(self.ascending_node + v) * math.sin(self.inclination)

        # z rotation - argument of periapsis
        x3 = r * math.cos(self.ascending_node + v) * math.cos(self.arg_peri) - r * math.sin(self.ascending_node + v) * math.cos(self.inclination) * math.sin(self.arg_peri)
        y3 = r * math.cos(self.ascending_node + v) * math.sin(self.arg_peri) + r * math.sin(self.ascending_node + v) * math.cos(self.inclination) * math.cos(self.arg_peri)
        z3 = r * math.sin(self.ascending_node + v) * math.sin(self.inclination)


# test code
stars = generate_stars(1000)
edges = generate_edges(stars)
sorted_edges = sorted(edges,key=lambda edge: edge[2])
for edge in sorted_edges:
    if edge[2] > (2.0/3.0) * math.pi:
        print str(stars[edge[0]])
        print str(stars[edge[1]])
        print '({i},{j}),{weight:.3f}\n'.format(i=edge[0], j=edge[1], weight=edge[2])


    console = tcod.console_new(width, height)
    tcod.console_set_default_background(console, tcod.black)
    tcod.console_clear(console)
    for star in stars:
        azimuthal = int((star.azimuthal * width) / (2 * math.pi))
        polar = int((star.polar * height) / math.pi)
        magnitude = int(star.radial * 255.0)
        color = tcod.Color(magnitude, magnitude, magnitude)
        tcod.console_put_char_ex(console, azimuthal, polar, '*', color, tcod.black)
    return console




########
######## begin old pystars.py
########
import tcod
import stars

# Module Constants
LIMIT_FPS = 20

# actual size of the window
SCREEN_WIDTH = 150
SCREEN_HEIGHT = 70

# size of the map
WORLD_WIDTH = 360
WORLD_HEIGHT = 180

class Window(object):
    """
    Maintains state for a GUI window.
    Includes:
        position
        size
        contents
        draw()
    """

    def __init__(self, x, y, w, h, visible=False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.visible = visible
        self.console = tcod.console_new(self.w, self.h)
        self.contents = ["1. Hello.", "2. World."]
        tcod.console_set_default_background(self.console, tcod.black)
        tcod.console_set_default_foreground(self.console, tcod.white)
        self.selection = 0

    def draw(self, target_console):
        """Updates and blits the windows's console buffer to another console."""
        tcod.console_print_frame(self.console, 0, 0, self.w, self.h, True, tcod.BKGND_DEFAULT)
        for index in range (len(self.contents)):
            tcod.console_print(self.console, 3, index+2, self.contents[index])
        tcod.console_put_char_ex(self.console, 2, self.selection+2, '>', tcod.white, tcod.black)
        tcod.console_blit(self.console, 0, 0, self.w, self.h, target_console, self.x, self.y, 1.0, 0.9)

class World(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.console = tcod.console_new(self.width, self.height)
        self.elevation = tcod.heightmap_new(self.width, self.height)
        self.map = tcod.map_new(self.width, self.height)
        
        # put some interesting values into elevation
        noise = tcod.noise_new(2,tcod.NOISE_DEFAULT_HURST, tcod.NOISE_DEFAULT_LACUNARITY, 0)
        for x in range (0, self.width):
            for y in range (0, self.height):
                k = 3.4
                value = tcod.noise_get(noise,[x/k,y/k], tcod.NOISE_PERLIN)
                tcod.heightmap_set_value(self.elevation, x, y, value)
        tcod.noise_delete(noise)

        self.update()
    
    def update(self):
        """Update the world's console buffer with current map data."""
        for x in range (0, self.width):
            for y in range (0, self.height):
                cell_value = tcod.heightmap_get_value(self.elevation, x, y)
                cell_value = int(cell_value * 127) + 127
                tcod.map_set_properties(self.map, x, y, (cell_value < 150), (cell_value < 150 and cell_value > 75))
                if not tcod.map_is_transparent(self.map, x, y):
                    cell_color = tcod.white
                elif not tcod.map_is_walkable(self.map, x, y):
                    cell_color = tcod.blue
                else:
                    cell_color = tcod.black
                tcod.console_set_char_background(self.console, x, y, cell_color)
        
def run():
    # INIT

    # libtcod
    tcod.console_set_custom_font('pystars12x12.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_ASCII_INROW, 16, 48)
    tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'PyStars')
    tcod.sys_set_fps(LIMIT_FPS)
    key = tcod.Key()
    mouse = tcod.Mouse()

    # game data
    world = World(WORLD_WIDTH, WORLD_HEIGHT)

    # screen setup
    viewport = Window(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, True)
    action_menu = Window(0, 0, 30, 30)
    camera = {'x':0, 'y':0}

    starmap = stars.generate_stars(1602)
    projection = stars.get_cylindrical_projection(starmap)

    brightest = min(starmap, key=lambda star: star.radial)
    print brightest

    # GAME LOOP
    while tcod.console_is_window_closed() is False:
        # DRAWING
        #world.update()
        #tcod.console_blit(world.console, camera['x'], camera['y'], WORLD_WIDTH, WORLD_HEIGHT, None, 0, 0)
        # tcod.console_blit(projection, camera['x'], camera['y'], WORLD_WIDTH, WORLD_HEIGHT, None, 0, 0)
        tcod.console_flush()
        
        # USER INPUT
        while tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS|tcod.EVENT_MOUSE,key,mouse) > 0:
            if key.vk == tcod.KEY_UP:
                camera['y'] -= 1
            if key.vk == tcod.KEY_DOWN:
                camera['y'] += 1
            if key.vk == tcod.KEY_LEFT:
                camera['x'] -= 1
            if key.vk == tcod.KEY_RIGHT:
                camera['x'] += 1
            camera['x'] = max(0, min(camera['x'], WORLD_WIDTH-SCREEN_WIDTH))
            camera['y'] = max(0, min(camera['y'], WORLD_HEIGHT-SCREEN_HEIGHT))

        # GAME LOGIC
########
######## end old pystars.py
########