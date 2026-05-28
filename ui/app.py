from textual.app import App, ComposeResult
from ui.screens.home import HomeScreen


class MyApp(App):

    CSS_PATH =  [
                    "styles/app.tcss",
                    "styles/home.tcss",
                    "styles/sniffer.tcss",
                ]

    TITLE = "BMS Tester"

    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        self.push_screen(HomeScreen())