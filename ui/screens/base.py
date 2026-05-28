# ─────────────────────────────────────────────
#  BASE SCREEN — base.py
#  Parent class for all screens in the app.
#  Provides StatusBar automatically to every
#  screen that inherits from it.
# ─────────────────────────────────────────────

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer

from ui.widgets.status_bar import StatusBar


class BaseScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Header()
        yield from self.screen_body()    # subclass content goes here
        yield Footer()
        yield StatusBar()

    def screen_body(self) -> ComposeResult:
        """
        Override this in every subclass instead of compose().
        Yields the main content of the screen.
        """
        return
        yield
