import reflex as rx
from app.states.auth_state import AuthState


def form_field(
    label: str,
    name: str,
    placeholder: str,
    field_type: str = "text",
    required: bool = True,
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        rx.el.input(
            name=name,
            placeholder=placeholder,
            type=field_type,
            required=required,
            default_value=AuthState.modal_form_data.get(name, ""),
            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
        ),
        class_name="mb-4",
    )


def user_modal() -> rx.Component:
    return rx.el.dialog(
        rx.el.div(
            rx.el.form(
                rx.el.div(
                    rx.el.h2(
                        rx.cond(
                            AuthState.modal_user_email,
                            "Editar Usuário",
                            "Adicionar Novo Usuário",
                        ),
                        class_name="text-2xl font-bold text-gray-900",
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="w-5 h-5"),
                        on_click=AuthState.close_user_modal,
                        type="button",
                        class_name="p-1 rounded-full hover:bg-gray-100",
                    ),
                    class_name="flex justify-between items-center pb-4 mb-6 border-b",
                ),
                form_field("Nome Completo", "full_name", "Jane Doe"),
                form_field(
                    "E-mail Corporativo",
                    "email",
                    "jane.doe@example.com",
                    field_type="email",
                    required=True,
                ),
                form_field("Setor/Departamento", "department", "Engenharia"),
                rx.el.div(
                    rx.el.label(
                        "Função",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.select(
                        rx.el.option("Padrão", value="Standard"),
                        rx.el.option("Admin", value="Admin"),
                        name="role",
                        default_value=AuthState.modal_form_data.get("role", "Standard"),
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(class_name="my-6 border-t"),
                form_field(
                    "Senha",
                    "password",
                    "Deixe em branco para não alterar",
                    field_type="password",
                    required=False,
                ),
                form_field(
                    "Confirmar Senha",
                    "confirm_password",
                    "Repita a nova senha",
                    field_type="password",
                    required=False,
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancelar",
                        type="button",
                        on_click=AuthState.close_user_modal,
                        class_name="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg font-semibold hover:bg-gray-200 transition-colors w-full",
                    ),
                    rx.el.button(
                        rx.cond(
                            AuthState.modal_user_email,
                            "Salvar Alterações",
                            "Criar Usuário",
                        ),
                        type="submit",
                        class_name="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors w-full",
                    ),
                    class_name="flex justify-end gap-3 mt-8",
                ),
                on_submit=AuthState.handle_user_form_submit,
                reset_on_submit=True,
            ),
            class_name="bg-white p-8 rounded-2xl shadow-2xl w-full max-w-lg",
        ),
        open=AuthState.show_user_modal,
        class_name="backdrop:bg-black/40 z-50",
    )