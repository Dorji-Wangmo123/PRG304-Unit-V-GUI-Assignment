
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup


class HelloDorjiApp(App):

    def build(self):

        # Main layout
        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        # Heading
        label = Label(
            text="Hello!",
            font_size=24
        )

        # Click button
        button = Button(
            text="Click Me",
            font_size=20,
            size_hint=(1, 0.3)
        )

        button.bind(on_press=self.show_message)

        layout.add_widget(label)
        layout.add_widget(button)

        return layout

    # Display popup message
    def show_message(self, instance):

        popup_layout = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=15
        )

        message = Label(
            text="Hello! Welcome to Kivy.",
            font_size=18
        )

        ok_button = Button(
            text="OK",
            size_hint=(1, 0.4)
        )

        popup_layout.add_widget(message)
        popup_layout.add_widget(ok_button)

        popup = Popup(
            title="Message",
            content=popup_layout,
            size_hint=(0.7, 0.4),
            auto_dismiss=False
        )

        ok_button.bind(on_press=popup.dismiss)

        popup.open()


if __name__ == "__main__":
    HelloDorjiApp().run()
