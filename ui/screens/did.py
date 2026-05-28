from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Label


class DIDScreen(Screen):

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Black Box & Logging")
        yield Footer()