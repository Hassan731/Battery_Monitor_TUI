from textual.app import App, ComposeResult
from textual.widgets import Header, Label, Footer

class BMSMonitorApp(App):

    # TITLE is shown in the header
    TITLE = "BMS Monitor"          
    
    # global key bindings (automatically added to the help menu and Footer)
    BINDINGS =  [
                    ("q", "quit", "Quit")       # (key, action_name, label)
                ]


    # Define the UI layout in the compose method
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Label("Hello from BMS Tester")
