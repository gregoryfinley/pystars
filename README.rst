PyStars
=======

.. ::image image.PNG

This is a private project for learning and exploring both Python and the Doryen library (libtcod).

PyStars uses procedural generation to render an ASCII-style star map. It also computes the positions of the planets in our solar system and renders a view either from above or from the perspective of Earth using a simple equirectangular projection.

Requirements
------------

* Python 3.7.3
* python-tcod

Installation
------------

To install python-tcod::

    pip3 install tcod

To run the project::

    cd pystars-master
    python pystars

Keys
----

| tab: toggle view 
| up/down: increase/decrease time scale 
| pause: pause 
| space: reset 

References
----------

- https://en.wikipedia.org/wiki/Equatorial_coordinate_system
- http://mathworld.wolfram.com/SpherePointPicking.html
- http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/
- https://en.wikipedia.org/wiki/Hertzsprung%E2%80%93Russell_diagram
- https://en.wikipedia.org/wiki/Color%E2%80%93color_diagram
- https://en.wikipedia.org/wiki/Apparent_magnitude
- http://www.davidcolarusso.com/astro/
- https://ssd.jpl.nasa.gov/?planet_pos
- https://en.wikipedia.org/wiki/Equirectangular_projection
- https://en.wikipedia.org/wiki/Newton%27s_method
- http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python%2Blibtcod