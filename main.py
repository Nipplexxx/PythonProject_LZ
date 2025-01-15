from kivy.app import App
from kivy.uix.label import Label

class NameApp(App):
    def build(self):
        return Label(text="Hello world!")

if __name__ == "__main__":
    NameApp().run()
