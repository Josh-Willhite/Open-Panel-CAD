'''
Created on Jun 24, 2013

@author: Josh Willhite
'''


class Line:
    def __init__(self, layer, x0, y0, z0, x1, y1, z1):
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.layer = layer

    def __str__(self):
        return ("\nLayer:%s (%.3f, %.3f, %.3f) (%.3f, %.3f, %.3f)\n"
                % (self.layer, self.x0, self.y0, self.z0, self.x1, self.y1,
                self.z1))


def getLines(fileName):
    """

    :param fileName:
    :return:
    """
    lines = []  # array to hold line objects

    f = open(fileName, 'r')
    dxf = f.read()
    f.close()
    # filter the geometry objects into a list
    geoTextBlock = (dxf[dxf.index('ENTITIES') + 8:dxf.index('VIEWPORT')]
                    .split('  0'))
    # remove the 1st and last empty elements of the list
    geoTextBlock = geoTextBlock[1:len(geoTextBlock) - 1]

    for textBlock in geoTextBlock:
        shape = textBlock.split('\n')
        if shape[1] == 'LINE':
            currLine = Line(shape[5], float(shape[7]), float(shape[9]),
                            float(shape[11]), float(shape[13]),
                            float(shape[15]), float(shape[17]))

            lines.append(currLine)
    return lines


