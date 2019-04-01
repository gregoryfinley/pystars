# orbit_etc.py is just unused code cut from orbit.py

import math

# should write functions to determine the times and places of celestial events
# like equinoxes, solstices, etc.

def apoapsis(eccentricity, semimajor_axis):
    """Return apoapsis."""
    return semimajor_axis * (1.0 + eccentricity)

def periapsis(eccentricity, semimajor_axis):
    """Return periapsis."""
    return semimajor_axis * (1.0 - eccentricity)

def true_anomaly(eccentricity, eccentric_anomaly):
    """Return the angle between the orbit's periapsis and the orbiting body."""
        y = sqrt(1.0 + eccentricity) * math.sin(eccentric_anomaly / 2.0)
        x = sqrt(1.0 - eccentricity) * math.cos(eccentric_anomaly / 2.0)
        v = 2.0 * math.atan2(y, x)

def mean_motion(period):
    """Return the mean motion in radians."""
    return 2.0 * math.pi / period

def right_ascension(x, y)
    return math.atan2(y, x)

def declination(x, y, z)
    return math.atan2(z, math.sqrt(x * x + y * y))


# UNVERIFIED

def L_0(self):
    """Mean longitude at epoch."""
    return self.node + self.peri + self.M_0

def mean_longitude(self, t):
    """Get the mean longitude in radians at time since epoch t."""
    return self.node + self.peri + self.mean_anomaly(t)

def mean_anomaly(self, t):
    """Get the mean anomaly in radians at time since epoch t."""
    return 2.0 * math.pi * (t - self.tp) / self.period

