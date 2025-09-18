import reflex as rx
from typing import TypedDict
import datetime


class ChatMessage(TypedDict):
    sender: str
    receiver: str
    text: str
    timestamp: str


class ChatState(rx.State):
    messages: list[ChatMessage] = [
        {
            "sender": "jane.doe@example.com",
            "receiver": "admin@example.com",
            "text": "Hey, can you review the latest designs for the landing page?",
            "timestamp": "10:30 AM",
        },
        {
            "sender": "admin@example.com",
            "receiver": "jane.doe@example.com",
            "text": "Sure, send them over. I'll take a look this afternoon.",
            "timestamp": "10:31 AM",
        },
        {
            "sender": "jane.doe@example.com",
            "receiver": "admin@example.com",
            "text": "Great, thanks! I've attached the Figma link to the Kanban card.",
            "timestamp": "10:31 AM",
        },
        {
            "sender": "john.smith@example.com",
            "receiver": "admin@example.com",
            "text": "Morning! Just wanted to confirm our marketing sync for 2 PM.",
            "timestamp": "11:00 AM",
        },
    ]
    active_chat_with: str = "jane.doe@example.com"

    def set_active_chat(self, email: str):
        self.active_chat_with = email

    @rx.var
    async def current_chat_messages(self) -> list[ChatMessage]:
        from app.states.auth_state import AuthState

        auth_state = await self.get_state(AuthState)
        current_user_email = auth_state.current_user_email
        return [
            msg
            for msg in self.messages
            if msg["sender"] == current_user_email
            and msg["receiver"] == self.active_chat_with
            or (
                msg["sender"] == self.active_chat_with
                and msg["receiver"] == current_user_email
            )
        ]

    @rx.event
    async def send_message(self, form_data: dict):
        from app.states.auth_state import AuthState

        auth_state = await self.get_state(AuthState)
        current_user_email = auth_state.current_user_email
        message_text = form_data["message"].strip()
        if not message_text:
            return
        new_message: ChatMessage = {
            "sender": current_user_email,
            "receiver": self.active_chat_with,
            "text": message_text,
            "timestamp": datetime.datetime.now().strftime("%I:%M %p"),
        }
        self.messages.append(new_message)
        yield