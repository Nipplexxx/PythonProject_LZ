from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
import random
import requests
import asyncio

class TaskApp(App):
    def build(self):
        # Главный макет для приложения
        self.layout = FloatLayout()

        # Кнопка для задания 1: Ввод данных в таблицу из кнопок
        self.table_button = Button(
            text="Добавить данные в таблицу",
            size_hint=(0.3, 0.1),
            pos_hint={"x": 0.35, "y": 0.8},
            on_press=self.add_to_table
        )
        self.layout.add_widget(self.table_button)

        # Таблица (GridLayout) для задания 1
        self.table = GridLayout(cols=4, size_hint=(0.9, 0.4), pos_hint={"x": 0.05, "y": 0.4})
        for header in ["Фамилия", "Имя", "Возраст", "Email"]:
            self.table.add_widget(Label(text=header))
        self.layout.add_widget(self.table)

        # Кнопка для задания 2: Переход по внешней ссылке
        self.link_button = Button(
            text="Открыть ссылку",
            size_hint=(0.3, 0.1),
            pos_hint={"x": 0.35, "y": 0.6},
            on_press=self.open_link
        )
        self.layout.add_widget(self.link_button)

        # Кнопка для выполнения HTTP-запроса (requests)
        self.http_button = Button(
            text="HTTP запрос",
            size_hint=(0.3, 0.1),
            pos_hint={"x": 0.35, "y": 0.5},
            on_press=self.perform_http_request
        )
        self.layout.add_widget(self.http_button)

        # Кнопка для асинхронного запроса (aiohttp)
        self.async_button = Button(
            text="Асинхронный запрос",
            size_hint=(0.3, 0.1),
            pos_hint={"x": 0.35, "y": 0.4},
            on_press=lambda x: asyncio.run(self.perform_async_request())
        )
        self.layout.add_widget(self.async_button)

        # Виджет DropDown (выпадающее меню)
        dropdown = DropDown()
        for option in ["Option 1", "Option 2", "Option 3"]:
            btn = Button(text=option, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        self.dropdown_button = Button(
            text="Выбрать опцию",
            size_hint=(0.3, 0.1),
            pos_hint={"x": 0.35, "y": 0.3}
        )
        self.dropdown_button.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(self.dropdown_button, 'text', x))
        self.layout.add_widget(self.dropdown_button)

        return self.layout

    def add_to_table(self, instance):
        """Добавляет данные в таблицу из кнопок (задание 1)."""
        for data in ["Иванов", "Иван", str(random.randint(18, 60)), "ivanov@example.com"]:
            self.table.add_widget(Label(text=data))

    def open_link(self, instance):
        """Открывает внешнюю ссылку (задание 2)."""
        import webbrowser
        webbrowser.open("https://www.google.com")

    def perform_http_request(self, instance):
        """Выполняет HTTP-запрос с использованием библиотеки requests."""
        try:
            response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
            if response.status_code == 200:
                print("Response:", response.json())
            else:
                print("Error:", response.status_code)
        except Exception as e:
            print("Request failed:", e)

    async def perform_async_request(self):
        """Выполняет асинхронный HTTP-запрос с использованием aiohttp."""
        import aiohttp
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://jsonplaceholder.typicode.com/posts/1") as response:
                    if response.status == 200:
                        data = await response.json()
                        print("Async Response:", data)
                    else:
                        print("Async Error:", response.status)
        except Exception as e:
            print("Async request failed:", e)

if __name__ == "__main__":
    TaskApp().run()
