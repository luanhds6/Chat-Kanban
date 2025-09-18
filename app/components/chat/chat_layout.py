import reflex as rx
from app.states.auth_state import AuthState
from app.states.chat_state import ChatState


def contact_item(user: dict) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.el.img(
                src=f"https://api.dicebear.com/9.x/initials/svg?seed={user['full_name']}",
                class_name="w-10 h-10 rounded-full",
            ),
            rx.cond(
                user["online"],
                rx.el.div(
                    class_name="absolute bottom-0 right-0 w-3 h-3 bg-green-500 border-2 border-white rounded-full"
                ),
                rx.el.div(
                    class_name="absolute bottom-0 right-0 w-3 h-3 bg-gray-400 border-2 border-white rounded-full"
                ),
            ),
            class_name="relative",
        ),
        rx.el.div(
            rx.el.p(user["full_name"], class_name="font-semibold text-gray-800"),
            rx.el.p(user["department"], class_name="text-sm text-gray-500"),
            class_name="flex-1 text-left",
        ),
        on_click=lambda: ChatState.set_active_chat(user["email"]),
        class_name=rx.cond(
            ChatState.active_chat_with == user["email"],
            "flex items-center gap-3 p-3 w-full rounded-lg bg-blue-50",
            "flex items-center gap-3 p-3 w-full rounded-lg hover:bg-gray-100",
        ),
    )


def message_bubble(message: dict, is_sender: bool) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(message["text"], class_name="text-sm"),
            class_name=rx.cond(
                is_sender,
                "bg-blue-600 text-white p-3 rounded-xl max-w-md",
                "bg-gray-200 text-gray-800 p-3 rounded-xl max-w-md",
            ),
        ),
        rx.el.span(message["timestamp"], class_name="text-xs text-gray-400 mt-1"),
        class_name=rx.cond(
            is_sender, "flex flex-col items-end", "flex flex-col items-start"
        ),
    )


def chat_layout() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Contacts", class_name="text-xl font-bold p-4 text-gray-900 border-b"
            ),
            rx.el.div(
                rx.foreach(
                    AuthState.users.values(),
                    lambda user: rx.cond(
                        user["email"] != AuthState.current_user_email,
                        contact_item(user),
                        rx.fragment(),
                    ),
                ),
                class_name="p-2 space-y-1 overflow-y-auto",
            ),
            class_name="w-80 border-r bg-white flex flex-col",
        ),
        rx.el.div(
            rx.cond(
                ChatState.active_chat_with,
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            AuthState.users[ChatState.active_chat_with]["full_name"],
                            class_name="text-lg font-semibold text-gray-900",
                        ),
                        rx.el.p(
                            AuthState.users[ChatState.active_chat_with]["department"],
                            class_name="text-sm text-gray-500",
                        ),
                        class_name="p-4 border-b bg-white",
                    ),
                    rx.el.div(
                        rx.foreach(
                            ChatState.current_chat_messages,
                            lambda msg: message_bubble(
                                msg, msg["sender"] == AuthState.current_user_email
                            ),
                        ),
                        class_name="flex-1 p-6 space-y-6 overflow-y-auto",
                    ),
                    rx.el.div(
                        rx.el.form(
                            rx.el.input(
                                name="message",
                                placeholder="Type a message...",
                                class_name="flex-1 bg-gray-100 border-transparent rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none",
                            ),
                            rx.el.button(
                                rx.icon("send", class_name="w-5 h-5"),
                                type="submit",
                                class_name="p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700",
                            ),
                            on_submit=ChatState.send_message,
                            reset_on_submit=True,
                            class_name="flex items-center gap-3",
                        ),
                        class_name="p-4 border-t bg-white",
                    ),
                    class_name="flex flex-col h-full",
                ),
                rx.el.div(
                    rx.icon("message-circle-off", class_name="w-24 h-24 text-gray-300"),
                    rx.el.p(
                        "Select a contact to start chatting",
                        class_name="text-gray-500 font-medium mt-4",
                    ),
                    class_name="flex flex-col items-center justify-center h-full text-center",
                ),
            ),
            class_name="flex-1 bg-gray-50 flex flex-col",
        ),
        class_name="flex flex-1 overflow-hidden",
    )