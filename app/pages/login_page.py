import reflex as rx
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("message-square-more", class_name="w-10 h-10 text-blue-600"),
                rx.el.h1("TeamSync", class_name="text-3xl font-bold text-gray-900"),
                class_name="flex items-center justify-center gap-3 mb-8",
            ),
            rx.el.h2(
                "Sign in to your account",
                class_name="text-2xl font-bold text-center text-gray-900",
            ),
            rx.el.p(
                "Welcome back! Please enter your details.",
                class_name="text-center text-gray-500 mb-8",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Email", class_name="block text-sm font-medium text-gray-700"
                    ),
                    rx.el.input(
                        type="email",
                        name="email",
                        placeholder="you@example.com",
                        required=True,
                        class_name="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Password", class_name="block text-sm font-medium text-gray-700"
                    ),
                    rx.el.input(
                        type="password",
                        name="password",
                        placeholder="••••••••",
                        required=True,
                        class_name="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
                    ),
                    class_name="mb-6",
                ),
                rx.el.button(
                    "Sign In",
                    type="submit",
                    class_name="w-full px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors",
                ),
                on_submit=AuthState.sign_in,
                reset_on_submit=True,
            ),
            rx.el.p(
                "Don't have an account? ",
                rx.el.a(
                    "Sign Up",
                    href="/signup",
                    class_name="font-semibold text-blue-600 hover:underline",
                ),
                class_name="text-center text-sm text-gray-500 mt-6",
            ),
            class_name="w-full max-w-md bg-white p-8 rounded-2xl shadow-lg border border-gray-100",
        ),
        class_name="flex items-center justify-center min-h-screen bg-gray-50 font-['Inter']",
    )