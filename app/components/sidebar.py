import reflex as rx
from app.states.base_state import BaseState
from app.states.auth_state import AuthState


def nav_item(icon: str, text: str, view: str) -> rx.Component:
    return rx.el.button(
        rx.icon(icon, class_name="w-5 h-5"),
        rx.el.span(text, class_name="font-medium"),
        on_click=lambda: BaseState.set_view(view),
        class_name=rx.cond(
            BaseState.current_view == view,
            "flex items-center gap-3 px-3 py-2 rounded-lg bg-gray-100 text-gray-900 w-full text-left",
            "flex items-center gap-3 px-3 py-2 rounded-lg text-gray-500 hover:bg-gray-100 hover:text-gray-900 w-full text-left",
        ),
    )


def user_profile_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.img(
                src=f"https://api.dicebear.com/9.x/initials/svg?seed={AuthState.current_user['full_name']}",
                class_name="w-10 h-10 rounded-full",
            ),
            rx.el.div(
                rx.el.p(
                    AuthState.current_user["full_name"],
                    class_name="font-semibold text-sm text-gray-900",
                ),
                rx.el.p(
                    AuthState.current_user["email"], class_name="text-xs text-gray-500"
                ),
                class_name="flex-1",
            ),
            rx.el.button(
                rx.icon(
                    "log-out", class_name="w-5 h-5 text-gray-500 hover:text-red-500"
                ),
                on_click=AuthState.sign_out,
                class_name="p-2 rounded-md hover:bg-gray-100",
            ),
            class_name="flex items-center gap-3 p-2",
        ),
        class_name="mt-auto p-2 border-t border-gray-100",
    )


def sidebar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("message-square-more", class_name="w-8 h-8 text-blue-600"),
                rx.el.h2("TeamSync", class_name="text-2xl font-bold text-gray-900"),
                class_name="flex items-center gap-3 p-4 border-b border-gray-100",
            ),
            rx.el.nav(
                nav_item("kanban", "Kanban Board", "Kanban"),
                nav_item("message-circle", "Chat", "Chat"),
                rx.cond(
                    AuthState.current_user["role"] == "Admin",
                    nav_item("users", "Manage Users", "Users"),
                    rx.fragment(),
                ),
                nav_item("settings", "Settings", "Settings"),
                class_name="flex flex-col gap-1 p-2",
            ),
        ),
        user_profile_card(),
        class_name="flex flex-col h-screen w-64 bg-white border-r border-gray-100",
    )