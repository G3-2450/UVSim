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
from kivy.properties import StringProperty, ObjectProperty

Builder.load_file('ConsoleWidget.kv')
Builder.load_file('LeftPaneWidget.kv')
Builder.load_file('MemRegWidget.kv')

class LeftPaneWidget(BoxLayout):
    pass

class MemRegWidget(BoxLayout):
    # Sample 100 memory slots to test scrollability 
    def on_kv_post(self, base_widget):
        self.populate_memory()

    def populate_memory(self):
        memory_box = self.ids.memory_box
        for i in range(100):
            row = BoxLayout(
                orientation = 'horizontal',
                size_hint_y = None,
                height = dp(40),
                spacing = dp(8)
            )

            mem_lable = Label(
                text=f"{i:02}",
                size_hint_x=None,
                width=dp(30),
                halign='right',
                valign='middle',
                text_size=(dp(30), dp(40)),
                color=(1, 1, 1, 1),
                font_size='16sp'
            )

            mem_input = TextInput(
                text='+0000',
                readonly=True,
                multiline=False,
                font_size='18sp',
                halign='center',
                background_color=(0, 0, 0, 1),
                foreground_color=(1, 1, 1, 1),
                size_hint_x=1,
                height=dp(30)
            )

            row.add_widget(mem_lable)
            row.add_widget(mem_input)
            memory_box.add_widget(row)

class ConsoleWidget(BoxLayout):
    # Call get_input with a callback function that takes the data the user enters as the input
    # Example:
    # 
    # def isEven(self, number):
    #     self.console.get_input(
    #         prompt_text="Give me a number: ",
    #         InputFunction = self.isEven
    #     )

    CallbackFunction = ObjectProperty(None)

    def execute_command(self, command_text):
        print(f"Command recieved: {command_text}")
        self.ids.console_input.text = ""

        if self.CallbackFunction:
            callback_function = self.CallbackFunction
            self.CallbackFunction = None
            self.disable_input()
            callback_function(command_text)
        else:
            raise Exception("no inputcallback")
    
    def disable_input(self):
        self.ids.console_input.disabled = True
        self.ids.console_input.hint_text = "Running program..."
        print(f"input is disabled")

    def get_input(self, promptText="Enter value: ", InputFunction = None):
        if InputFunction == None:
            print("WARNING: get_input called with no callback function")
            return
        
        self.CallbackFunction = InputFunction
        self.ids.console_input.hint_text = promptText
        self.ids.console_input.disabled = False
        self.ids.console_input.focus = True
        print(f"input is enabled")

class UVSimWindow(BoxLayout):
    pass

class UVSimApp(App):
    def build(self):
        return UVSimWindow()
    
if __name__ == '__main__':
    UVSimApp().run()