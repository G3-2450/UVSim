import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from core.main import load_program, run_program


from core.BasicMLOps import BasicMLOps

Builder.load_file('ConsoleWidget.kv')
Builder.load_file('LeftPaneWidget.kv')
Builder.load_file('MemRegWidget.kv')

class LeftPaneWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def upload_file(self): 
        # Opens a popup with the FileChooserListView window allowing the user to choose a .txt file. 
        # Once a file is selected, the Next button is clicked, passing the file to the editor popup.
        file_chooser = FileChooserListView(filters=['*.txt'], size_hint_y=0.9)
        btn_next = Button(text='Next', size_hint_y=0.1)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(file_chooser)
        layout.add_widget(btn_next)

        self.file_popup = Popup(title='Select BasicML File',
                                content=layout,
                                size_hint=(0.9, 0.9),
                                auto_dismiss=False)

        def open_editor(instance):
        # Handles transition of the .txt file from the file chooser popup to the editor popup.
            if not file_chooser.selection:
                return
            file_path = file_chooser.selection[0]
            self.file_popup.dismiss()
            self.open_editor_popup(file_path)

        btn_next.bind(on_release=open_editor)
        self.file_popup.open()

    def open_editor_popup(self, file_path):
        #Opens the editor popup where the user can choose to edit the contents of the selected .txt file.
        #Once Save button is clicked, the file is saved as 'user_program.txt".
        #Args: file_path(str) : this argument is a string the represents the file path to the selected .txt file.
        
        with open(file_path, 'r') as f:
            content = f.read()

        self.editor_input = TextInput(text=content, multiline=True, size_hint_y=0.9)
        btn_save = Button(text='Save', size_hint_y=0.1)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(self.editor_input)
        layout.add_widget(btn_save)

        self.editor_popup = Popup(title='Edit & Save File',
                                  content=layout,
                                  size_hint=(0.9, 0.9),
                                  auto_dismiss=False)

        def save_to_user_program(_):
            # saves the .txt file after edits as 'user_program.txt' and then closes the editor popup
            with open("user_program.txt", "w") as out:
                out.write(self.editor_input.text)
            self.editor_popup.dismiss()

        btn_save.bind(on_release=save_to_user_program)
        self.editor_popup.open()

    def run_button(self):
        app = App.get_running_app()
        root = app.root

        file_path = "user_program.txt"
        if not os.path.exists(file_path):
            root.ids.uvsim_console.add_message("Error: 'user_program.txt' not found.")
            return
        
        memory = load_program(file_path)

        memory_box = root.ids.mem_reg_display.ids.memory_box
        for i in range(100):
            mem_row = memory_box.children[99 - i] #reverse stacked
            text_input = mem_row.children[0]
            text_input.text = f"{memory[i]:05d}"

        run_program(memory)

        root.ids.uvsim_console.add_message("Program execution finished")


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

    # To add a message to the console ouput, call add_message("a string you want printed")


    CallbackFunction = ObjectProperty(None)
    _current_prompt = StringProperty("")

    def execute_command(self, input):
        print(f"Command recieved: {input}")
        self.ids.console_input.text = ""

        if self.CallbackFunction:
            callback_function = self.CallbackFunction
            self.CallbackFunction = None
            self.disable_input()
            
            self.add_message(self._current_prompt + str(input))
            self._current_prompt = None
            callback_function(input)
        else:
            raise Exception("no inputcallback")
    
    def disable_input(self):
        self.ids.console_input.disabled = True
        self.ids.console_input.hint_text = "Running program..."
        print(f"input is disabled")

    def add_message(self, text=None):
        if text == None:
            return

        currentText = self.ids.console_output.text

        if currentText.strip():
            newText = currentText + "\n" + str(text)
        else:
            newText = str(text)
        
        self.ids.console_output.text = newText
        Clock.schedule_once(self._scroll_to_bottom, 0.1)

    #added scroll to bottom funcion - console scolls to latest output
    def _scroll_to_bottom(self, *args):
        scroll_view = self.ids.console_scroll_view
        scroll_view.scroll_y = 0

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
