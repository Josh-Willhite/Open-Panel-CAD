"""
Created on Jun 24, 2013

[Copyright (c) 2013 Josh Willhite]

This program is released under the MIT license. Please see the file COPYING in this distribution for the license terms.
"""
import Panel


def getPanel(fileName):
    panel = Panel.Panel() # panel composed on individual lines

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
        print(shape)
        if 'LINE' in shape[1]:
            currLine = Panel.Line(shape[5].strip('\r'), float(shape[7]), float(shape[9]),
                            float(shape[11]), float(shape[13]),
                            float(shape[15]), float(shape[17]))

            panel.addLine(currLine)

    panel.centerXY()

    return panel


