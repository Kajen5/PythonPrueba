'''
Line (SmoothLine) Experiment
============================

This demonstrates the experimental and unfinished SmoothLine feature
for fast line drawing. You should see a multi-segment
path at the top of the screen, and sliders and buttons along the bottom.
You can click to add new points to the segment, change the transparency
and width of the line, or hit 'Animate' to see a set of sine and cosine
animations. The Cap and Joint buttons don't work: SmoothLine has not
implemented these features yet.
'''

from kivy.app import App
from kivy.properties import OptionProperty, NumericProperty, ListProperty, \
    BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.clock import Clock
from math import cos, sin
from kivy.core.window import Window
import random

Builder.load_string('''
<LinePlayground>:
    canvas:
        Color:
            rgba: .4, .4, 1, root.alpha
        Line:
            points: self.points
            joint: self.joint
            cap: self.cap
            width: self.linewidth
            close: self.close
        Color:
            rgba: .8, .8, .8, root.alpha_controlline
        Line:
            points: self.points
            close: self.close
        Color:
            rgba: 1, .4, .4, root.alpha
        Line:
            points: self.points2
            joint: self.joint
            cap: self.cap
            width: self.linewidth
            close: self.close

    GridLayout:
        cols: 3
        size_hint: 1, None
        height: 44 * 5

        GridLayout:
            cols: 2

            Label:
                text: 'Alpha'
            Slider:
                value: root.alpha
                on_value: root.alpha = float(args[1])
                min: 0.
                max: 1.
            Label:
                text: 'Alpha Control Line'
            Slider:
                value: root.alpha_controlline
                on_value: root.alpha_controlline = float(args[1])
                min: 0.
                max: 1.
            Label:
                text: 'Width'
            Slider:
                value: root.linewidth
                on_value: root.linewidth = args[1]
                min: 1
                max: 40
            Label:
                text: 'Cap'
            GridLayout:
                rows: 1
                ToggleButton:
                    group: 'cap'
                    text: 'none'
                    on_press: root.cap = self.text
                ToggleButton:
                    group: 'cap'
                    text: 'round'
                    on_press: root.cap = self.text
                ToggleButton:
                    group: 'cap'
                    text: 'square'
                    on_press: root.cap = self.text

            Label:
                text: 'Close'
            ToggleButton:
                text: 'Close line'
                on_press: root.close = self.state == 'down'

        AnchorLayout:
            GridLayout:
                cols: 1
                size_hint: None, None
                size: self.minimum_size
                ToggleButton:
                    size_hint: None, None
                    size: 100, 44
                    text: 'Animate'
                    on_state: root.animate(self.state == 'down')
                Button:
                    size_hint: None, None
                    size: 100, 44
                    text: 'Signal'
                    on_press: root.animate_signal()
                Button:
                    size_hint: None, None
                    size: 100, 44
                    text: 'Clear'
                    on_press: root.points = root.points2 = []

        GridLayout:
            cols: 2
            Label:
                text: 'hei'
            Slider:
                value: root.width * 0.8
                on_value: root.hei = args[1]
                min: 1
                max: 1000
            Label:
                text: 'test'
            Slider:
                value: root.tes
                on_value: root.tes = float(args[1])
                min: 1
                max: 50
            Label:
                text: 'velocidad'
            Slider:
                value: 1
                on_value: root.velocidad = float(args[1])
                min: 0
                max: 5
''')


class LinePlayground(FloatLayout):
    alpha_controlline = NumericProperty(1.0)
    alpha = NumericProperty(0.5)
    close = BooleanProperty(False)
    points = ListProperty([(100, 100),
                           [300, 300, 800, 300],
                           [500, 400, 100, 100]])
    points2 = ListProperty([])
    joint = OptionProperty('round')
    cap = OptionProperty('none', options=('round', 'square', 'none'))
    linewidth = NumericProperty(10.0)
    velocidad=NumericProperty(1)
    dt = NumericProperty(0)
    tes=NumericProperty(8)
    _update_points_animation_ev = None
    _update_points_signal=None
    step = 20
    hertz=150
    tempo=1
    signal=[random.random()for i in range(hertz*tempo)]

    def on_touch_down(self, touch):
        if super(LinePlayground, self).on_touch_down(touch):
            return True
        touch.grab(self)
        self.points.append(touch.pos)
        return True

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.points[-1] = touch.pos
            return True
        return super(LinePlayground, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            return True
        return super(LinePlayground, self).on_touch_up(touch)

    def animate(self, do_animation):
        if do_animation:
            self._update_points_animation_ev = Clock.schedule_interval(
                self.update_points_animation, 0)
            if self._update_points_signal is not None:
                self._update_points_signal.cancel()
        elif self._update_points_animation_ev is not None:
            self._update_points_animation_ev.cancel()

    def update_points_animation(self, dt):
        w=self.width * 0.8
        step=self.step
        cx=self.width * 0.1
        cy=self.height * 0.6
        hei=self.hei
        points = []
        points2 = []
        self.dt += (dt*self.velocidad)
        for i in range(int(w / step)):
            x = i * step
            points.append(cx + x)
            points.append(cy + cos(x / w * self.tes + self.dt) * hei * 0.2)
            points2.append(cx + x)
            points2.append(cy + sin(x / w * self.tes + self.dt) * hei * 0.2)
        self.points = points
        self.points2 = points2

    def animate_signal(self):
        w=self.width * 0.8
        cx=self.width * 0.1
        cy=self.height * 0.6
        hei=self.hei
        signal_adap=[]
        update=self.hertz*self.tempo
        for i,s in enumerate(self.signal):
            signal_adap.append(cx + i * w / update)
            signal_adap.append(cy + s * hei *0.2)
        self.points=signal_adap
            

class TestLineApp(App):
    def build(self):
        Window.Background = "yellow"
        Window.resizable = 1
        Window.allow_screensaver = False
        return LinePlayground() 


if __name__ == '__main__':
    TestLineApp().run()
