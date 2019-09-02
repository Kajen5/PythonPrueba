# This is a simple demo for advanced collisions and mesh creation from a set
# of points. Its purpose is only to give an idea on how to make complex stuff.

# Check garden.collider for better performance.

from math import cos, sin, pi, sqrt
from random import random, randint
from itertools import combinations

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.vector import Vector

Config.set('graphics', 'show_cursor', '0')
Config.set('input', 'mouse', 'mouse,disable_multitouch')

from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, Mesh, Point, Ellipse
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import (
    ListProperty,
    StringProperty,
    ObjectProperty,
    NumericProperty
)


class BaseShape(Widget):
    '''(internal) Base class for moving with touches or calls.'''

    # keep references for offset
    _old_pos = ListProperty([0, 0])
    _old_touch = ListProperty([0, 0])
    _new_touch = ListProperty([0, 0])

    # shape properties
    name = StringProperty('')
    poly = ListProperty([])
    shape = ObjectProperty()
    poly_len = NumericProperty(0)
    shape_len = NumericProperty(0)
    debug_collider = ObjectProperty()
    circulo = ObjectProperty()
    debug_collider_len = NumericProperty(0)

    def __init__(self, **kwargs):
        '''Create a shape with size [100, 100]
        and give it a label if it's named.
        '''
        super(BaseShape, self).__init__(**kwargs)
        self.size_hint = (None, None)


    def move_collider(self, offset_x, offset_y, *args):
        '''Move debug collider when the shape moves.'''
        points = self.debug_collider.points[:]

        for i in range(0, self.debug_collider_len, 2):
            points[i] += offset_x
            points[i + 1] += offset_y
        self.debug_collider.points = points
        dx = self.circulo.pos[0] + offset_x
        dy = self.circulo.pos[1] + offset_y
        self.circulo.pos =  dx, dy

    def on_debug_collider(self, instance, value):
        '''Recalculate length of collider points' array.'''
        self.debug_collider_len = len(value.points)

    def on_poly(self, instance, value):
        '''Recalculate length of polygon points' array.'''
        self.poly_len = len(value)

    def on_shape(self, instance, value):
        '''Recalculate length of Mesh vertices' array.'''

    def on_pos(self, instance, pos):
        '''Move polygon and its Mesh on each position change.
        This event is above all and changes positions of the other
        children-like components, so that a simple::

            shape.pos = (100, 200)

        would move everything, not just the widget itself.
        '''

        # position changed by touch
        offset_x = self._new_touch[0] - self._old_touch[0]
        offset_y = self._new_touch[1] - self._old_touch[1]

        # position changed by call (shape.pos = X)
        if not offset_x and not offset_y:
            offset_x = pos[0] - self._old_pos[0]
            offset_y = pos[1] - self._old_pos[1]
            self._old_pos = pos

        # move polygon points by offset
        for i in range(0, self.poly_len, 2):
            self.poly[i] += offset_x
            self.poly[i + 1] += offset_y

        # move debug collider if available
        if self.debug_collider is not None:
            self.move_collider(offset_x, offset_y)

        # return if no Mesh available
        if self.shape is None:
            return

        # move Mesh vertices by offset



    def move(self, touch, *args):
        '''Move shape with dragging.'''

        # grab single touch for shape

        # get touches
        x = self.x - touch[0]
        y = self.y - touch[1]
        new_pos = [x, y]
        self._new_touch = new_pos
        self._old_touch = [self.x, self.y]

        # get offsets, move & trigger on_pos event
        offset_x = self._new_touch[0] - self._old_touch[0]
        offset_y = self._new_touch[1] - self._old_touch[1]
        self.pos = [self.x + offset_x, self.y + offset_y]

    def shape_collide(self, x, y, *args):
        '''Point to polygon collision through a list of points.'''

        # ignore if no polygon area is set
        poly = self.poly
        if not poly:
            return False

        n = self.poly_len
        inside = False
        p1x = poly[0]
        p1y = poly[1]

        # compare point pairs via PIP algo, too long, read
        # https://en.wikipedia.org/wiki/Point_in_polygon
        for i in range(0, n + 2, 2):
            p2x = poly[i % n]
            p2y = poly[(i + 1) % n]

            if y > min(p1y, p2y) and y <= max(p1y, p2y) and x <= max(p1x, p2x):
                if p1y != p2y:
                    xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                if p1x == p2x or x <= xinters:
                    inside = not inside

            p1x, p1y = p2x, p2y
        return inside


class RegularShape(BaseShape):
    '''Starting from center and creating edges around for i.e.:
    regular triangles, squares, regular pentagons, up to "circle".
    '''
    color = []
    punto = int()

    def __init__(self, punto=0, edges=20, color=None, **kwargs):
        self.punto = punto
        super(RegularShape, self).__init__(**kwargs)
        if edges < 3:
            raise Exception('Not enough edges! (3+ only)')

        self.color = color
        self.name = str(color)
        rad_edge = (pi * 2) / float(edges)
        r_x = self.width / 2.0
        r_y = self.height / 2.0
        poly = []
        for i in range(edges):
            # get points within a circle with radius of [r_x, r_y]
            x = cos(rad_edge * i) * r_x + self.center_x
            y = sin(rad_edge * i) * r_y + self.center_y
            poly.extend([x, y])

            # add UV layout zeros for Mesh, see Mesh docs

        # draw Mesh shape from generated poly points
        with self.canvas:
            Color(*color)
            # self.shape = Ellipse(
            #     pos=self.pos
            # )
        self.poly = poly

    def on_touch_down(self, touch, *args):
        if self.shape_collide(*touch.pos):
            touch.grab(self)


class LinePlayground(FloatLayout):
    otros = list()
    player = ObjectProperty()
    movy = 4
    movx = 8
    mov = ReferenceListProperty(velocity_x, velocity_y)
    player_x = NumericProperty(0)
    player_y = NumericProperty(0)
    player_pos = ListProperty((0,0))


    def __init__(self, **kwargs):
        super(LinePlayground, self).__init__(**kwargs)
        # register an event for collision
        self.register_event_type('on_collision')
        self.height = Window.size[0]
        self.width = Window.size[1]
        with self.canvas:
            Color(1,1,1)
            self.player = RegularShape(color=(1,1,1))
            self.player.pos = self.player_pos
            self.collision_circles(self.player, distance=20, color=(1,1,1), debug=True)
    


    def collision_circles(self, shape=None, distance=100, debug=False,color=None, *args):
        '''Simple circle <-> circle collision between the shapes i.e. there's
        a simple line between the centers of the two shapes and the collision
        is only about measuring distance -> 1+ radii intersections.
        '''

        # get all combinations from all available shapes


        for com in self.otros:
            x = (self.player.center_x - com.center_x) ** 2
            y = (self.player.center_y - com.center_y) ** 2
            if sqrt(x + y) <= distance:
                # dispatch a custom event if the objects collide
                self.dispatch('on_collision',  com)

        # draw collider only if debugging
        if not debug:
            return

        # add circle collider only if the shape doesn't have one
        d = distance / 2.0
        cx, cy = shape.center
        points = [(cx + d * cos(i), cy + d * sin(i)) for i in range(44)]
        points = [p for ps in points for p in ps]
        with shape.canvas:
            Color(*color)
            shape.debug_collider = Point(points=points)
            shape.circulo = Ellipse(size=(distance+2,distance+2), pos=[shape.center_x - distance/2, shape.center_y - distance/2])
 

    def on_collision(self, pair, *args):
        '''Dispatched when objects collide, gives back colliding objects
        as a "pair" argument holding their instances.
        '''
        pair.color

    def on_touch_move(self, touch):
        self.player_x, self.player_y = touch.pos
        self.hola = str(touch.pos)

    def build(self):
        # the environment for all 2D shapes
        scene = FloatLayout()

        # check for simple collisions between the shapes
        Clock.schedule_interval(self.update,0)
        return scene

    def update(self,nab):
        # list of 2D shapes, starting with regular ones
        self.player.pos = Window.mouse_pos
        for shape in self.otros:
            
            if not (-100< shape.x < self.width+55):
                del shape
                continue
            if not (-100 < shape.y < self.height+55):
                del shape
                continue
            shape.move((self.movx,self.movy))

        if randint(0, 100) > 80:
            z = randint(0, 1020)
            if z < 255:
                color = (1, z / 255., 0)
            elif z < 510:
                color = (1 - ((z - 255) / 255.), 1, 0)
            elif z < 765:
                color = (0, 1, (z - 510) / 255.)
            else:
                color = (0, 1 - ((z - 765) / 255.), 1)
            shape = RegularShape(color=color, punto=z, size=(30,30))
            print(len(self.otros))
            if randint(0, 100) > (100 * (abs(self.movy) / (abs(self.movx) +
             abs(self.movy)))):
                shape.y = randint(0, self.height)
                if self.movx > 0:
                    shape.x = self.width + 50
                if -self.movx > 0:
                    shape.x = -500
            else:
                shape.x = randint(0, self.width)
                if self.movy > 0:
                    shape.y = self.height + 50
                if -self.movy > 0:
                    shape.y = -50
            self.otros.append(shape)
            self.add_widget(shape)
            self.collision_circles(shape, distance=randint(50,100), color=color, debug=True)

        # move shapes to some random position

class Collisions(App):
    def build(self):
        game = LinePlayground() 
        Window.Background = "yellow"
        Window.resizable = 1
        Window.allow_screensaver = False
        Clock.schedule_interval(game.update,60**-1)
        return game


if __name__ == '__main__':
    Collisions().run()