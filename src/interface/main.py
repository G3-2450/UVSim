from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.lang import Builder

Builder.load_file('ConsoleWidget.kv')
Builder.load_file('LeftPaneWidget.kv')
Builder.load_file('MemRegWidget.kv')

class LeftPaneWidget(BoxLayout):
    pass

class MemRegWidget(BoxLayout):
    pass

class ConsoleWidget(BoxLayout):
    pass

class UVSimWindow(BoxLayout):
    pass

class UVSimApp(App):
    def build(self):
        return UVSimWindow()
    
if __name__ == '__main__':
    UVSimApp().run()