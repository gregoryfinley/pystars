"""Orbit.py docstring."""

import math

def right_ascension(x, y):
    return math.atan2(y, x) * 180.0 / math.pi

def declination(x, y, z):
    return math.atan2(z, math.sqrt(x * x + y * y)) * 180.0 / math.pi

def eccentric_anomaly(mean_anomaly, eccentricity, tolerance=1e-6):
    """Return the eccentric anomaly in radians.

    Uses the Newton-Raphson method to approximate a solution for the value
    of E in Kepler's equation, M = E - e * math.sin(E), where M = mean
    anomaly, E = eccentric anomaly, and e = eccentricity.

    Args:
        mean_anomaly: The mean anomaly in radians.
        eccentricity: The eccentricity.
        tolerance: The tolerance required to accept a solution to 
            Kepler's equation. Defaults to 1e-6.

    Returns:
        float: The eccentric anomaly in radians.

    Raises:
        ZeroDivisionError: The Newton-Raphson method divided by zero.
    """
    E = mean_anomaly + eccentricity * math.sin(mean_anomaly)
    while abs(E - eccentricity * math.sin(E) - mean_anomaly) > tolerance:
        func = E - eccentricity * math.sin(E) - mean_anomaly
        func_prime = 1.0 - eccentricity * math.cos(E)
        try:
            E = E - func / func_prime
        except ZeroDivisionError:
            raise
    return E

class Orbit():
    """An elliptical orbit defined by six Keplerian elements.
    
    Attributes:
        eccentricity: Eccentricity.
        semimajor_axis: Semi-major axis in au.
        inclination: Inclination in radians.
        ascending_node: Longitude of the ascending node in radians.
        arg_peri: Argument of periapsis in radians.
        epoch_mean_anomaly: Mean anomaly at epoch in radians.
    """

    def __init__(self, eccentricity, semimajor_axis, inclination,
                 ascending_node, arg_peri, epoch_mean_anomaly, degrees=True):
        """Inits Orbit with six Keplerian elements."""
        self.eccentricity = eccentricity
        self.semimajor_axis = semimajor_axis
        if degrees:
            self.inclination = math.radians(inclination)
            self.ascending_node = math.radians(ascending_node)
            self.arg_peri = math.radians(arg_peri)
            self.epoch_mean_anomaly = math.radians(epoch_mean_anomaly)
        else:
            self.inclination = inclination
            self.ascending_node = ascending_node
            self.arg_peri = arg_peri
            self.epoch_mean_anomaly = epoch_mean_anomaly

    @property
    def period(self):
        """Sidereal period in years."""
        return math.sqrt(self.semimajor_axis ** 3.0)

    @property
    def periapsis_time(self):
        """Time of periapsis passage in years from epoch."""
        return -1.0 * self.epoch_mean_anomaly * self.period / (2.0 * math.pi)

    def position(self, t):
        """Get the ecliptic coordinates at time since epoch t."""

        # M = mean anomaly at t
        M = 2.0 * math.pi * (t - self.periapsis_time) / self.period

        E = eccentric_anomaly(M, self.eccentricity) # call self or Orbit?

        # v = true anomaly
        y = math.sqrt(1.0 + self.eccentricity) * math.sin(E / 2.0)
        x = math.sqrt(1.0 - self.eccentricity) * math.cos(E / 2.0)
        v = 2.0 * math.atan(y/x) # here atan produces nicer results than atan2

        # r = radial distance
        r = (self.semimajor_axis * (1.0 - self.eccentricity ** 2) / (1.0 
             + self.eccentricity * math.cos(v)))

        # note: (r,v) is the orbiting body's polar coordinates in its own
        # orbital plane with origin at focus

        # reduced form of Z-X'-Z" passive Euler rotation to ecliptic plane
        X = (r * (math.cos(self.ascending_node) * math.cos(self.arg_peri + v)
             - math.sin(self.ascending_node) * math.sin(self.arg_peri + v) 
             * math.cos(self.inclination)))
        Y = (r * (math.sin(self.ascending_node) * math.cos(self.arg_peri + v)
             + math.cos(self.ascending_node) * math.sin(self.arg_peri + v)
             * math.cos(self.inclination)))
        Z = (r * math.sin(self.arg_peri + v) * math.sin(self.inclination))

        return (X, Y, Z)

    def __str__(self):
        return ("e:{e:.7f} a:{a:.4f} i:{i:.4f} node:{node:.4f} peri:{peri:.4f}"
                " M:{M:.4f}".format(e=self.eccentricity, a=self.semimajor_axis,
                i=self.inclination, node=self.ascending_node,
                peri=self.arg_peri, M=self.epoch_mean_anomaly))