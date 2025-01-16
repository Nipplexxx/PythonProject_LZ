from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle


# Виджет с цветным фоном
class ColoredBackground(Widget):
    def __init__(self, color, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


# Первый экран
class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(ColoredBackground((0.2, 0.6, 0.8, 1)))

        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)
        self.title = Label(text="Добро пожаловать в игру Крестики-Нолики!",
                           font_size=24, color=(1, 1, 1, 1), size_hint_y=None, height=50)
        self.title.opacity = 0  # Прячем текст для анимации
        layout.add_widget(self.title)

        next_button = Button(text="Далее", font_size=24,
                             size_hint=(0.5, 0.2), pos_hint={"center_x": 0.5},
                             background_color=(0.3, 0.7, 0.3, 1), background_normal="")
        next_button.bind(on_press=self.go_to_next)
        layout.add_widget(next_button)

        self.add_widget(layout)
        self.animate_elements()

    def animate_elements(self):
        anim = Animation(opacity=1, duration=1.5)
        anim.start(self.title)

    def go_to_next(self, instance):
        self.manager.transition = SlideTransition(direction="left", duration=1)
        self.manager.current = "screen2"


# Второй экран
class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(ColoredBackground((0.8, 0.5, 0.3, 1)))

        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)
        self.title = Label(text="Введите имена игроков", font_size=24, color=(1, 1, 1, 1))
        self.title.opacity = 0
        layout.add_widget(self.title)

        self.player1_input = TextInput(hint_text="Имя первого игрока",
                                       font_size=20, size_hint_y=None, height=50)
        layout.add_widget(self.player1_input)

        self.player2_input = TextInput(hint_text="Имя второго игрока",
                                       font_size=20, size_hint_y=None, height=50)
        layout.add_widget(self.player2_input)

        start_game_button = Button(text="Начать игру", font_size=24, size_hint=(0.5, 0.2),
                                   pos_hint={"center_x": 0.5}, background_color=(0.7, 0.3, 0.5, 1),
                                   background_normal="")
        start_game_button.bind(on_press=self.start_game)
        layout.add_widget(start_game_button)

        self.add_widget(layout)
        self.animate_elements()

    def animate_elements(self):
        anim = Animation(opacity=1, duration=1.5)
        anim.start(self.title)

    def start_game(self, instance):
        player1 = self.player1_input.text
        player2 = self.player2_input.text

        if player1 and player2:
            self.manager.get_screen("screen3").set_players(player1, player2)
            self.manager.transition = SlideTransition(direction="left", duration=1)
            self.manager.current = "screen3"


# Третий экран
class TicTacToeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(ColoredBackground((0.4, 0.4, 0.8, 1)))

        self.players = ("", "")
        self.turn = "X"
        self.board = [None] * 9

        self.layout = BoxLayout(orientation="vertical", spacing=10, padding=20)
        self.status_label = Label(text="Ход: X", font_size=24, color=(1, 1, 1, 1), size_hint_y=None, height=50)
        self.layout.add_widget(self.status_label)

        self.grid = GridLayout(cols=3, spacing=5, size_hint_y=0.6)
        for i in range(9):
            btn = Button(font_size=32, background_color=(0.3, 0.3, 0.7, 1), background_normal="")
            btn.bind(on_press=self.make_move)
            self.grid.add_widget(btn)
            self.board[i] = btn
        self.layout.add_widget(self.grid)

        restart_button = Button(text="Играть снова", font_size=24, size_hint=(0.5, 0.2),
                                pos_hint={"center_x": 0.5}, background_color=(0.6, 0.3, 0.4, 1),
                                background_normal="")
        restart_button.bind(on_press=self.restart_game)
        self.layout.add_widget(restart_button)

        self.add_widget(self.layout)

    def set_players(self, player1, player2):
        self.players = (player1, player2)
        self.status_label.text = f"Ход: {self.turn} ({self.players[0]})"

    def make_move(self, instance):
        if instance.text == "":
            instance.text = self.turn
            if self.check_winner():
                self.status_label.text = f"Победитель: {self.turn} ({self.get_current_player()})"
                self.disable_board()
                return
            self.turn = "O" if self.turn == "X" else "X"
            self.status_label.text = f"Ход: {self.turn} ({self.get_current_player()})"

    def check_winner(self):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for condition in win_conditions:
            if self.board[condition[0]].text == self.board[condition[1]].text == self.board[condition[2]].text != "":
                return True
        return False

    def disable_board(self):
        for btn in self.board:
            btn.disabled = True

    def restart_game(self, instance):
        self.turn = "X"
        for btn in self.board:
            btn.text = ""
            btn.disabled = False
        self.status_label.text = f"Ход: {self.turn} ({self.players[0]})"

    def get_current_player(self):
        return self.players[0] if self.turn == "X" else self.players[1]


# Приложение
class TicTacToeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FirstScreen(name="screen1"))
        sm.add_widget(SecondScreen(name="screen2"))
        sm.add_widget(TicTacToeScreen(name="screen3"))
        return sm


if __name__ == "__main__":
    TicTacToeApp().run()