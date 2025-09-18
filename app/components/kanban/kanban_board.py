import reflex as rx
import reflex_enterprise as rxe
from app.states.kanban_state import KanbanState
from app.states.auth_state import AuthState
from app.components.kanban.kanban_card import kanban_card
from app.components.kanban.add_task_modal import add_task_modal
from app.components.kanban.edit_task_modal import edit_task_modal


@rx.memo
def kanban_column(title: str, tasks: list) -> rx.Component:
    count = tasks.length()
    drop_params = rxe.dnd.DropTarget.collected_params
    return rxe.dnd.drop_target(
        rx.el.div(
            rx.el.div(
                rx.el.h2(title, class_name="text-base font-semibold text-slate-700"),
                rx.el.span(
                    count,
                    class_name="px-2 py-0.5 text-xs font-bold text-slate-600 bg-slate-200 rounded-full",
                ),
                class_name="flex items-center justify-between px-4 py-3 border-b border-slate-200",
            ),
            rx.el.div(
                rx.foreach(tasks, lambda t: kanban_card(task=t)),
                class_name="p-4 flex flex-col gap-4 h-full overflow-y-auto",
            ),
            class_name=rx.cond(
                drop_params.is_over,
                "flex flex-col flex-shrink-0 w-80 bg-blue-50 rounded-xl border border-blue-400 transition-colors duration-300",
                "flex flex-col flex-shrink-0 w-80 bg-slate-100 rounded-xl border border-slate-200 transition-colors duration-300",
            ),
        ),
        accept=["task"],
        on_drop=lambda item: KanbanState.move_task(item, title),
        key=title,
    )


def kanban_board_header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Kanban Board", class_name="text-3xl font-bold text-slate-900"),
            rx.el.p(
                "Organize and track your team's work.", class_name="text-slate-500 mt-1"
            ),
        ),
        rx.el.div(
            rx.el.select(
                rx.el.option("All Assignees", value="All"),
                rx.foreach(
                    AuthState.users.values(),
                    lambda user: rx.el.option(user["full_name"], value=user["email"]),
                ),
                on_change=KanbanState.set_assignee_filter,
                default_value=KanbanState.assignee_filter,
                class_name="bg-white border border-slate-200 rounded-lg px-3 py-2 text-sm font-medium text-slate-700 shadow-sm focus:ring-2 focus:ring-blue-500",
            ),
            rx.el.select(
                rx.el.option("All Tags", value="All"),
                rx.foreach(
                    KanbanState.all_tags, lambda tag: rx.el.option(tag, value=tag)
                ),
                on_change=KanbanState.set_tag_filter,
                default_value=KanbanState.tag_filter,
                class_name="bg-white border border-slate-200 rounded-lg px-3 py-2 text-sm font-medium text-slate-700 shadow-sm focus:ring-2 focus:ring-blue-500",
            ),
            rx.el.button(
                rx.icon("plus", class_name="w-5 h-5 mr-2"),
                "Add Task",
                on_click=KanbanState.toggle_add_task_modal,
                class_name="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-all duration-200 shadow-sm transform hover:scale-105",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="flex justify-between items-center mb-8 px-8",
    )


def kanban_board() -> rx.Component:
    return rx.el.div(
        kanban_board_header(),
        rx.el.div(
            rx.foreach(
                KanbanState.columns,
                lambda col: kanban_column(
                    title=col, tasks=KanbanState.tasks_by_column[col]
                ),
            ),
            class_name="flex gap-6 p-8 overflow-x-auto",
        ),
        add_task_modal(),
        edit_task_modal(),
        class_name="flex flex-col h-full",
    )