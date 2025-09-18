import reflex as rx
from typing import TypedDict, Literal
import re


class User(TypedDict):
    full_name: str
    email: str
    department: str
    password: str
    role: Literal["Admin", "Standard"]
    online: bool
    language: str
    timezone: str


class AuthState(rx.State):
    users: dict[str, User] = {
        "admin@example.com": {
            "full_name": "Admin User",
            "email": "admin@example.com",
            "department": "Management",
            "password": "Password123!",
            "role": "Admin",
            "online": True,
            "language": "Portugués (Brasil)",
            "timezone": "(GMT-03:00) Brasilía",
        },
        "jane.doe@example.com": {
            "full_name": "Jane Doe",
            "email": "jane.doe@example.com",
            "department": "Engineering",
            "password": "Password123!",
            "role": "Standard",
            "online": True,
            "language": "English (US)",
            "timezone": "(GMT-08:00) Pacific Time",
        },
        "john.smith@example.com": {
            "full_name": "John Smith",
            "email": "john.smith@example.com",
            "department": "Marketing",
            "password": "Password123!",
            "role": "Standard",
            "online": False,
            "language": "Portugués (Brasil)",
            "timezone": "(GMT-03:00) Brasilía",
        },
    }
    current_user_email: str = "admin@example.com"
    in_session: bool = True
    show_user_modal: bool = False
    modal_user_email: str | None = None
    modal_form_data: dict = {}
    search_query: str = ""
    department_filter: str = "All"

    @rx.var
    def current_user(self) -> User | None:
        return self.users.get(self.current_user_email)

    @rx.var
    def filtered_users(self) -> list[User]:
        def filter_func(user: User) -> bool:
            matches_search = (
                self.search_query.lower() in user["full_name"].lower()
                or self.search_query.lower() in user["email"].lower()
            )
            matches_department = (
                self.department_filter == "All"
                or user["department"] == self.department_filter
            )
            return matches_search and matches_department

        return sorted(
            [user for user in self.users.values() if filter_func(user)],
            key=lambda u: u["full_name"],
        )

    @rx.var
    def all_departments(self) -> list[str]:
        return sorted(list(set((user["department"] for user in self.users.values()))))

    def _validate_password(self, password: str) -> bool:
        if len(password) < 8:
            return False
        if not re.search("[A-Z]", password):
            return False
        if not re.search("[a-z]", password):
            return False
        if not re.search("[0-9]", password):
            return False
        return True

    @rx.event
    def sign_up(self, form_data: dict):
        email = form_data["email"].lower().strip()
        password = form_data["password"]
        confirm_password = form_data["confirm_password"]
        if not email.endswith("@example.com"):
            yield rx.toast.error("Use um e-mail corporativo válido (@example.com)")
            return
        if email in self.users:
            yield rx.toast.error("E-mail já cadastrado.")
            return
        if not self._validate_password(password):
            yield rx.toast.error(
                "A senha deve ter pelo menos 8 caracteres, uma maiúscula, uma minúscula e um número."
            )
            return
        if password != confirm_password:
            yield rx.toast.error("As senhas não coincidem.")
            return
        new_user: User = {
            "full_name": form_data["full_name"].strip(),
            "email": email,
            "department": form_data["department"].strip(),
            "password": password,
            "role": "Standard",
            "online": True,
        }
        self.users[email] = new_user
        self.current_user_email = email
        self.in_session = True
        yield rx.toast.success("Conta criada com sucesso!")
        return rx.redirect("/")

    @rx.event
    def sign_in(self, form_data: dict):
        email = form_data["email"].lower()
        if user := self.users.get(email):
            if user["password"] == form_data["password"]:
                self.current_user_email = email
                self.in_session = True
                user["online"] = True
                self.users[email] = user
                yield rx.toast.success(f"Bem-vindo de volta, {user['full_name']}!")
                return rx.redirect("/")
        self.in_session = False
        yield rx.toast.error("E-mail ou senha inválidos.")

    @rx.event
    def sign_out(self):
        if self.current_user:
            user = self.current_user
            user["online"] = False
            self.users[self.current_user_email] = user
        self.in_session = False
        self.current_user_email = ""
        return rx.redirect("/login")

    @rx.event
    def check_session(self):
        if not self.in_session:
            return rx.redirect("/login")

    def open_user_modal(self, email: str | None = None):
        self.modal_user_email = email
        if email and (user := self.users.get(email)):
            self.modal_form_data = {
                "full_name": user["full_name"],
                "email": user["email"],
                "department": user["department"],
                "role": user["role"],
                "password": "",
                "confirm_password": "",
            }
        else:
            self.modal_form_data = {}
        self.show_user_modal = True

    def close_user_modal(self):
        self.show_user_modal = False
        self.modal_user_email = None
        self.modal_form_data = {}

    @rx.event
    def handle_user_form_submit(self, form_data: dict):
        if self.modal_user_email:
            return AuthState.update_user(form_data)
        else:
            return AuthState.create_user(form_data)

    @rx.event
    def create_user(self, form_data: dict):
        email = form_data["email"].lower().strip()
        password = form_data["password"]
        confirm_password = form_data["confirm_password"]
        if not email.endswith("@example.com"):
            yield rx.toast.error("Use um e-mail corporativo válido (@example.com)")
            return
        if email in self.users:
            yield rx.toast.error("E-mail já cadastrado.")
            return
        if not password or not self._validate_password(password):
            yield rx.toast.error(
                "A senha deve ter pelo menos 8 caracteres, uma maiúscula, uma minúscula e um número."
            )
            return
        if password != confirm_password:
            yield rx.toast.error("As senhas não coincidem.")
            return
        new_user: User = {
            "full_name": form_data["full_name"].strip(),
            "email": email,
            "department": form_data["department"].strip(),
            "password": password,
            "role": form_data["role"],
            "online": False,
        }
        self.users[email] = new_user
        yield rx.toast.success(f"Usuário {new_user['full_name']} criado.")
        self.show_user_modal = False
        self.modal_user_email = None

    @rx.event
    def update_user(self, form_data: dict):
        if not self.modal_user_email:
            return
        user = self.users[self.modal_user_email]
        user["full_name"] = form_data["full_name"].strip()
        user["department"] = form_data["department"].strip()
        user["role"] = form_data["role"]
        password = form_data.get("password", "")
        if password:
            if not self._validate_password(password):
                yield rx.toast.error(
                    "A senha deve ter pelo menos 8 caracteres, uma maiúscula, uma minúscula e um número."
                )
                return
            if password != form_data.get("confirm_password"):
                yield rx.toast.error("As senhas não coincidem.")
                return
            user["password"] = password
        self.users[self.modal_user_email] = user
        yield rx.toast.success(f"Usuário {user['full_name']} atualizado.")
        self.show_user_modal = False
        self.modal_user_email = None

    @rx.event
    def delete_user(self, email: str):
        if email == self.current_user_email:
            yield rx.toast.error("Não é possível excluir a si mesmo.")
            return
        if email in self.users:
            del self.users[email]
            yield rx.toast.success(f"Usuário {email} excluído.")