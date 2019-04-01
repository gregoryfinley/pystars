from collections import namedtuple
import itertools
import random
import math


SphericalCoordinates = namedtuple('SphericalCoordinates', ['radial', 'azimuthal', 'polar'])


def generate_stars(n):
    """ Returns a list of n stars with randomized positions."""
    return [Star(get_random_spherical_coordinates()) for i in range(n)]

def get_random_spherical_coordinates():
    """
    Returns randomized spherical coordinates such that multiple coordinates
    generated in this way should be evenly distributed within a unit sphere.

    Radial distance is normalized from [0, 1]
    Azimuthal angle interval is [0, 2*pi)
    Polar angle interval is [-pi/2, pi/2)

    Note: polar angle interval excludes pi because of the implementation of
    Python's random.uniform() and random.random() functions. But radial distance
    can output 1.0 because of floating point rounding errors after pow()

    References:
    https://en.wikipedia.org/wiki/Equatorial_coordinate_system
    http://mathworld.wolfram.com/SpherePointPicking.html
    """
    radial = pow(random.random(), 1.0/3.0)
    azimuthal = random.random() * 2.0 * math.pi
    polar = math.acos(random.uniform(1.0, -1.0)) - math.pi / 2.0
    return SphericalCoordinates(radial, azimuthal, polar)


class Star():
    new_id = itertools.count()

    def __init__(self, coordinates):
        self.id = next(Star.new_id)
        self.coordinates = coordinates
        #TODO: use colortemp.py to give each star a realistic color

    @property
    def right_ascension(self):
        """Right ascension in degrees."""
        return self.coordinates.azimuthal * 180.0 / math.pi

    @property
    def declination(self):
        """Declination in degrees."""
        return self.coordinates.polar * 180.0 / math.pi

    @property
    def radial(self):
        """Get the radial distance."""
        return self.coordinates.radial

    @property
    def azimuthal(self):
        """Get the azimuthal angle in radians."""
        return self.coordinates.azimuthal

    @property
    def polar(self):
        """Get the polar angle in radians."""
        return self.coordinates.polar

    def __str__(self):
        return 'id: {id}, coord: ({radial:.3f}, {azimuthal:.3f}, {polar:.3f})'.format(id=self.id, radial=self.radial, azimuthal=self.azimuthal, polar=self.polar)
