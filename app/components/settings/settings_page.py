import reflex as rx
from app.states.settings_state import SettingsState
from app.states.auth_state import AuthState


def settings_card(
    icon: str,
    title: str,
    description: str,
    children: rx.Component,
    on_submit_handler: rx.event.EventHandler,
) -> rx.Component:
    return rx.el.form(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name="w-5 h-5 text-gray-500"),
                rx.el.div(
                    rx.el.h3(title, class_name="text-lg font-semibold text-gray-900"),
                    rx.el.p(description, class_name="text-sm text-gray-500"),
                ),
                class_name="flex items-start gap-3",
            ),
            class_name="p-6 border-b border-gray-200",
        ),
        rx.el.div(children, class_name="p-6"),
        rx.el.div(
            rx.el.button(
                "Salvar",
                type="submit",
                class_name="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors shadow-sm",
            ),
            class_name="flex justify-end p-6 bg-gray-50 border-t border-gray-200",
        ),
        on_submit=on_submit_handler,
        class_name="bg-white border border-gray-200 rounded-xl shadow-sm",
    )


def form_input(label: str, name: str, value: rx.Var, **kwargs) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        rx.el.input(
            name=name,
            default_value=value,
            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
            **kwargs,
        ),
    )


def form_select(
    label: str, name: str, value: rx.Var, options: list[str], **kwargs
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        rx.el.select(
            rx.foreach(options, lambda opt: rx.el.option(opt, value=opt)),
            name=name,
            default_value=value,
            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
            **kwargs,
        ),
    )


def form_switch(label: str, name: str, is_checked: rx.Var) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            rx.el.span(label, class_name="text-sm font-medium text-gray-900"),
            rx.el.input(
                type="checkbox",
                name=name,
                checked=is_checked,
                class_name="sr-only peer",
            ),
            rx.el.div(
                class_name="relative w-11 h-6 bg-gray-200 rounded-full peer peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"
            ),
            class_name="flex items-center justify-between cursor-pointer",
        )
    )


def profile_settings() -> rx.Component:
    return settings_card(
        "user-cog",
        "Perfil",
        "Edite suas informações pessoais.",
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Foto de Perfil",
                    class_name="block text-sm font-medium text-gray-700 mb-2",
                ),
                rx.el.div(
                    rx.el.img(
                        src=f"https://api.dicebear.com/9.x/initials/svg?seed={AuthState.current_user['full_name']}",
                        class_name="w-20 h-20 rounded-full",
                    ),
                    rx.el.button(
                        "Alterar Foto",
                        class_name="ml-4 px-3 py-1.5 text-sm font-semibold text-gray-700 bg-white border border-gray-300 rounded-lg shadow-sm hover:bg-gray-50",
                    ),
                    class_name="flex items-center",
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                form_input(
                    "Nome Completo", "full_name", AuthState.current_user["full_name"]
                ),
                form_input("Setor", "department", AuthState.current_user["department"]),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6",
            ),
            form_select(
                "Idioma",
                "language",
                SettingsState.language,
                ["Portugués (Brasil)", "English (US)"],
            ),
            form_select(
                "Fuso Horário",
                "timezone",
                SettingsState.timezone,
                ["(GMT-03:00) Brasilía", "(GMT-08:00) Pacific Time"],
            ),
            class_name="space-y-6",
        ),
        on_submit_handler=SettingsState.save_profile_settings,
    )


def password_settings() -> rx.Component:
    return settings_card(
        "lock-keyhole",
        "Alterar Senha",
        "Modifique sua senha de acesso.",
        rx.el.div(
            form_input(
                "Senha Atual",
                "current_password",
                "",
                type="password",
                placeholder="••••••••",
            ),
            form_input(
                "Nova Senha",
                "new_password",
                "",
                type="password",
                placeholder="••••••••",
            ),
            form_input(
                "Confirmar Nova Senha",
                "confirm_password",
                "",
                type="password",
                placeholder="••••••••",
            ),
            class_name="space-y-6",
        ),
        on_submit_handler=SettingsState.change_password,
    )


def notification_settings() -> rx.Component:
    return settings_card(
        "bell-ring",
        "Notificações",
        "Gerencie como você recebe notificações.",
        rx.el.div(
            form_switch("Notificações Push", "push", SettingsState.push_notifications),
            form_switch(
                "Notificações por E-mail", "email", SettingsState.email_notifications
            ),
            form_switch("Som de Mensagem", "sound", SettingsState.sound_notifications),
            rx.el.div(
                rx.el.p(
                    "Horário de Silâncio",
                    class_name="text-sm font-medium text-gray-900",
                ),
                rx.el.p(
                    "Desativar notificações durante este período.",
                    class_name="text-sm text-gray-500",
                ),
                class_name="mt-6 mb-2",
            ),
            rx.el.div(
                form_input(
                    "De", "silent_start", SettingsState.silent_hours_start, type="time"
                ),
                form_input(
                    "Até", "silent_end", SettingsState.silent_hours_end, type="time"
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="space-y-4",
        ),
        on_submit_handler=SettingsState.save_notification_settings,
    )


def theme_settings() -> rx.Component:
    colors = [
        "slate",
        "gray",
        "zinc",
        "neutral",
        "stone",
        "red",
        "orange",
        "amber",
        "yellow",
        "lime",
        "green",
        "emerald",
        "teal",
        "cyan",
        "sky",
        "blue",
        "indigo",
        "violet",
        "purple",
        "fuchsia",
        "pink",
        "rose",
    ]
    return settings_card(
        "palette",
        "Tema",
        "Personalize a aparância do aplicativo.",
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Modo de Cor", class_name="text-sm font-medium text-gray-900 mb-2"
                ),
                rx.el.div(
                    rx.el.button(
                        "Claro",
                        on_click=SettingsState.set_theme("light"),
                        class_name=rx.cond(
                            SettingsState.theme == "light",
                            "px-6 py-2 rounded-lg bg-blue-600 text-white font-semibold",
                            "px-6 py-2 rounded-lg bg-gray-100 text-gray-700 font-semibold",
                        ),
                    ),
                    rx.el.button(
                        "Escuro",
                        on_click=SettingsState.set_theme("dark"),
                        class_name=rx.cond(
                            SettingsState.theme == "dark",
                            "px-6 py-2 rounded-lg bg-blue-600 text-white font-semibold",
                            "px-6 py-2 rounded-lg bg-gray-100 text-gray-700 font-semibold",
                        ),
                    ),
                    class_name="flex items-center gap-2 p-1 bg-gray-200 rounded-xl w-fit",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Cor de Destaque",
                    class_name="text-sm font-medium text-gray-900 mb-2",
                ),
                rx.el.div(
                    rx.foreach(
                        colors,
                        lambda color: rx.el.button(
                            on_click=SettingsState.set_accent_color(color),
                            class_name=f"w-8 h-8 rounded-full bg-{color}-500 ring-2 ring-offset-2",
                            style={
                                "ringColor": rx.cond(
                                    SettingsState.accent_color == color,
                                    f"var(--{color}-500)",
                                    "transparent",
                                )
                            },
                        ),
                    ),
                    class_name="grid grid-cols-8 md:grid-cols-11 gap-2",
                ),
            ),
            class_name="space-y-6",
        ),
        on_submit_handler=SettingsState.save_theme_settings,
    )


def integration_settings() -> rx.Component:
    return settings_card(
        "plug-zap",
        "Integrações",
        "Conecte com outros aplicativos.",
        rx.el.div(
            form_switch(
                "Conectar com Notion", "notion", SettingsState.notion_connected
            ),
            form_switch(
                "Conectar com Google Drive",
                "gdrive",
                SettingsState.google_drive_connected,
            ),
            form_input(
                "URL do Webhook do Slack",
                "slack_webhook",
                SettingsState.slack_webhook_url,
                placeholder="https://hooks.slack.com/services/...",
            ),
            class_name="space-y-4",
        ),
        on_submit_handler=SettingsState.save_integrations,
    )


def admin_settings() -> rx.Component:
    return rx.cond(
        AuthState.current_user["role"] == "Admin",
        rx.el.div(
            settings_card(
                "shield-half",
                "Segurança",
                "Gerencie as configurações de segurança da equipe.",
                rx.el.div(
                    form_input(
                        "Tempo de expiração de sessão (horas)",
                        "session_expiration",
                        SettingsState.session_expiration,
                        type="number",
                    ),
                    class_name="space-y-6",
                ),
                on_submit_handler=SettingsState.save_admin_settings,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Estatísticas de Uso",
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    class_name="p-6 border-b border-gray-200",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Usuários Ativos",
                            class_name="text-sm font-medium text-gray-500",
                        ),
                        rx.el.p(
                            SettingsState.active_users_stat,
                            class_name="text-2xl font-bold text-gray-900",
                        ),
                        class_name="p-4 bg-gray-100 rounded-lg",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Mensagens Enviadas",
                            class_name="text-sm font-medium text-gray-500",
                        ),
                        rx.el.p(
                            SettingsState.messages_sent_stat,
                            class_name="text-2xl font-bold text-gray-900",
                        ),
                        class_name="p-4 bg-gray-100 rounded-lg",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Tarefas Criadas",
                            class_name="text-sm font-medium text-gray-500",
                        ),
                        rx.el.p(
                            SettingsState.tasks_created_stat,
                            class_name="text-2xl font-bold text-gray-900",
                        ),
                        class_name="p-4 bg-gray-100 rounded-lg",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-4 p-6",
                ),
                class_name="mt-8 bg-white border border-gray-200 rounded-xl shadow-sm",
            ),
            class_name="space-y-8",
        ),
        rx.fragment(),
    )


def settings_tabs() -> rx.Component:
    tabs = ["Perfil", "Notificações", "Tema", "Integrações", "Admin"]

    def tab_button(name: str) -> rx.Component:
        return rx.el.button(
            name,
            on_click=lambda: SettingsState.set_active_tab(name),
            class_name=rx.cond(
                SettingsState.active_tab == name,
                "px-4 py-2 text-sm font-semibold text-white bg-blue-600 rounded-lg",
                "px-4 py-2 text-sm font-semibold text-gray-600 hover:bg-gray-100 rounded-lg",
            ),
        )

    return rx.el.div(
        rx.foreach(
            tabs,
            lambda tab: rx.cond(
                (tab == "Admin") & (AuthState.current_user["role"] != "Admin"),
                rx.fragment(),
                tab_button(tab),
            ),
        ),
        class_name="flex items-center gap-2 mb-8",
    )


def settings_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Configurações", class_name="text-3xl font-bold text-gray-900"),
        settings_tabs(),
        rx.match(
            SettingsState.active_tab,
            (
                "Perfil",
                rx.el.div(
                    profile_settings(), password_settings(), class_name="space-y-8"
                ),
            ),
            ("Notificações", notification_settings()),
            ("Tema", theme_settings()),
            ("Integrações", integration_settings()),
            ("Admin", admin_settings()),
            rx.el.div("Selecione uma categoria"),
        ),
        class_name="h-full p-8 overflow-y-auto",
    )