import reflex as rx
from typing import Literal


class BaseState(rx.State):
    current_view: Literal["Chat", "Kanban", "Settings", "Users"] = "Kanban"

    def set_view(self, view: Literal["Chat", "Kanban", "Settings", "Users"]):
        self.current_view = view