import sys
import os
from WriteToGuiConsole import WriteToGuiConsole
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
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from core.main import UVSimCore


from core.BasicMLOps import BasicMLOps

Builder.load_file('ConsoleWidget.kv')
Builder.load_file('LeftPaneWidget.kv')
Builder.load_file('MemRegWidget.kv')

class LeftPaneWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    #UI theme colors
    bg_color = ListProperty([0, 0, 0, 1])
    text_color = ListProperty([1, 1, 1, 1])
    button_bg_color = ListProperty([0.0, 0.518, 0.239, 1])
    button_text_color = ListProperty([1, 1, 1, 1])
    header_bg_color = ListProperty([0.0, 0.518, 0.239, 1])
    header_text_color = ListProperty([1, 1, 1, 1])

    #theme toggle handler
    def toggle_theme(self, mode):
        app = App.get_running_app()
        root = app.root

        if mode == "Light Mode":
            # Set light theme colors
            self.bg_color = [1, 1, 1, 1]
            self.text_color = [0, 0, 0, 1]
            self.button_bg_color = [0.0, 0.518, 0.239, 1]
            self.button_text_color = [1, 1, 1, 1]
            self.header_bg_color = [0.0, 0.518, 0.239, 1]
            self.header_text_color = [1, 1, 1, 1]

            # Change right pane background to white
            root.ids.right_pane.canvas.before.children[0].rgba = (1, 1, 1, 1)

            # Change MemReg background to white
            root.ids.mem_reg_display.canvas.before.children[0].rgba = (1, 1, 1, 1)

            # Change label colors to black
            root.ids.mem_reg_display.ids.accumulator_label.color = (0, 0, 0, 1)
            root.ids.mem_reg_display.ids.program_counter_label.color = (0, 0, 0, 1)
            for row in root.ids.mem_reg_display.ids.memory_box.children:
                label = row.children[1]  # label is second child
                label.color = (0, 0, 0, 1)

        else:
            # Set dark theme colors
            self.bg_color = [0, 0, 0, 1]
            self.text_color = [1, 1, 1, 1]
            self.button_bg_color = [0.0, 0.518, 0.239, 1]
            self.button_text_color = [1, 1, 1, 1]
            self.header_bg_color = [0.0, 0.518, 0.239, 1]
            self.header_text_color = [1, 1, 1, 1]

            # Reset right pane background
            root.ids.right_pane.canvas.before.children[0].rgba = (0.1608, 0.1608, 0.1608, 1)

            # Reset MemReg background to gray
            root.ids.mem_reg_display.canvas.before.children[0].rgba = (0.1608, 0.1608, 0.1608, 1)

            # Reset label colors to white
            root.ids.mem_reg_display.ids.accumulator_label.color = (1, 1, 1, 1)
            root.ids.mem_reg_display.ids.program_counter_label.color = (1, 1, 1, 1)
            for row in root.ids.mem_reg_display.ids.memory_box.children:
                label = row.children[1]
                label.color = (1, 1, 1, 1)

    def upload_file(self):
        file_chooser = FileChooserListView(filters=['*.txt'], size_hint_y=0.9)
        btn_next = Button(text='Next', size_hint_y=0.1)
        btn_cancel = Button(text='Cancel', size_hint_y=0.1)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(file_chooser)
        layout.add_widget(btn_next)
        layout.add_widget(btn_cancel)

        self.file_popup = Popup(title='Select BasicML File',
                                content=layout,
                                size_hint=(0.9, 0.9),
                                auto_dismiss=False)

        def open_editor(instance):
            if not file_chooser.selection:
                return
            file_path = file_chooser.selection[0]
            self.file_popup.dismiss()
            with open(file_path, 'r') as f:
                content = f.read()
            self.ids.editor_input.text = content

        def cancel_file_popup(instance):
            self.file_popup.dismiss()

        btn_next.bind(on_release=open_editor)
        btn_cancel.bind(on_release=cancel_file_popup)
        self.file_popup.open()

    def save_editor_to_file(self):
        content = self.ids.editor_input.text
        with open("user_program.txt", "w") as out:
            out.write(content)

        app = App.get_running_app()
        root = app.root
        file_path = "user_program.txt"
        if not os.path.exists(file_path):
            root.ids.uvsim_console.add_message("Error: 'user_program.txt' not found.")
            return

        memory = app.CoreInstance.load_program(file_path)
        self.populate_memory(root, memory)


    def open_editor_popup(self, file_path):
        #Opens the editor popup where the user can choose to edit the contents of the selected .txt file.
        #Once Save button is clicked, the file is saved as 'user_program.txt".
        #Args: file_path(str) : this argument is a string the represents the file path to the selected .txt file.
        
        with open(file_path, 'r') as f:
            content = f.read()

        self.editor_input = TextInput(text=content, multiline=True, size_hint_y=0.9)
        btn_save = Button(text='Save', size_hint_y=0.1)
        btn_cancel = Button(text='Cancel', size_hint_y=0.1)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(self.editor_input)
        layout.add_widget(btn_save)
        layout.add_widget(btn_cancel)

        self.editor_popup = Popup(title='Edit & Save File',
                                  content=layout,
                                  size_hint=(0.9, 0.9),
                                  auto_dismiss=False)

        def save_to_user_program(_):
            # saves the .txt file after edits as 'user_program.txt' and then closes the editor popup
            with open("user_program.txt", "w") as out:
                out.write(self.editor_input.text)

            app = App.get_running_app()
            root = app.root

            file_path = "user_program.txt"
            if not os.path.exists(file_path):
                root.ids.uvsim_console.add_message("Error: 'user_program.txt' not found.")
                return
            
            memory = app.CoreInstance.load_program(file_path)

            # app = App.get_running_app()
            # root = app.root
            self.populate_memory(root, memory)
            self.editor_popup.dismiss()
        
        def cancel_editor_popup(_):
            self.editor_popup.dismiss()

        btn_save.bind(on_release=save_to_user_program)
        btn_cancel.bind(on_release=cancel_editor_popup)
        self.editor_popup.open()

    def populate_memory(self, root, memory):
        memory_box = root.ids.mem_reg_display.ids.memory_box
        for i in range(100):
            mem_row = memory_box.children[99 - i]    #reverse stacked
            text_input = mem_row.children[0]
            text_input.text = f"{memory[i]:+06d}"    # for six-digit signed numbers


    def run_button(self):
        app = App.get_running_app()
        root = app.root
        file_path = "user_program.txt"

        if not os.path.exists(file_path):
            print("Error: 'user_program.txt' not found.")
            return

        memory = app.CoreInstance.load_program(file_path)
        self.populate_memory(root, memory)
        app.CoreInstance.run_program()
        #print("Program execution finished.")


        # root.ids.uvsim_console.add_message("Program execution finished")
        # print("Program execution finished")

    def step_button(self):
        app = App.get_running_app()
        core = app.CoreInstance
        root = app.root

        core.step()

        # update registers on gui
        root.ids.mem_reg_display.ids.accumulator.text = f"{core.accumulator:+05d}"
        root.ids.mem_reg_display.ids.program_counter.text = f"{core.program_counter:02d}"

        # update memory on gui
        memory_box = root.ids.mem_reg_display.ids.memory_box
        for i in range(100):
            row = memory_box.children[99 - i]
            mem_input = row.children[0]
            mem_input.text = f"{core.memory[i]:+06d}"   # also for runtime step update


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

            mem_label = Label(
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

            row.add_widget(mem_label)
            row.add_widget(mem_input)
            memory_box.add_widget(row)

    bg_color = ListProperty([0.1608, 0.1608, 0.1608, 1])
    label_color = ListProperty([1, 1, 1, 1])
    box_bg_color = ListProperty([0, 0, 0, 1])
    box_text_color = ListProperty([1, 1, 1, 1])

class ConsoleWidget(BoxLayout):
    # Call get_input with a callback function that takes the data the user enters as the input
    # Example:
    # 
    # def isEven(self, number):
    #     self.ConsoleWidget.get_input(
    #         prompt_text="Give me a number: ",
    #         InputFunction=labda user_input: self.isEven(user_input)
    #     )

    # To add a message to the console ouput, call add_message("a string you want printed")


    CallbackFunction = ObjectProperty(None, allownone=True)
    _current_prompt = StringProperty( "" ) 

    def execute_command( self, input ):
        print(f"Input recieved: { input }")
        self.ids.console_input.text = ""

        if self.CallbackFunction:
            callback_function = self.CallbackFunction
            self.CallbackFunction = None
            self.ids.console_input.disabled = True
            self.ids.console_input.hint_text = "Running program..."

            self.add_message( self._current_prompt + str( input ) )
            self._current_prompt = ""
            callback_function( input )
        else:
            self.add_message("Error: No input callback function provided")

    def add_message( self, text=None ):
        if text == None:
            return

        currentText = self.ids.console_output.text

        if currentText.strip():
            newText = currentText + "\n" + str( text )
        else:
            newText = str( text )
        
        self.ids.console_output.text = newText
        Clock.schedule_once( self._scroll_to_bottom, 0.1 )

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

class UVSimWindow(BoxLayout):
    pass

class UVSimApp(App):
    def build(self):
        Clock.schedule_once(self._setup_console_redirect, 0.1)

        return UVSimWindow()
    
    def _setup_console_redirect(self, dt):

        # redirect std output to the custom console
        add_message_func = App.get_running_app().root.ids.uvsim_console.add_message
        sys.stdout = WriteToGuiConsole(add_message_func)
        # sys.stderr = WriteToGuiConsole(add_message_func)

        # use get_input instead of input
        get_input_func = App.get_running_app().root.ids.uvsim_console.get_input
        self.CoreInstance = UVSimCore(get_input_func)
    
if __name__ == '__main__':
    UVSimApp().run()
