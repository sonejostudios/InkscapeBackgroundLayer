#!/usr/bin/env python

# These two lines are only needed if you don't put the script directly into
# the installation directory
import sys
sys.path.append('/usr/share/inkscape/extensions')

# We will use the inkex module with the predefined Effect base class
import inkex
# The simplestyle module provides functions for style parsing
import simplestyle



class AddBackgroundLayer(inkex.Effect):
    """
    Creates a new background layer with black or white background color.
    """
    def __init__(self):
        """
        Constructor.
        Defines the "--bgcolor" option of a script.
        """
        # Call the base class constructor
        inkex.Effect.__init__(self)

        # Define string option "--bgcolor" with "-b" shortcut and default value "#FFFFFF"
        self.OptionParser.add_option('-b', '--bgcolor', action = 'store',
          type = 'string', dest = 'bgcolor', default = '#FFFFFF',
          help = 'Background color')



    def draw_SVG_square(self, (w,h), (x,y), parent):
        """
        Method to draw rectangles.
        """

        # Get script's "--bgcolor" option value
        what = self.options.bgcolor


        style = {   'stroke'        : 'none',
                    'stroke-width'  : '1',
                    'fill'          : '%s' % what
                }
                    
        attribs = {
            'style'     : simplestyle.formatStyle(style),
            'height'    : str(h),
            'width'     : str(w),
            'x'         : str(x),
            'y'         : str(y)
                }
        circ = inkex.etree.SubElement(parent, inkex.addNS('rect','svg'), attribs )

    
    def effect(self):
        """
        Effect behaviour.
        Overrides base class' method and inserts new preview layer.
        """
        # Get script's "--bgcolor" option value
        what = self.options.bgcolor

        # Get access to main SVG document element and get its dimensions
        svg = self.document.getroot()

        # Get document dimentions
        width  = self.unittouu(svg.get('width'))
        height = self.unittouu(svg.get('height'))


        # Create a new layer
        background_layer = inkex.etree.SubElement(svg, 'g')
        background_layer.set(inkex.addNS('label', 'inkscape'), 'Background Layer')
        background_layer.set(inkex.addNS('id'), 'background_layer')
        background_layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
        background_layer.set(inkex.addNS('insensitive', 'sodipodi'), 'true') #lock layer


        # background layer as parent
        #parent = self.current_layer
        parent = background_layer

        
        # draw rectangles on preview layer
        #draw_SVG_square((w,h), (x,y), parent)
        
        #draw background layer
        self.draw_SVG_square((width,height), (0,0), parent)








# Create effect instance and apply it
effect = AddBackgroundLayer()
effect.affect()



