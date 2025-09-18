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
            "flex items-center gap-3 px-3 py-2 rounded-lg bg-slate-700 text-white w-full text-left transition-colors duration-200",
            "flex items-center gap-3 px-3 py-2 rounded-lg text-slate-400 hover:bg-slate-700 hover:text-white w-full text-left transition-colors duration-200",
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
                    class_name="font-semibold text-sm text-white",
                ),
                rx.el.p(
                    AuthState.current_user["email"], class_name="text-xs text-slate-400"
                ),
                class_name="flex-1",
            ),
            rx.el.button(
                rx.icon(
                    "log-out", class_name="w-5 h-5 text-slate-400 hover:text-red-400"
                ),
                on_click=AuthState.sign_out,
                class_name="p-2 rounded-md hover:bg-slate-700 transition-colors duration-200",
            ),
            class_name="flex items-center gap-3 p-2",
        ),
        class_name="mt-auto p-2 border-t border-slate-700",
    )


def sidebar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("message-square-more", class_name="w-8 h-8 text-blue-400"),
                rx.el.h2("ChatCompany", class_name="text-2xl font-bold text-white"),
                class_name="flex items-center gap-3 p-4 border-b border-slate-700",
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
        class_name="flex flex-col h-screen w-64 bg-slate-800 border-r border-slate-700",
    )