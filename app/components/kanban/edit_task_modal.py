import reflex as rx
from app.states.kanban_state import KanbanState, Task
from app.states.auth_state import AuthState


def form_group(label: str, children: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        children,
    )


def attachment_item(attachment_url: str) -> rx.Component:
    return rx.el.div(
        rx.icon("paperclip", class_name="w-4 h-4 text-gray-500"),
        rx.el.a(
            attachment_url.split("/")[-1],
            href=attachment_url,
            target="_blank",
            class_name="text-sm text-blue-600 hover:underline truncate",
        ),
        class_name="flex items-center gap-2 p-2 bg-gray-100 rounded-md",
    )


def comment_item(comment: dict) -> rx.Component:
    author_user = AuthState.users[comment["author"]]
    return rx.el.div(
        rx.el.img(
            src=f"https://api.dicebear.com/9.x/initials/svg?seed={author_user['full_name']}",
            class_name="w-8 h-8 rounded-full",
        ),
        rx.el.div(
            rx.el.p(
                author_user["full_name"],
                class_name="font-semibold text-sm text-gray-800",
            ),
            rx.el.p(comment["text"], class_name="text-sm text-gray-600"),
        ),
        class_name="flex items-start gap-3",
    )


def edit_task_modal() -> rx.Component:
    return rx.el.dialog(
        rx.cond(
            KanbanState.editing_task,
            rx.el.div(
                rx.el.form(
                    rx.el.div(
                        rx.el.h2(
                            "Edit Task", class_name="text-2xl font-bold text-gray-900"
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="w-5 h-5"),
                            on_click=KanbanState.close_edit_task_modal,
                            type="button",
                            class_name="p-1 rounded-full hover:bg-gray-100",
                        ),
                        class_name="flex justify-between items-center pb-4 mb-6 border-b",
                    ),
                    rx.el.div(
                        form_group(
                            "Title",
                            rx.el.input(
                                name="title",
                                default_value=KanbanState.editing_task["title"],
                                required=True,
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
                            ),
                        ),
                        form_group(
                            "Description",
                            rx.el.textarea(
                                name="description",
                                default_value=KanbanState.editing_task["description"],
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 h-24",
                            ),
                        ),
                        class_name="space-y-4",
                    ),
                    rx.el.div(
                        form_group(
                            "Assignee",
                            rx.el.select(
                                rx.foreach(
                                    AuthState.users.values(),
                                    lambda user: rx.el.option(
                                        user["full_name"], value=user["email"]
                                    ),
                                ),
                                name="assignee",
                                default_value=KanbanState.editing_task["assignee"],
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
                            ),
                        ),
                        form_group(
                            "Due Date",
                            rx.el.input(
                                type="date",
                                name="due_date",
                                default_value=KanbanState.editing_task["due_date"],
                                required=True,
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
                            ),
                        ),
                        class_name="grid grid-cols-2 gap-4 mt-4",
                    ),
                    rx.el.div(
                        form_group(
                            "Priority",
                            rx.el.select(
                                rx.el.option("Low", value="Low"),
                                rx.el.option("Medium", value="Medium"),
                                rx.el.option("High", value="High"),
                                name="priority",
                                default_value=KanbanState.editing_task["priority"],
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
                            ),
                        ),
                        form_group(
                            "Tags (comma-separated)",
                            rx.el.input(
                                name="tags",
                                default_value=KanbanState.editing_task["tags"].join(
                                    ", "
                                ),
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500",
                            ),
                        ),
                        class_name="grid grid-cols-2 gap-4 mt-4",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            type="button",
                            on_click=KanbanState.close_edit_task_modal,
                            class_name="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg font-semibold hover:bg-gray-200 transition-colors",
                        ),
                        rx.el.button(
                            "Save Changes",
                            type="submit",
                            class_name="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors",
                        ),
                        class_name="flex justify-end gap-3 mt-8 pt-4 border-t",
                    ),
                    on_submit=KanbanState.update_task,
                ),
                rx.el.div(
                    rx.el.h3("Activity", class_name="text-lg font-semibold mt-6 mb-4"),
                    rx.el.div(
                        rx.el.h4(
                            "Attachments", class_name="font-semibold text-sm mb-2"
                        ),
                        rx.el.div(
                            rx.foreach(
                                KanbanState.editing_task["attachments"], attachment_item
                            ),
                            class_name="grid grid-cols-2 gap-2 mb-4",
                        ),
                        rx.el.h4("Comments", class_name="font-semibold text-sm mb-2"),
                        rx.el.div(
                            rx.foreach(
                                KanbanState.editing_task["comments"], comment_item
                            ),
                            class_name="space-y-4 mb-4",
                        ),
                        rx.el.form(
                            rx.el.textarea(
                                name="comment_text",
                                placeholder="Add a comment...",
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 h-16",
                            ),
                            rx.el.button(
                                "Post Comment",
                                type="submit",
                                class_name="px-4 py-2 mt-2 bg-gray-200 text-gray-800 rounded-lg text-sm font-semibold hover:bg-gray-300",
                            ),
                            on_submit=KanbanState.add_comment,
                            reset_on_submit=True,
                            class_name="flex flex-col items-end",
                        ),
                    ),
                    class_name="w-96 pl-8 border-l ml-8",
                ),
                class_name="bg-white p-8 rounded-2xl shadow-2xl w-full max-w-5xl flex",
            ),
            rx.fragment(),
        ),
        open=KanbanState.show_edit_task_modal,
        class_name="backdrop:bg-black/40 z-50",
    )