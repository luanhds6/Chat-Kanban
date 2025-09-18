import reflex as rx
from app.states.base_state import BaseState
from app.components.sidebar import sidebar
from app.components.kanban.kanban_board import kanban_board
from app.components.chat.chat_layout import chat_layout
from app.components.users.user_management import user_management_view
from app.components.settings.settings_page import settings_page


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.match(
                BaseState.current_view,
                ("Kanban", kanban_board()),
                ("Chat", chat_layout()),
                ("Users", user_management_view()),
                ("Settings", settings_page()),
                rx.el.div("Unknown View"),
            ),
            class_name="flex-1 flex flex-col overflow-hidden",
        ),
        class_name="flex h-screen bg-white font-['Inter']",
    )