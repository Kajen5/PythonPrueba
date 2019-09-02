# This is a simple demo for advanced collisions and mesh creation from a set
# of points. Its purpose is only to give an idea on how to make complex stuff.

# Check garden.collider for better performance.

from math import cos, sin, pi, sqrt
from random import random, randint
from kivy import platform
from itertools import combinations
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config

Config.set('input', 'mouse', 'mouse,disable_multitouch')

from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, Mesh, Point, Ellipse
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.vector import Vector
from kivy.properties import (
    ListProperty,
    StringProperty,
    ObjectProperty,
    NumericProperty,
    ReferenceListProperty
)

Builder.load_string('''

<LinePlayground>:
    BoxLayout:
        orientation: "vertical"
        Label:
            font_size: "20sp"
            size_hint: 1, None
            text: "Score " + str(root.score)
        Label:
            font_size: "40sp"
            halign: 'center'
            valign: 'middle'
            center: root.center
            text: "Vida " + str(root.vida / 10.0) + " seg"
<Manager>:
    id: screen_manager

    Screen:
        name: "home"
        BoxLayout:
            orientation: "vertical"
            padding: 60
            spacing: 100
            Label:
                font_size: 70
                halign: "center"
                valign: "middle"
                text: "Guerra de Luz"
            Button:
                text: "Iniciar"
                halign: "center"
                valign: "middle"
                font_size: 100
                text_size: self.size
                on_release: root.current = 'game';game.onGame()

    Screen:
        name: "game"
        LinePlayground:
            id: game
    Screen:
        name: "Resumen"
        BoxLayout:
            orientation: "vertical"
            padding: 60
            spacing: 200
            Label:
                font_size: 70
                halign: "center"
                valign: "middle"
                text: "Score " + str(game.score) 
            Button:
                font_size: "30sp"
                text: "Salir"
                halign: "center"
                valign: "middle"
                on_release: root.current = "home";game.reset()
                ''')

# str(root.score) + " seg"


class BaseShape(Widget):
    '''(internal) Base class for moving with touches or calls.'''

    # keep references for offset
    _old_pos = ListProperty([0, 0])
    _old_touch = ListProperty([0, 0])
    _new_touch = ListProperty([0, 0])

    # shape properties
    name = StringProperty('')
    shape = ObjectProperty()
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

        dx = self.circulo.pos[0] + offset_x
        dy = self.circulo.pos[1] + offset_y
        self.circulo.pos =  dx, dy


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

        # move debug collider if available
        if self.circulo is not None:
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



class RegularShape(BaseShape):
    '''Starting from center and creating edges around for i.e.:
    regular triangles, squares, regular pentagons, up to "circle".
    '''
    color = []

    def __init__(self, color=None, **kwargs):
        super(RegularShape, self).__init__(**kwargs)

        self.color = color
        self.name = str(color)

        r_x = self.width / 2.0
        r_y = self.height / 2.0
            # add UV layout zeros for Mesh, see Mesh docs

        # draw Mesh shape from generated poly points
        with self.canvas:
            Color(*color)
            # self.shape = Ellipse(
            #     pos=self.pos
            # )

    def on_touch_down(self, touch, *args):
        pass


def generarColor():
    z = randint(0, 1020)
    if z < 255:
        color = (1, z / 255., 0)
    elif z < 510:
        color = (1 - ((z - 255) / 255.), 1, 0)
    elif z < 765:
        color = (0, 1, (z - 510) / 255.)
    else:
        color = (0, 1 - ((z - 765) / 255.), 1)
    return color



class LinePlayground(FloatLayout):
    menu = ObjectProperty()
    otros = list()
    player = ObjectProperty()
    tiempo = NumericProperty(0)
    score = NumericProperty(0)
    vida = NumericProperty(100)
    movy = NumericProperty(5.0)
    movx = NumericProperty(5.0)
    mov = ReferenceListProperty(movx, movy)
    player_x = NumericProperty(0)
    player_y = NumericProperty(0)
    auxiliar_vida = 0
    delay = NumericProperty(500)
    player_pos = ListProperty((0,0))
    _update = None
    use_mouse = platform not in ('ios', 'android')

    def __init__(self, **kwargs):
        super(LinePlayground, self).__init__(**kwargs)
        # register an event for collision
        self.register_event_type('on_collision')


    def onGame(self):
        if self.use_mouse:
            Window.show_cursor = False
        with self.canvas:
            Color(1, 1, 1)
            self.player = RegularShape(color=(1, 1, 1))
            self.player.pos = self.player_pos
        with self.player.canvas:
            Color(1,1,1)
            self.player.circulo = Ellipse(size=(40,40), pos=self.player.pos)
        self.player.size = 40, 40
        self._update = Clock.schedule_interval(self.update, 60 ** -1)

    def offGame(self):
        self._update.cancel()
        if self.use_mouse:
            Window.show_cursor = True
        self.parent.parent.current = "Resumen"

    def reset(self):
        self.score = 0
        self.tiempo = 0
        self.delay = 0
        self.movy = 5
        self.movx = 5
        self.otros.append(self.player)
        for i in self.otros:
            i.canvas
            self.otros.remove(i)
            self.remove_widget(i)
            del i
        self.player.canvas.remove(self.player.circulo)
        self.player = ObjectProperty()
        self.vida = 100


    def createOther(self, lista, color = None ):
        if color == None:
            color = generarColor()
            d = randint(70,150)
        else:
            color = 1,1,1
            d = 50
        shape = RegularShape(color=color)
        shape.pos = self.NewPosicion()
        lista.append(shape)
        self.add_widget(shape)
        cx, cy = shape.center
        shape.size = d, d
        with shape.canvas:
            Color(*color)
            shape.circulo = Ellipse(size=(d,d), pos=shape.pos)

    def NewPosicion(self):
        if self.movy == 0:
            x = randint(0, self.width)
            if self.movy > 0:
                y = self.height + 50
            else:
                y = -50
        elif randint(0, 100) > (100 * (abs(self.movy) / (abs(self.movx) +
             abs(self.movy)))):
            y = randint(-50, self.height-50)
            if self.movx > 0:
                x = self.width + 50
            else:
                x = -500
        else:
            x = randint(-50, self.width-50)
            if self.movy > 0:
                y = self.height + 50
            else:
                y = -50
        return x, y

    def on_collision(self, pair, *args):
        '''Dispatched when objects collide, gives back colliding objects
        as a "pair" argument holding their instances.
        '''
        if pair.color == (1, 1, 1):
            self.vida += 50
            self.score += 150
            pos = self.NewPosicion()
            pair.pos = pos
            pair.circulo.pos = pos
            self.movx, self.movy = Vector(self.movx, self.movy) * (1.05 - .05 * self.movx / 20)
            h = Vector(self.movx, self.movy)
            self.movx, self.movy = h.rotate(-10)
        else:
            self.vida -= 10

    def on_touch_move(self, touch):
        self.player_x, self.player_y = touch.pos


    def on_touch_down(self, touch):
        self.player_x, self.player_y = touch.pos
        # def build(self):
        # the environment for all 2D shapes

        # check for simple collisions between the shapes

    def update(self,nab):
        # list of 2D shapes, starting with regular ones
        h = Vector(self.movx, self.movy)
        self.movx, self.movy = h.rotate(0.05)

        if self.use_mouse:
            self.player.pos[0] = Window.mouse_pos[0] - self.player.height / 2
            self.player.pos[1] = Window.mouse_pos[1] - self.player.height / 2
        self.tiempo += 1
        if self.tiempo%10 == 0 and self.score/10 <= 21:
            print(len(self.otros))
            if randint(1,10) == 3:
                self.createOther(self.otros,(1, 1, 1))
            self.createOther(self.otros)
        for shape in self.otros:
            shape.move((self.movx, self.movy))
            if not ((-100 < shape.x < self.width + 55) or
            (-100 < shape.y < self.height + 55)):
                pos = self.NewPosicion()
                shape.pos = pos
                shape.circulo.pos = pos
        for com in self.otros:
            x = (self.player.center_x - com.center_x) ** 2
            y = (self.player.center_y - com.center_y) ** 2
            if sqrt(x + y) <= (self.player.height + com.height) / 2:
                # dispatch a custom event if the objects collide
                self.dispatch('on_collision', com)
        # move shapes to some random position
        if self.tiempo % 10 == 0:
            self.score += 1
            if self.vida < 0:
                self.offGame()
            self.vida -= 1

    def animate(self):
        self._update = Clock.schedule_interval(self.update, 60 ** -1)

class Manager(ScreenManager):

    def cambiar(self, name):
        self.current = name

class Collisions(App):
    def build(self):
        # game = LinePlayground() 
        # Window.allow_screensaver = False
        # Clock.schedule_interval(game.update,60 ** -1)
        return Manager()


if __name__ == '__main__':
    Collisions().run()