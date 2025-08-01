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
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.behaviors import ButtonBehavior
from core.main import UVSimCore
from core.BasicMLOps import BasicMLOps

Builder.load_file('ConsoleWidget.kv')
Builder.load_file('LeftPaneWidget.kv')
Builder.load_file('MemRegWidget.kv')

class TabButton(ButtonBehavior, Label):
    # tab button widget
    def __init__(self, tab_name, file_path, content, **kwargs):
        super().__init__(**kwargs)
        self.tab_name = tab_name
        self.file_path = file_path
        self.content = content
        self.text = tab_name
        self.size_hint_y = None
        self.height = dp(40)
        self.size_hint_x = 1
        self.text_size = (None, None)
        self.halign = 'center'
        self.valign = 'middle'
        self.is_active = False
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.update_appearance()
    
    def update_graphics(self, *args):
        self.update_appearance()
    
    def update_appearance(self):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.is_active:
                Color(0.0, 0.518, 0.239, 1)  # Active tab color
            else:
                Color(0.2, 0.2, 0.2, 1)  # Inactive tab color
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(5)])
        
        if self.is_active:
            self.color = (1, 1, 1, 1)
        else:
            self.color = (0.8, 0.8, 0.8, 1)

class LeftPaneWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tabs = []  # List to store tab information
        self.active_tab_index = -1
        
        # Add a default "New File" tab
        Clock.schedule_once(self.add_default_tab, 0.1)

    def add_default_tab(self, dt):
        """Add a default empty tab"""
        self.add_tab("New File", None, "")

    #UI theme colors
    bg_color = ListProperty([0.09, 0.09, 0.09, 1])
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
            self.bg_color = [0.09, 0.09, 0.09, 1]
            self.text_color = [1, 1, 1, 1]
            self.button_bg_color = [0.0, 0.518, 0.239, 1]
            self.button_text_color = [1, 1, 1, 1]
            self.header_bg_color = [0.0, 0.518, 0.239, 1]
            self.header_text_color = [1, 1, 1, 1]

            # Reset right pane background
            root.ids.right_pane.canvas.before.children[0].rgba = (0.09, 0.09, 0.09, 1)

            # Reset MemReg background to gray
            root.ids.mem_reg_display.canvas.before.children[0].rgba = (0.09, 0.09, 0.09, 1)

            # Reset label colors to white
            root.ids.mem_reg_display.ids.accumulator_label.color = (1, 1, 1, 1)
            root.ids.mem_reg_display.ids.program_counter_label.color = (1, 1, 1, 1)
            for row in root.ids.mem_reg_display.ids.memory_box.children:
                label = row.children[1]
                label.color = (1, 1, 1, 1)

    def add_tab(self, tab_name, file_path, content):
        #Add a new tab with the given content
        # Store tab information first
        tab_info = {
            'name': tab_name,
            'file_path': file_path,
            'content': content,
            'button': None,
            'modified': False
        }
        tab_index = len(self.tabs)
        self.tabs.append(tab_info)
        
        # Create tab button with correct index
        tab_button = TabButton(tab_name, file_path, content)
        tab_button.bind(on_press=lambda x: self.switch_tab(tab_index))
        tab_info['button'] = tab_button
        
        # Add button to tab container
        if hasattr(self, 'ids') and 'tab_container' in self.ids:
            self.ids.tab_container.add_widget(tab_button)
        
        # Switch to the new tab
        self.switch_tab(tab_index)
    
    def switch_tab(self, tab_index):
        #Switch to the specified tab
        if tab_index < 0 or tab_index >= len(self.tabs):
            return
        
        # Save current tab content if there's an active tab
        if self.active_tab_index >= 0:
            current_content = self.ids.editor_input.text
            self.tabs[self.active_tab_index]['content'] = current_content
            self.tabs[self.active_tab_index]['button'].is_active = False
            self.tabs[self.active_tab_index]['button'].update_appearance()
        
        # Switch to new tab
        self.active_tab_index = tab_index
        tab_info = self.tabs[tab_index]
        
        # Update editor content
        self.ids.editor_input.text = tab_info['content']
        
        # Update tab button appearance
        tab_info['button'].is_active = True
        tab_info['button'].update_appearance()
    
    def close_tab(self, tab_index):
        #Close the specified tab
        if len(self.tabs) <= 1:
            return  # Don't close the last tab
        
        if tab_index < 0 or tab_index >= len(self.tabs):
            return
        
        # Remove tab button from UI
        tab_button = self.tabs[tab_index]['button']
        if hasattr(self, 'ids') and 'tab_container' in self.ids:
            self.ids.tab_container.remove_widget(tab_button)
        
        # Remove tab from list
        self.tabs.pop(tab_index)
        
        # Adjust active tab index
        if tab_index == self.active_tab_index:
            # If closing active tab, switch to previous tab or first tab
            new_active = max(0, tab_index - 1)
            self.active_tab_index = -1
            self.switch_tab(new_active)
        elif tab_index < self.active_tab_index:
            self.active_tab_index -= 1

    def upload_file(self):
        file_chooser = FileChooserListView(filters=['*.txt'], size_hint_y=0.9)
        btn_next = Button(text='Open in New Tab', size_hint_y=0.1)
        btn_cancel = Button(text='Cancel', size_hint_y=0.1)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(file_chooser)
        
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=10)
        button_layout.add_widget(btn_next)
        button_layout.add_widget(btn_cancel)
        layout.add_widget(button_layout)

        self.file_popup = Popup(title='Select BasicML File',
                                content=layout,
                                size_hint=(0.9, 0.9),
                                auto_dismiss=False)

        def open_in_new_tab(instance):
            if not file_chooser.selection:
                return
            file_path = file_chooser.selection[0]
            self.file_popup.dismiss()
            
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Extract filename for tab name
                tab_name = os.path.basename(file_path)
                
                # Add new tab
                self.add_tab(tab_name, file_path, content)
                
            except Exception as e:
                app = App.get_running_app()
                root = app.root
                root.ids.uvsim_console.add_message(f"Error loading file: {str(e)}")

        def cancel_file_popup(instance):
            self.file_popup.dismiss()

        btn_next.bind(on_press=open_in_new_tab)
        btn_cancel.bind(on_press=cancel_file_popup)
        self.file_popup.open()
    
    def save_current_tab(self):
        #Save the current tab's content
        if self.active_tab_index < 0:
            return
        
        current_tab = self.tabs[self.active_tab_index]
        current_content = self.ids.editor_input.text
        current_tab['content'] = current_content
        
        # If tab has a file path, save to that file
        if current_tab['file_path']:
            try:
                with open(current_tab['file_path'], 'w') as f:
                    f.write(current_content)
                current_tab['modified'] = False
            except Exception as e:
                app = App.get_running_app()
                root = app.root
                root.ids.uvsim_console.add_message(f"Error saving file: {str(e)}")
        else:
            with open("user_program.txt", "w") as out:
                out.write(current_content)
            current_tab['file_path'] = "user_program.txt"
            current_tab['name'] = "user_program.txt"
            current_tab['button'].text = "user_program.txt"
            current_tab['button'].tab_name = "user_program.txt"
            current_tab['modified'] = False
        
        self.load_current_tab_program()
    
    def load_current_tab_program(self):
        """Load the current tab's program into memory"""
        if self.active_tab_index < 0:
            return
        
        current_tab = self.tabs[self.active_tab_index]
        if not current_tab['file_path']:
            return
        
        app = App.get_running_app()
        root = app.root
        
        if not os.path.exists(current_tab['file_path']):
            root.ids.uvsim_console.add_message(f"Error: '{current_tab['file_path']}' not found.")
            return

        memory = app.CoreInstance.load_program(current_tab['file_path'])
        if memory is None:
            root.ids.uvsim_console.add_message("Error: Failed to load memory.")
            return
            
        self.populate_memory(root, memory)

    def new_tab(self):
        #Create a new empty tab
        tab_count = len([tab for tab in self.tabs if tab['name'].startswith('New File')])
        tab_name = f"New File {tab_count + 1}" if tab_count > 0 else "New File"
        self.add_tab(tab_name, None, "")

    def save_editor_to_file(self):
        self.save_current_tab()

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
        for i in range(250):
            mem_row = memory_box.children[249 - i]    #reverse stacked
            text_input = mem_row.children[0]
            text_input.text = f"{memory[i]:+06d}"    # for six-digit signed numbers

    def run_button(self):
        # First save the current tab
        self.save_current_tab()
        
        if self.active_tab_index < 0:
            return
        
        current_tab = self.tabs[self.active_tab_index]
        if not current_tab['file_path']:
            return
        
        app = App.get_running_app()
        root = app.root
        
        if not os.path.exists(current_tab['file_path']):
            root.ids.uvsim_console.add_message(f"Error: '{current_tab['file_path']}' not found.")
            return

        memory = app.CoreInstance.load_program(current_tab['file_path'])
        if memory is None:
            root.ids.uvsim_console.add_message("Error: Failed to load memory.")
            return
            
        self.populate_memory(root, memory)
        app.CoreInstance.run_program()
        #print("Program execution finished.")

        # root.ids.uvsim_console.add_message("Program execution finished")
        # print("Program execution finished")

    def step_button(self):
        app = App.get_running_app()
        core = app.CoreInstance
        root = app.root

        core.executor.step()

        # update registers on gui
        root.ids.mem_reg_display.ids.accumulator.text = f"{core.executor.memory_model.accumulator:+05d}"
        root.ids.mem_reg_display.ids.program_counter.text = f"{core.executor.memory_model.program_counter:02d}"

        # update memory on gui
        memory_box = root.ids.mem_reg_display.ids.memory_box
        for i in range(250):
            row = memory_box.children[249 - i]
            mem_input = row.children[0]
            mem_input.text = f"{core.memory_model.memory[i]:+06d}"   # also for runtime step update


class MemRegWidget(BoxLayout):
    # Sample 100 memory slots to test scrollability 
    def on_kv_post(self, base_widget):
        self.populate_memory()

    def populate_memory(self):
        memory_box = self.ids.memory_box
        for i in range(250):
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

    bg_color = ListProperty([0.09, 0.09, 0.09, 1])
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
