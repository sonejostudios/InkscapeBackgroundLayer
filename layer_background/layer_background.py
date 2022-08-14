#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2021 Vincent Rateau, info@sonejo.net
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
"""
This extension creates a background layer and draws a rectangle with the document's
or viewBox's (if present) size.
This extention is only compatible with Inkscape >= 1.0
"""

import inkex
from inkex import Rectangle
from inkex.elements import Group


# draw rectangle
def draw_rect(x, y, w, h, stroke_width, fill, name):
    elem = Rectangle(x=str(x), y=str(y), width=str(w), height=str(h))
    elem.style = {'stroke': '#000000', 'stroke-width': str(stroke_width), 'fill': fill}
    elem.set('inkscape:label', name)
    return elem

def parse_viewbox(viewbox):
    """Parse the specified viewbox string"""
    if viewbox is None:
        return None
    try:
        result = [float(coordinate) for coordinate in viewbox.split()]
    except ValueError:
        return None
    if len(result) != 4:
        return None
    return result



class DrawBackground(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--setcolor", default=inkex.Color("black"), type=inkex.Color, help="Replace color")

    def myrect(self):
        #Get options
        bgcolor = self.options.setcolor

        # Get access to main SVG document element
        svg = self.document.getroot()
        viewbox = parse_viewbox(svg.get('viewBox'))
        if viewbox is None:
            # if there is no viewbox, use the document dimensions
            # to size the background
            x = y = 0
            width  = self.svg.unittouu(svg.get('width'))
            height = self.svg.unittouu(svg.get('height'))
        else:
            # it there is a valid viewbox, use it to size (and position)
            # the background
            x, y, width, height = viewbox

        # Draw rectangle
        return draw_rect(x, y, width, height, 0, bgcolor, 'Background')


    def effect(self):
        # create locked background layer
        layer = self.svg.add(Group.new('Background', id='bglayer'))
        layer.set('inkscape:groupmode', 'layer')
        layer.set('sodipodi:insensitive', 'true')

        # append background rectangle to layer
        layer.append(self.myrect())



if __name__ == '__main__':
    DrawBackground().run()
