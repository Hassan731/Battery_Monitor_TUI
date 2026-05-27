from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Header, Footer, Label


class FeatureCard(Widget):

    def __init__(self, icon: str, label: str) -> None:
        super().__init__()
        self.icon  = icon
        self.label = label

    def compose(self) -> ComposeResult:
        yield Label(self.icon,  classes="card-icon")
        yield Label(self.label, classes="card-name")


class HomeScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="home-grid"):
            with Horizontal(id="col-main"):
                with Vertical(id="col-bb"):
                    yield FeatureCard(icon="📦", label="Black Box & Logging")
                with Vertical(id="col-mid"):
                    yield FeatureCard(icon="📡", label="Live Monitoring")
                    yield FeatureCard(icon="📋", label="DID Read / Write")
            with Vertical(id="col-right"):
                yield FeatureCard(icon="🔍", label="CAN Sniffer")
                yield FeatureCard(icon="▶",  label="Routine Control")
                yield FeatureCard(icon="⚙",  label="Settings")
        yield Footer()