from tkinter import Label

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Ellipse, Rectangle, RoundedRectangle
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.slider import Slider
import math
import random

class PaintWidget(Widget):
    def __init__(self, **kwargs):
        super(PaintWidget, self).__init__(**kwargs)
        self.current_color = [1, 1, 1, 1]
        self.shape = "line"
        self.line_width = 2
        self.size_multiplier = 1.0
        self.shadow_enabled = False
        self.start_point = None  # For single straight lines
        self.control_points = []  # For Bezier curves

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            with self.canvas:
                Color(*self.current_color)
                if self.shadow_enabled:
                    Color(0, 0, 0, 0.3)
                    Rectangle(pos=(touch.x + 5, touch.y - 5),
                              size=(50 * self.size_multiplier, 50 * self.size_multiplier))
                Color(*self.current_color)

                if self.shape == "line":
                    if self.start_point is None:
                        self.start_point = (touch.x, touch.y)
                    else:
                        Line(points=[self.start_point[0], self.start_point[1], touch.x, touch.y], width=self.line_width)
                        self.start_point = None

                elif self.shape == "bezier":
                    self.control_points.append((touch.x, touch.y))
                    if len(self.control_points) == 3:
                        self.draw_bezier()

                elif self.shape == "star":
                    self.draw_star(touch.x, touch.y, 50 * self.size_multiplier)

                elif self.shape == "triangle":
                    self.draw_triangle(touch.x, touch.y, 50 * self.size_multiplier)

                elif self.shape == "rounded_rectangle":
                    RoundedRectangle(pos=(touch.x - 25 * self.size_multiplier, touch.y - 25 * self.size_multiplier),
                                     size=(50 * self.size_multiplier, 50 * self.size_multiplier),
                                     radius=[10 * self.size_multiplier])

                elif self.shape == "eraser":
                    Color(1, 1, 1, 1)
                    if random.choice([True, False]):
                        Ellipse(pos=(touch.x - 10, touch.y - 10), size=(20, 20))
                    else:
                        Rectangle(pos=(touch.x - 10, touch.y - 10), size=(20, 20))

    def draw_bezier(self):
        p0, p1, p2 = self.control_points
        points = []
        for t in [i / 100.0 for i in range(101)]:
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
            points.extend([x, y])
        Line(points=points, width=self.line_width)
        self.control_points.clear()

    def draw_star(self, x, y, size):
        points = []
        for i in range(10):
            angle = math.radians(i * 36)
            radius = size if i % 2 == 0 else size / 2
            points.extend([x + radius * math.cos(angle), y + radius * math.sin(angle)])
        Line(points=points, close=True, width=self.line_width)

    def draw_triangle(self, x, y, size):
        points = [
            x, y + size,
            x - size / 2, y - size / 2,
            x + size / 2, y - size / 2
        ]
        Line(points=points, close=True, width=self.line_width)

    def clear_canvas(self):
        self.canvas.clear()
        self.start_point = None
        self.control_points.clear()

class PaintApp(App):
    def build(self):
        layout = FloatLayout()

        self.paint_widget = PaintWidget()
        self.paint_widget.size_hint = (0.5, 1)
        self.paint_widget.pos_hint = {"x": 0, "y": 0}
        layout.add_widget(self.paint_widget)

        self.mirror_widget = PaintWidget()
        self.mirror_widget.size_hint = (0.5, 1)
        self.mirror_widget.pos_hint = {"x": 0.5, "y": 0}
        layout.add_widget(self.mirror_widget)

        clear_btn = Button(text="Очистить", size_hint=(0.1, 0.1), pos_hint={"x": 0, "y": 0.9})
        clear_btn.bind(on_release=lambda x: self.paint_widget.clear_canvas())
        layout.add_widget(clear_btn)

        color_picker = ColorPicker(size_hint=(0.2, 0.5), pos_hint={"x": 0.8, "y": 0.5})
        color_picker.bind(color=self.update_color)
        layout.add_widget(color_picker)

        line_btn = Button(text="Линия", size_hint=(0.1, 0.1), pos_hint={"x": 0, "y": 0.8})
        line_btn.bind(on_release=lambda x: self.set_shape("line"))
        layout.add_widget(line_btn)

        bezier_btn = Button(text="Безье", size_hint=(0.1, 0.1), pos_hint={"x": 0, "y": 0.7})
        bezier_btn.bind(on_release=lambda x: self.set_shape("bezier"))
        layout.add_widget(bezier_btn)

        star_btn = Button(text="Звезда", size_hint=(0.1, 0.1), pos_hint={"x": 0, "y": 0.6})
        star_btn.bind(on_release=lambda x: self.set_shape("star"))
        layout.add_widget(star_btn)

        triangle_btn = Button(text="Треугольник", size_hint=(0.1, 0.1), pos_hint={"x": 0, "y": 0.5})
        triangle_btn.bind(on_release=lambda x: self.set_shape("triangle"))
        layout.add_widget(triangle_btn)

        rounded_rect_btn = Button(text="Скругление", size_hint=(0.1, 0.1), pos_hint={"x": 0, "y": 0.4})
        rounded_rect_btn.bind(on_release=lambda x: self.set_shape("rounded_rectangle"))
        layout.add_widget(rounded_rect_btn)

        eraser_btn = Button(text="Ластик", size_hint=(0.1, 0.1), pos_hint={"x": 0.1, "y": 0.9})
        eraser_btn.bind(on_release=lambda x: self.set_shape("eraser"))
        layout.add_widget(eraser_btn)

        line_width_slider = Slider(min=1, max=20, value=self.paint_widget.line_width, size_hint=(0.3, 0.05),
                                   pos_hint={"x": 0.3, "y": 0.8})
        line_width_slider.bind(value=self.update_line_width)
        layout.add_widget(line_width_slider)

        # Кнопка сохранения
        save_btn = Button(text="Сохранить", size_hint=(0.1, 0.1), pos_hint={"x": 0.1, "y": 0.9})
        save_btn.bind(on_release=self.save_canvas)
        layout.add_widget(save_btn)

        return layout

    def update_color(self, instance, value):
        self.paint_widget.current_color = value

    def set_shape(self, shape):
        self.paint_widget.shape = shape

    def update_line_width(self, instance, value):
        self.paint_widget.line_width = int(value)

    def save_canvas(self, instance):
        self.paint_widget.export_to_png("drawing.png")
        print("Сохранено как drawing.png")

if __name__ == "__main__":
    PaintApp().run()
