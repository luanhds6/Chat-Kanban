import reflex as rx
import reflex_enterprise as rxe
from app.states.kanban_state import KanbanState, Task
from app.states.auth_state import AuthState


def tag_component(tag: str, color: str) -> rx.Component:
    return rx.el.span(
        tag,
        class_name=f"px-2 py-1 text-xs font-medium rounded-full bg-{color}-100 text-{color}-700",
    )


def priority_indicator(priority: rx.Var[str]) -> rx.Component:
    return rx.el.div(
        class_name=rx.match(
            priority,
            ("High", "w-3 h-1.5 rounded-full bg-red-500"),
            ("Medium", "w-3 h-1.5 rounded-full bg-yellow-500"),
            ("Low", "w-3 h-1.5 rounded-full bg-green-500"),
            "w-3 h-1.5 rounded-full bg-gray-300",
        )
    )


@rx.memo
def kanban_card(task: Task) -> rx.Component:
    assignee_user = AuthState.users[task["assignee"]]
    draggable_params = rxe.dnd.Draggable.collected_params
    return rxe.dnd.draggable(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    priority_indicator(task["priority"]),
                    rx.el.h3(task["title"], class_name="font-semibold text-gray-800"),
                    class_name="flex items-center gap-2",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("copy", class_name="w-4 h-4"),
                        on_click=lambda: KanbanState.duplicate_task(task["id"]),
                        class_name="p-1 text-gray-400 hover:text-gray-600 rounded-md hover:bg-gray-100",
                    ),
                    rx.el.button(
                        rx.icon("trash-2", class_name="w-4 h-4"),
                        on_click=lambda: KanbanState.delete_task(task["id"]),
                        class_name="p-1 text-gray-400 hover:text-red-500 rounded-md hover:bg-red-50",
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex justify-between items-start",
            ),
            rx.el.p(
                task["description"],
                class_name="text-sm text-gray-600 mt-2 line-clamp-2",
            ),
            rx.el.div(
                rx.foreach(task["tags"], lambda tag: tag_component(tag, "blue")),
                class_name="flex flex-wrap gap-2 mt-3",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("paperclip", class_name="w-4 h-4 text-gray-500"),
                        rx.el.span(
                            task["attachments"].length(),
                            class_name="text-xs font-medium",
                        ),
                        class_name="flex items-center gap-1 text-gray-500",
                    ),
                    rx.el.div(
                        rx.icon("message-square", class_name="w-4 h-4 text-gray-500"),
                        rx.el.span(
                            task["comments"].length(), class_name="text-xs font-medium"
                        ),
                        class_name="flex items-center gap-1 text-gray-500",
                    ),
                    class_name="flex items-center gap-3",
                ),
                rx.el.div(
                    rx.el.img(
                        src=f"https://api.dicebear.com/9.x/initials/svg?seed={assignee_user['full_name']}",
                        class_name="w-6 h-6 rounded-full border-2 border-white",
                        title=assignee_user["full_name"],
                    )
                ),
                class_name="flex justify-between items-center mt-4",
            ),
            on_click=lambda: KanbanState.open_edit_task_modal(task["id"]),
            class_name="bg-white p-4 rounded-xl border border-gray-200 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-200 cursor-pointer",
        ),
        type="task",
        item={"id": task["id"]},
        key=task["id"].to_string(),
    )