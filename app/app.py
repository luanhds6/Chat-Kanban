import reflex as rx
import reflex_enterprise as rxe
from app.pages.login_page import login_page
from app.pages.signup_page import signup_page
from app.pages.dashboard_page import index
from app.states.auth_state import AuthState
from app.states.settings_state import SettingsState

app = rxe.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(
    index,
    route="/",
    on_load=[AuthState.check_session, SettingsState.load_user_settings],
)
app.add_page(login_page, route="/login")
app.add_page(signup_page, route="/signup")
app.add_page(index, title="ChatCompany")