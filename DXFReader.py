'''
Created on Jun 24, 2013

Copyright (c) 2013 @author: Josh Willhite

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
import Panel

def getPanel(fileName):
    """

    :param fileName:
    :return:
    """

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
        if shape[1] == 'LINE':
            currLine = Panel.Line(shape[5], float(shape[7]), float(shape[9]),
                            float(shape[11]), float(shape[13]),
                            float(shape[15]), float(shape[17]))

            panel.addLine(currLine)
    return panel


