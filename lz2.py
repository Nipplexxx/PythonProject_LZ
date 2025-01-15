from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.properties import StringProperty
from random import choice
import webbrowser

# Список шрифтов для случайного выбора
FONTS = ['Roboto', 'DejaVuSans', 'Arial']

class LabWorkApp(App):
    text_length = StringProperty("Длина текста: 0")

    def build(self):
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # **1. Таблица для ввода данных**
        data_table = GridLayout(cols=2, size_hint=(1, 0.2))
        self.input1 = TextInput(hint_text="Введите фамилию", multiline=False)
        self.input2 = TextInput(hint_text="Введите имя", multiline=False)
        self.input3 = TextInput(hint_text="Введите возраст", multiline=False)
        self.input4 = TextInput(hint_text="Введите email", multiline=False)

        data_table.add_widget(Label(text="Фамилия:"))
        data_table.add_widget(self.input1)
        data_table.add_widget(Label(text="Имя:"))
        data_table.add_widget(self.input2)
        data_table.add_widget(Label(text="Возраст:"))
        data_table.add_widget(self.input3)
        data_table.add_widget(Label(text="Email:"))
        data_table.add_widget(self.input4)

        root.add_widget(data_table)

        # **2. FloatLayout с кнопкой добавления**
        float_layout = FloatLayout(size_hint=(1, 0.2))
        submit_button = Button(
            text="Добавить данные", size_hint=(0.3, 0.3), pos_hint={'x': 0.35, 'y': 0.35}
        )
        submit_button.bind(on_press=self.add_data)

        self.data_label = Label(
            text="Добавленные данные появятся здесь",
            size_hint=(1, 0.5),
            pos_hint={'x': 0, 'y': 0.7},
        )
        float_layout.add_widget(self.data_label)
        float_layout.add_widget(submit_button)
        root.add_widget(float_layout)

        # **3. Панель с ссылками**
        link_panel = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), spacing=10)
        self.link_display = TextInput(text="Выберите ссылку", readonly=True, size_hint=(0.4, 1))
        link_panel.add_widget(self.link_display)

        links = [
            ("Kivy Docs", "https://kivy.org/doc/stable"),
            ("Python", "https://www.python.org"),
            ("GitHub", "https://github.com"),
            ("Google", "https://www.google.com"),
        ]

        for name, url in links:
            button = Button(text=name, size_hint=(0.15, 1))
            button.bind(on_press=lambda instance, u=url: self.open_link(u))
            link_panel.add_widget(button)

        root.add_widget(link_panel)

        # **4. Слайдер для изменения размера кнопки**
        slider_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        slider_label = Label(text="Измените размер кнопки:", size_hint=(0.3, 1))
        self.slider = Slider(min=50, max=200, value=100, size_hint=(0.7, 1))
        self.slider.bind(value=self.on_slider_value_change)

        slider_layout.add_widget(slider_label)
        slider_layout.add_widget(self.slider)
        root.add_widget(slider_layout)

        # **5. StackLayout для кнопок**
        stack_layout = StackLayout(size_hint=(1, 0.2), spacing=10)
        for i in range(5):
            stack_layout.add_widget(Button(text=f"Кнопка {i + 1}", size_hint=(0.2, 0.5)))
        root.add_widget(stack_layout)

        # **6. AnchorLayout с сеткой**
        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(1, 0.2))
        grid_in_anchor = GridLayout(cols=3, rows=1, size_hint=(None, None), size=(300, 100))
        for i in range(3):
            grid_in_anchor.add_widget(Button(text=f"Сетка {i + 1}"))
        anchor_layout.add_widget(grid_in_anchor)
        root.add_widget(anchor_layout)

        # **7. Три колонки с BoxLayout**
        column_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        for i in range(3):
            box = BoxLayout(orientation='vertical')
            for j in range(3):
                box.add_widget(Button(text=f"Колонка {i + 1} Виджет {j + 1}"))
            column_layout.add_widget(box)
        root.add_widget(column_layout)

        # **8. Вывод состояния кнопок**
        state_button = Button(text="Состояние кнопки", size_hint=(1, 0.1))
        state_button.bind(
            on_press=lambda instance: print("Кнопка нажата"),
            on_release=lambda instance: print("Кнопка отпущена")
        )
        root.add_widget(state_button)

        return root

    def add_data(self, instance):
        """Добавляет данные из текстовых полей в метку с выбором случайного шрифта."""
        font = choice(FONTS)
        self.data_label.text = (
            f"[font={font}]Фамилия: {self.input1.text}\n"
            f"Имя: {self.input2.text}\n"
            f"Возраст: {self.input3.text}\n"
            f"Email: {self.input4.text}[/font]"
        )
        self.input1.text = ""
        self.input2.text = ""
        self.input3.text = ""
        self.input4.text = ""

    def open_link(self, url):
        """Открывает указанную ссылку в браузере."""
        self.link_display.text = url
        webbrowser.open(url)

    def on_slider_value_change(self, instance, value):
        """Изменяет размер шрифта метки в зависимости от положения слайдера."""
        self.data_label.font_size = value

if __name__ == "__main__":
    LabWorkApp().run()
