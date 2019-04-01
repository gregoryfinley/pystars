# stars_etc.py is just unused code cut from stars.py

"""
Docstring
"""

from collections import namedtuple
import itertools
import random
import math
from sys import float_info

from colortemp import temperature_to_rgb
import libtcodpy as tcod

"""
All coordinates for modeling the solar system will be in heliocentric ecliptic 
coordinates.

'Heliocentric ecliptic coordinates. The origin is the center of the Sun. The 
fundamental plane is the plane of the ecliptic. The primary direction (the x 
axis) is the vernal equinox. A right-handed convention specifies a y axis 90
degrees to the east in the fundamental plane; the z axis points toward the 
north ecliptic pole. The reference frame is relatively stationary, aligned 
with the vernal equinox.'

Reference:
https://en.wikipedia.org/wiki/Ecliptic_coordinate_system#/media/File:Heliocentric_rectangular_ecliptic.png
"""

# Class factory for SphericalCoordinates tuple type
SphericalCoordinates = namedtuple('SphericalCoordinates',['radial','azimuthal','polar'],False,False)
EuclideanCoordinates = namedtuple('EuclideanCoordinates',['x','y','z'],False,False)

def spherical_to_euclidean(spherical):
    x = spherical.radial * math.sin(spherical.polar) * math.cos(spherical.azimuthal)
    y = spherical.radial * math.sin(spherical.polar) * math.sin(spherical.azimuthal)
    z = spherical.radial * math.cos(spherical.polar)
    return EuclideanCoordinates(x,y,z)

# TODO(Greg): check correctness, atan2(y/x) vs (x/y)
def euclidean_to_spherical(euclidean):
    radial = math.sqrt(euclidean.x**2 + euclidean.y**2 + euclidean.z**2, 0.5)
    azimuthal = math.atan2(euclidean.y, euclidean.x)
    polar = math.asin(euclidean.z / radial)
    return SphericalCoordinates(radial, azimuthal, polar)

def eccentric_anomaly(M, e, tolerance=1e-12, max_iter=100):
    """
    Returns the eccentric anomaly as computed by the Newton-Raphson method.
    """
    E = M
    for i in range(max_iter):
        f = E - e * math.sin(E) - M
        fp = 1.0 - e * math.cos(E)
        if fp == 0: # TODO(Greg): handle this more correctly?
            E = -sys.float_info.max
        E = E - f / fp
        if abs(M - (E - e * math.sin(E))) <= tolerance:
            continue
    return E



class Planet(object):
    def __init__(self, name, sprite, color, semimajor_axis, eccentricity, inclination, ascending_node, perihelion, axial_tilt, mean_anomaly):
        """
        Construct a new planet object.
        
        Earth-like values from Wikipedia:
        axial_tilt = 23.4392811

        semimajor_axis = 1.00000102 AU
        eccentricity = 0.0167086
        inclination = 7.155 degrees
        ascending_node = 11.26064 degrees
        perihelion = 114.20783 degrees
        mean_anomaly = 358.617 degress

        Note: mean anomaly varies with time. The mean anomaly here is used to determine the time of perihelion passage. (Maybe?!)
        """
        self.name = name

        # TODO(Greg): extract these attributes so stars.py does not require libtcod
        self.sprite = sprite
        self.color = color
        
        self.semimajor_axis = semimajor_axis
        self.eccentricity = eccentricity
        self.inclination = inclination
        self.ascending_node = ascending_node
        self.perihelion = perihelion
        self.mean_anomaly = mean_anomaly # There must be a better way. The naming is very confusing.
      
        self.axial_tilt = axial_tilt

        # Period is derived from the semi-major axis, but can be faked if
        # needed by the game designer.
        self.period = math.sqrt(self.semimajor_axis**3.0)
        if not self.period == 0.0:
            self.period = 1.0
        
        # The time of perihelion passage is derived, but can be faked if
        # needed by the game designer.
        self.tp = -1.0 * self.mean_anomaly * self.period / (2.0 * math.pi)

    def get_position(self, t):
        """Get the planet's heliocentric equatorial coordinates at time t."""
        e = self.eccentricity
        a = self.semimajor_axis # semi-major axis of orbiting body (AU)
        O = math.radians(self.ascending_node) # longitude of ascending node
        w = math.radians(self.perihelion) # longitude of perihelion
        i = math.radians(self.inclination) # angle between plane of Sun's equator and the planet's orbit

        # mean anomaly at t
        M = 2.0 * math.pi * (t - self.tp) / self.period

        # eccentric anomaly
        E = eccentric_anomaly(M, e)

        # true anomaly
        v = 2.0 * math.atan(math.sqrt((1.0 + e) / (1.0 - e)) * math.tan(E / 2.0))

        # radial distance
        r = a * (1.0 - e**2) / (1.0 + e * math.cos(v))

        # convert polar coordinates (r,v) to Euclidiean heliocentric ecliptic coordinates (x,y,z)
        x = r * (math.cos(O) * math.cos(w + v) - math.sin(O) * math.sin(w + v) * math.cos(i))
        y = r * (math.sin(O) * math.cos(w + v) + math.cos(O) * math.sin(w + v) * math.cos(i))
        z = r * math.sin(w + v) * math.sin(i)

        # rotate the coordinates into heliocentric equatorial coordinates (X,Y,Z)
        X = x
        Y = y * math.cos(i) - z * math.sin(i)
        Z = y * math.sin(i) + z * math.cos(i)

        return (X, Y, Z)

class Star(object):
    new_id = itertools.count().next

    def __init__(self, coordinate):
        self.id = Star.new_id()
        self.coordinate = coordinate

        # Make this mess better...
        self.brightness = pow(self.radial, 3.0)
        if self.brightness < 0.0016: # 7
            self.sprite = chr(8)
            self.apmag = 0
            print self
        elif self.brightness < 0.004: # 13
            self.sprite = chr(9)
            self.apmag = 1
        elif self.brightness < 0.01: # 25
            self.sprite = chr(10)
            self.apmag = 2
        elif self.brightness < 0.0251: # 50
            self.sprite = chr(11)
            self.apmag = 3
        elif self.brightness < 0.0631: # 100
            self.sprite = chr(12)
            self.apmag = 4
        elif self.brightness < 0.158: # 200
            self.sprite = chr(13)
            self.apmag = 5
        elif self.brightness < 0.398:
            self.sprite = chr(14)
            self.apgmag = 6
        else:
            self.sprite = chr(15)
            self.apmag = 7

    @property
    def radial(self):
        """Get the radial distance."""
        return self.coordinate.radial

    @property
    def azimuthal(self):
        """Get the azimuthal angle in radians."""
        return self.coordinate.azimuthal

    @property
    def polar(self):
        """Get the polar angle in radians."""
        return self.coordinate.polar

    @property
    def x(self):
        """Get the unit sphere x position."""
        return self.position.x
    
    @property
    def y(self):
        """Get the unit sphere y position."""
        self.position.y

    @property
    def z(self):
        """Get the unit sphere z position."""
        self.position.z

    def __str__(self):
        return 'id: {id}, coord: ({radial:.3f}, {azimuthal:.3f}, {polar:.3f})'.format(id=self.id, radial=self.radial, azimuthal=self.azimuthal, polar=self.polar)

def orthodromic_distance(coordinate1, coordinate2):
    """
    Returns the orthodromic distance between two spherical coordinates on a unit sphere.

    Should work with both Star and SphericalCoordinates types.
    Ignores radial distances.
    """
    return math.acos(math.sin(coordinate1.polar) * math.sin(coordinate2.polar) + math.cos(coordinate1.polar) * math.cos(coordinate2.polar) * math.cos(coordinate1.azimuthal - coordinate2.azimuthal))

def get_random_spherical_coordinate():
    """
    Returns a randomized spherical coordinate such that multiple coordinates
    generated in this way should be evenly distributed within a ball.
    Coordinates are intended for use as equatorial coordinates.

    Radial distance is normalized from [0,1]
    Azimuthal angle interval is [0,2pi)
    Polar angle interval is [0,pi)

    Note: polar angle interval excludes pi because of the implementation of
    Python's random.uniform() and random.random() functions. But radial distance
    will often output 1.0 because of floating point rounding errors after pow()

    References:
    http://mathworld.wolfram.com/SpherePointPicking.html
    https://en.wikipedia.org/wiki/Equatorial_coordinate_system
    """
    radial = pow(random.random(), 1.0/3.0)
    azimuthal = 2.0 * math.pi * random.random()
    polar = math.acos(random.uniform(-1.0, 1.0))
    return SphericalCoordinates(radial, azimuthal, polar)

EuclideanCoordinates = namedtuple('EuclideanCoordinates', ['x', 'y', 'z'], False, False)

def generate_edges(stars, limit=math.pi/4.0):
    """
    Returns a list of weighted edges between all Star() objects in a given list.
    
    The orthodromic distance between stars is used for their edge weights.

    Edges are stored as follows: [(node,node,weight),(node,node,weight),...]
    """
    edges = []
    length = len(stars)
    for i in range(length):
        for j in range(i+1,length):
            weight = orthodromic_distance(stars[i], stars[j])
            if weight <= limit:
                edges.append((stars[i].id, stars[j].id,weight))
    return edges

def generate_arcs(stars, limit=math.pi/4.0):
    """
    Returns a dictionary of weighted arcs betweens all Star() objects in a given list.
    
    The orthodromic distance between stars is used for their arc weights.

    Arcs are stored as follows: {source: [(destination,weight), (destination,weight)], ...}
    """
    graph = []
    length = len(stars)
    for src in range(length):
        arcs = []
        for dest in range(length):
            weight = orthodromic_distance(stars[src], stars[dest])
            if src != dest and weight <= limit:
                arcs.append((stars[dest].id, weight))
        graph.append((stars[src].id, arcs))
    return dict(graph)

# libtcod utilities

def get_cylindrical_projection(stars, width=360, height=180):
    """
    Return a tcod console instance of width and height that renders an equirectangular projection of the given list of stars.
    """
    console = tcod.console_new(width, height)

    for star in stars:
        azimuthal = int((star.azimuthal * width) / (2 * math.pi))
        polar = int((star.polar / math.pi) * height)

        # Color Work
        rgb = temperature_to_rgb(random.uniform(4000,20000))
        brightness = 1.0 - star.radial * 0.75
        
        color = tcod.Color(rgb[0], rgb[1], rgb[2])
        (h,s,v) = tcod.color_get_hsv(color)
        tcod.color_set_hsv(color,h,s,brightness)

        tcod.console_put_char_ex(console, azimuthal, polar, star.sprite, color, tcod.black)
    
    # Background Texture
    noise3d = tcod.noise_new(3)
    for map_x in range(width):
        for map_y in range(height):
            azimuthal = (map_x / (width * 1.0)) * 2.0 * math.pi
            polar = (map_y / (height * 1.0)) * math.pi
            x = math.sin(polar) * math.cos(azimuthal)
            y = math.sin(polar) * math.sin(azimuthal)
            z = math.cos(polar)
            blue = int(tcod.noise_get_turbulence(noise3d,[x,y,z],32.0) * 16.0 + 16.0)
            green = int(tcod.noise_get(noise3d,[x,y,z]) * 8.0 + 8.0)
            red = int(tcod.noise_get_fbm(noise3d,[x,y,z],32.0) * 4.0 + 4.0)
            background = tcod.Color(red,green,blue)

            if map_y == height/2 or map_x == 0 or map_x == width/2:
                background = tcod.darkest_yellow

            tcod.console_set_char_background(console,map_x,map_y,background)

    tcod.noise_delete(noise3d)
    return console





@property
def x(self):
    """Get the unit sphere x position."""
    return self.position.x

@property
def y(self):
    """Get the unit sphere y position."""
    return self.position.y

@property
def z(self):
    """Get the unit sphere z position."""
    return self.position.z