Created on Jun 24, 2013
[Copyright (c) 2013 Josh Willhite]
Repository: https://github.com/Josh-Willhite/Open-Panel-CAD
Email: jwillhite@gmail.com

# Open-Panel-CAD

Transform a 2D DXF format aluminum composite panel drawing into a 3D model

### -BASIC FUNCTIONALITY-

Allows the user to create a a folded 3D model of a panel based on a 2D flat pattern stored in a dxf format file.
---

### -Work Flow-

1. Issue command "->open foo.dxf"
2. Issue command "->view top" to view the XY plane.
3. Select lines that makes up the plane to be folded, also select route line that the plane will be folded around.
4. Issue command "->fold angle", note angle is in degrees.
5. Repeat steps 1-4 until panel is folded.
---

### -INSTALL INSTRUCTIONS-

1. Install or verify that the following dependencies exist on your machine:
    1. Python2.7 follow instructions here: http://www.python.org
    2. Pyglet1.1.4 follow instructions here: http://pyglet.org/
    3. Numpy follow instructions here: http://www.numpy.org/
2. Pull source code from repository or download archive.
3. At command prompt run:python2.7 display.py


