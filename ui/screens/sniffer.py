from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Label

from ui.screens.base import BaseScreen


class SnifferScreen(BaseScreen):

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
    ]

    def screen_body(self) -> ComposeResult:
        yield Label("Sniffer")