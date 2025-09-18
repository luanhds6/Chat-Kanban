import reflex as rx
from app.states.auth_state import AuthState, User
from app.components.users.user_modal import user_modal


def user_management_header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Gerenciar Usuários", class_name="text-3xl font-bold text-gray-900"
            ),
            rx.el.p(
                "Adicione, edite ou remova usuários da sua equipe.",
                class_name="text-gray-500 mt-1",
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("search", class_name="w-5 h-5 text-gray-400"),
                rx.el.input(
                    placeholder="Pesquisar por nome ou e-mail...",
                    on_change=AuthState.set_search_query,
                    class_name="bg-transparent focus:ring-0 border-none w-full placeholder-gray-400 text-sm",
                ),
                class_name="flex items-center gap-2 bg-white border border-gray-200 rounded-lg px-3 py-2 w-full max-w-xs shadow-sm",
            ),
            rx.el.select(
                rx.el.option("Todos os Setores", value="All"),
                rx.foreach(
                    AuthState.all_departments,
                    lambda dept: rx.el.option(dept, value=dept),
                ),
                on_change=AuthState.set_department_filter,
                class_name="bg-white border border-gray-200 rounded-lg px-3 py-2 text-sm font-medium text-gray-700 shadow-sm focus:ring-2 focus:ring-blue-500",
            ),
            rx.el.button(
                rx.icon("plus", class_name="w-5 h-5 mr-2"),
                "Adicionar Usuário",
                on_click=lambda: AuthState.open_user_modal(None),
                class_name="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors shadow-sm",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="flex justify-between items-center mb-8 px-8",
    )


def user_table_row(user: User) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.img(
                    src=f"https://api.dicebear.com/9.x/initials/svg?seed={user['full_name']}",
                    class_name="w-10 h-10 rounded-full",
                ),
                rx.el.div(
                    rx.el.p(user["full_name"], class_name="font-medium text-gray-800"),
                    rx.el.p(user["email"], class_name="text-sm text-gray-500"),
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            user["department"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
        ),
        rx.el.td(
            rx.el.span(
                user["role"],
                class_name=rx.cond(
                    user["role"] == "Admin",
                    "px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800",
                    "px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800",
                ),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    class_name=rx.cond(
                        user["online"],
                        "h-2.5 w-2.5 rounded-full bg-green-500 mr-2",
                        "h-2.5 w-2.5 rounded-full bg-gray-400 mr-2",
                    )
                ),
                rx.cond(user["online"], "Online", "Offline"),
                class_name="flex items-center text-sm text-gray-600",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    "Editar",
                    on_click=lambda: AuthState.open_user_modal(user["email"]),
                    class_name="text-blue-600 hover:text-blue-900 font-medium",
                ),
                rx.el.button(
                    "Excluir",
                    on_click=lambda: AuthState.delete_user(user["email"]),
                    class_name="text-red-600 hover:text-red-900 font-medium ml-4",
                ),
                class_name="text-right text-sm font-medium",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        class_name="hover:bg-gray-50",
    )


def user_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Nome",
                            scope="col",
                            class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Departamento",
                            scope="col",
                            class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Função",
                            scope="col",
                            class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Status",
                            scope="col",
                            class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(scope="col", class_name="relative px-6 py-3"),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(AuthState.filtered_users, user_table_row),
                    class_name="bg-white divide-y divide-gray-200",
                ),
                min_w="full",
            ),
            class_name="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8",
        ),
        class_name="flex flex-col px-8",
    )


def user_management_view() -> rx.Component:
    return rx.el.div(
        user_management_header(),
        user_table(),
        user_modal(),
        class_name="w-full h-full bg-gray-50 pt-8",
    )