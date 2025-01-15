from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
import psycopg2

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres'
}

# Screen Definitions
class RegistrationScreen(Screen):
    login_input = ObjectProperty(None)
    password_input = ObjectProperty(None)
    error_label = ObjectProperty(None)

    def connect_to_database(self):
        try:
            with psycopg2.connect(**DB_CONFIG) as connection:
                connection.autocommit = True
                with connection.cursor() as cursor:
                    query = ("SELECT * FROM users WHERE login = %s AND password = %s")
                    cursor.execute(query, (self.login_input.text, self.password_input.text))
                    result = cursor.fetchone()
                    if result:
                        self.error_label.text = ""
                        return result
                    else:
                        self.error_label.text = "User not found!"
                        return None
        except Exception as e:
            self.error_label.text = "Database error!"
            print(e)
            return None

class UserInfoScreen(Screen):
    login_label = ObjectProperty(None)
    password_label = ObjectProperty(None)
    fio_label = ObjectProperty(None)
    email_label = ObjectProperty(None)
    phone_label = ObjectProperty(None)

    def set_data(self, user_data):
        self.login_label.text = f"Login: {user_data[1]}"
        self.password_label.text = f"Password: {user_data[2]}"
        self.fio_label.text = f"Full Name: {user_data[3]}"
        self.email_label.text = f"Email: {user_data[4]}"
        self.phone_label.text = f"Phone: {user_data[5]}"

class AddUserScreen(Screen):
    login_input = ObjectProperty(None)
    password_input = ObjectProperty(None)
    fio_input = ObjectProperty(None)
    email_input = ObjectProperty(None)
    phone_input = ObjectProperty(None)
    message_label = ObjectProperty(None)

    def add_user_to_database(self):
        try:
            with psycopg2.connect(**DB_CONFIG) as connection:
                connection.autocommit = True
                with connection.cursor() as cursor:
                    query = ("INSERT INTO users (login, password, fio, email, phone) VALUES (%s, %s, %s, %s, %s)")
                    cursor.execute(query, (
                        self.login_input.text,
                        self.password_input.text,
                        self.fio_input.text,
                        self.email_input.text,
                        self.phone_input.text
                    ))
                    self.message_label.text = "User added successfully!"
        except Exception as e:
            self.message_label.text = "Error adding user to database!"
            print(e)

class CustomScreenManager(ScreenManager):
    def switch_to_user_info(self, user_data):
        if user_data:
            self.current = "user_info"
            self.get_screen("user_info").set_data(user_data)
        else:
            print("Invalid login or password")

    def switch_to_registration(self):
        self.current = "registration"

    def switch_to_add_user(self):
        self.current = "add_user"

# Main Application
class Lab4App(App):
    def build(self):
        # Create ScreenManager and add screens
        manager = CustomScreenManager(transition=FadeTransition())

        registration_screen = RegistrationScreen(name="registration")
        user_info_screen = UserInfoScreen(name="user_info")
        add_user_screen = AddUserScreen(name="add_user")

        manager.add_widget(registration_screen)
        manager.add_widget(user_info_screen)
        manager.add_widget(add_user_screen)

        return manager

kv_content = """
<RegistrationScreen>:
    login_input: login_input
    password_input: password_input
    error_label: error_label

    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        Label:
            text: "Login"
            font_size: 24

        TextInput:
            id: login_input
            hint_text: "Enter your login"
            multiline: False

        TextInput:
            id: password_input
            hint_text: "Enter your password"
            multiline: False
            password: True

        Label:
            id: error_label
            text: ""
            color: 1, 0, 0, 1

        BoxLayout:
            size_hint_y: None
            height: '40dp'

            Button:
                text: "Submit"
                on_press: root.manager.switch_to_user_info(root.connect_to_database())

            Button:
                text: "Add User"
                on_press: root.manager.switch_to_add_user()

<UserInfoScreen>:
    login_label: login_label
    password_label: password_label
    fio_label: fio_label
    email_label: email_label
    phone_label: phone_label

    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        Label:
            id: login_label
            text: "Login:"

        Label:
            id: password_label
            text: "Password:"

        Label:
            id: fio_label
            text: "Full Name:"

        Label:
            id: email_label
            text: "Email:"

        Label:
            id: phone_label
            text: "Phone:"

        Button:
            text: "Back"
            on_press: root.manager.switch_to_registration()

<AddUserScreen>:
    login_input: login_input
    password_input: password_input
    fio_input: fio_input
    email_input: email_input
    phone_input: phone_input
    message_label: message_label

    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        Label:
            text: "Add New User"
            font_size: 24

        TextInput:
            id: login_input
            hint_text: "Enter login"
            multiline: False

        TextInput:
            id: password_input
            hint_text: "Enter password"
            multiline: False
            password: True

        TextInput:
            id: fio_input
            hint_text: "Enter full name"
            multiline: False

        TextInput:
            id: email_input
            hint_text: "Enter email"
            multiline: False

        TextInput:
            id: phone_input
            hint_text: "Enter phone"
            multiline: False

        Label:
            id: message_label
            text: ""
            color: 0, 1, 0, 1

        Button:
            text: "Add User"
            on_press: root.add_user_to_database()

        Button:
            text: "Back"
            on_press: root.manager.switch_to_registration()
"""

from kivy.lang import Builder
Builder.load_string(kv_content)

if __name__ == "__main__":
    Lab4App().run()
