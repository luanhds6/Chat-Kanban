import reflex as rx
from typing import Literal, TypedDict
from app.states.auth_state import AuthState


class SettingsState(rx.State):
    active_tab: str = "Perfil"
    language: str = "Portugués (Brasil)"
    timezone: str = "(GMT-03:00) Brasilía"
    push_notifications: bool = True
    email_notifications: bool = True
    sound_notifications: bool = False
    silent_hours_start: str = "22:00"
    silent_hours_end: str = "08:00"
    theme: str = "light"
    accent_color: str = "blue"
    notion_connected: bool = True
    google_drive_connected: bool = False
    slack_webhook_url: str = ""
    session_expiration: int = 24
    password_policy: dict = {"length": 8, "uppercase": True, "number": True}
    active_users_stat: int = 152
    messages_sent_stat: int = 12843
    tasks_created_stat: int = 789

    @rx.event
    async def load_user_settings(self):
        auth_state = await self.get_state(AuthState)
        if auth_state.current_user:
            user = auth_state.current_user
            self.language = user.get("language", "Portugués (Brasil)")
            self.timezone = user.get("timezone", "(GMT-03:00) Brasilía")

    def set_active_tab(self, tab_name: str):
        self.active_tab = tab_name

    @rx.event
    async def save_profile_settings(self, form_data: dict):
        auth_state = await self.get_state(AuthState)
        if auth_state.current_user:
            user = auth_state.current_user
            user["full_name"] = form_data["full_name"]
            user["department"] = form_data["department"]
            user["language"] = form_data["language"]
            user["timezone"] = form_data["timezone"]
            self.language = user["language"]
            self.timezone = user["timezone"]
            auth_state.users[auth_state.current_user_email] = user
            yield rx.toast.success("Perfil salvo com sucesso!")

    @rx.event
    async def change_password(self, form_data: dict):
        current_password = form_data["current_password"]
        new_password = form_data["new_password"]
        confirm_password = form_data["confirm_password"]
        auth_state = await self.get_state(AuthState)
        if auth_state.current_user:
            user = auth_state.current_user
            if user["password"] != current_password:
                yield rx.toast.error("Senha atual incorreta.")
                return
            if new_password != confirm_password:
                yield rx.toast.error("As novas senhas não coincidem.")
                return
            if not auth_state._validate_password(new_password):
                yield rx.toast.error("A nova senha não é forte o suficiente.")
                return
            user["password"] = new_password
            auth_state.users[auth_state.current_user_email] = user
            yield rx.toast.success("Senha alterada com sucesso!")

    @rx.event
    def save_notification_settings(self, form_data: dict):
        self.push_notifications = form_data.get("push", False)
        self.email_notifications = form_data.get("email", False)
        self.sound_notifications = form_data.get("sound", False)
        self.silent_hours_start = form_data["silent_start"]
        self.silent_hours_end = form_data["silent_end"]
        yield rx.toast.success("Notificações salvas com sucesso!")

    @rx.event
    def save_theme_settings(self):
        yield rx.toast.success("Tema salvo com sucesso!")

    @rx.event
    def save_integrations(self, form_data: dict):
        self.notion_connected = form_data.get("notion", False)
        self.google_drive_connected = form_data.get("gdrive", False)
        self.slack_webhook_url = form_data["slack_webhook"]
        yield rx.toast.success("Integrações salvas com sucesso!")

    @rx.event
    def save_admin_settings(self, form_data: dict):
        self.session_expiration = int(form_data["session_expiration"])
        yield rx.toast.success("Configurações de administrador salvas!")