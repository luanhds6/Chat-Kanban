import reflex as rx
from app.states.kanban_state import KanbanState
from app.states.auth_state import AuthState


def add_task_modal() -> rx.Component:
    return rx.el.dialog(
        rx.el.div(
            rx.el.form(
                rx.el.div(
                    rx.el.h2(
                        "Add New Task", class_name="text-2xl font-bold text-gray-900"
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="w-5 h-5"),
                        on_click=KanbanState.toggle_add_task_modal,
                        type="button",
                        class_name="p-1 rounded-full hover:bg-gray-100",
                    ),
                    class_name="flex justify-between items-center pb-4 mb-6 border-b",
                ),
                rx.el.div(
                    rx.el.label(
                        "Title",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        name="title",
                        placeholder="e.g., Finalize quarterly report",
                        required=True,
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Description",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.textarea(
                        name="description",
                        placeholder="Add more details about the task...",
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 h-24",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Assignee",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.select(
                            rx.foreach(
                                AuthState.users.values(),
                                lambda user: rx.el.option(
                                    user["full_name"], value=user["email"]
                                ),
                            ),
                            name="assignee",
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
                        ),
                        class_name="flex-1",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Due Date",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="date",
                            name="due_date",
                            required=True,
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
                        ),
                        class_name="flex-1",
                    ),
                    class_name="flex gap-4 mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Priority",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.select(
                            rx.el.option("Low", value="Low"),
                            rx.el.option("Medium", value="Medium"),
                            rx.el.option("High", value="High"),
                            name="priority",
                            default_value="Medium",
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
                        ),
                        class_name="flex-1",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Tags (comma-separated)",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            name="tags",
                            placeholder="UI/UX, Backend, High Priority",
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
                        ),
                        class_name="flex-1",
                    ),
                    class_name="flex gap-4 mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        type="button",
                        on_click=KanbanState.toggle_add_task_modal,
                        class_name="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg font-semibold hover:bg-gray-200 transition-colors w-full sm:w-auto",
                    ),
                    rx.el.button(
                        "Add Task",
                        type="submit",
                        class_name="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors w-full sm:w-auto",
                    ),
                    class_name="flex justify-end gap-3",
                ),
                on_submit=KanbanState.add_task,
                reset_on_submit=True,
            ),
            class_name="bg-white p-8 rounded-2xl shadow-2xl w-full max-w-2xl",
        ),
        open=KanbanState.show_add_task_modal,
        class_name="backdrop:bg-black/40 z-50",
    )