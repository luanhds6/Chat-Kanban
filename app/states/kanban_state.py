import reflex as rx
from typing import TypedDict, Literal
import datetime


class Comment(TypedDict):
    author: str
    text: str
    timestamp: str


class HistoryLog(TypedDict):
    user: str
    action: str
    timestamp: str


class Task(TypedDict):
    id: int
    title: str
    description: str
    assignee: str
    due_date: str
    tags: list[str]
    status: Literal["To Do", "In Progress", "Done"]
    priority: Literal["Low", "Medium", "High"]
    attachments: list[str]
    comments: list[Comment]
    history: list[HistoryLog]


class KanbanState(rx.State):
    tasks: list[Task] = [
        {
            "id": 1,
            "title": "Design new landing page",
            "description": "Create mockups and wireframes for the new V2 landing page.",
            "assignee": "jane.doe@example.com",
            "due_date": "2024-08-15",
            "tags": ["UI/UX", "High Priority"],
            "status": "In Progress",
            "priority": "High",
            "attachments": ["/placeholder.svg"],
            "comments": [
                {
                    "author": "admin@example.com",
                    "text": "Let's use a blue color scheme.",
                    "timestamp": "2024-08-01 10:00",
                }
            ],
            "history": [
                {
                    "user": "admin@example.com",
                    "action": "Created task",
                    "timestamp": "2024-07-30 09:00",
                }
            ],
        },
        {
            "id": 2,
            "title": "Develop authentication flow",
            "description": "Implement JWT-based authentication for the backend API.",
            "assignee": "jane.doe@example.com",
            "due_date": "2024-08-20",
            "tags": ["Backend", "Security"],
            "status": "In Progress",
            "priority": "High",
            "attachments": [],
            "comments": [],
            "history": [],
        },
        {
            "id": 3,
            "title": "Setup CI/CD pipeline",
            "description": "Configure GitHub Actions for automated testing and deployment.",
            "assignee": "admin@example.com",
            "due_date": "2024-08-10",
            "tags": ["DevOps"],
            "status": "Done",
            "priority": "Medium",
            "attachments": [],
            "comments": [],
            "history": [],
        },
        {
            "id": 4,
            "title": "Write API documentation",
            "description": "Use Swagger/OpenAPI to document all API endpoints.",
            "assignee": "john.smith@example.com",
            "due_date": "2024-08-25",
            "tags": ["Documentation"],
            "status": "To Do",
            "priority": "Medium",
            "attachments": [],
            "comments": [],
            "history": [],
        },
        {
            "id": 5,
            "title": "Plan Q4 marketing campaign",
            "description": "Outline strategy, budget, and KPIs for the upcoming quarter.",
            "assignee": "john.smith@example.com",
            "due_date": "2024-09-01",
            "tags": ["Marketing", "Strategy"],
            "status": "To Do",
            "priority": "Low",
            "attachments": [],
            "comments": [],
            "history": [],
        },
    ]
    columns: list[Literal["To Do", "In Progress", "Done"]] = [
        "To Do",
        "In Progress",
        "Done",
    ]
    show_add_task_modal: bool = False
    show_edit_task_modal: bool = False
    editing_task_id: int | None = None
    assignee_filter: str = "All"
    tag_filter: str = "All"

    @rx.var
    def editing_task(self) -> Task | None:
        if self.editing_task_id is None:
            return None
        for task in self.tasks:
            if task["id"] == self.editing_task_id:
                return task
        return None

    @rx.var
    def all_tags(self) -> list[str]:
        tags = set()
        for task in self.tasks:
            for tag in task["tags"]:
                tags.add(tag)
        return sorted(list(tags))

    @rx.var
    def filtered_tasks(self) -> list[Task]:
        def filter_func(task: Task) -> bool:
            matches_assignee = (
                self.assignee_filter == "All"
                or task["assignee"] == self.assignee_filter
            )
            matches_tag = self.tag_filter == "All" or self.tag_filter in task["tags"]
            return matches_assignee and matches_tag

        return [task for task in self.tasks if filter_func(task)]

    @rx.var
    def tasks_by_column(self) -> dict[str, list[Task]]:
        tasks_by_col = {col: [] for col in self.columns}
        for task in self.filtered_tasks:
            if task["status"] in tasks_by_col:
                tasks_by_col[task["status"]].append(task)
        return tasks_by_col

    def toggle_add_task_modal(self):
        self.show_add_task_modal = not self.show_add_task_modal

    def open_edit_task_modal(self, task_id: int):
        self.editing_task_id = task_id
        self.show_edit_task_modal = True

    def close_edit_task_modal(self):
        self.show_edit_task_modal = False
        self.editing_task_id = None

    async def _log_history(self, task_id: int, action: str):
        from app.states.auth_state import AuthState

        auth_state = await self.get_state(AuthState)
        user_email = auth_state.current_user_email
        log = HistoryLog(
            user=user_email,
            action=action,
            timestamp=datetime.datetime.now().isoformat(),
        )
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                self.tasks[i]["history"].append(log)
                break

    @rx.event
    async def add_task(self, form_data: dict):
        new_id = max((t["id"] for t in self.tasks)) + 1 if self.tasks else 1
        new_task: Task = {
            "id": new_id,
            "title": form_data["title"],
            "description": form_data["description"],
            "assignee": form_data["assignee"],
            "due_date": form_data["due_date"],
            "priority": form_data["priority"],
            "tags": [tag.strip() for tag in form_data["tags"].split(",")]
            if form_data["tags"]
            else [],
            "status": "To Do",
            "attachments": [],
            "comments": [],
            "history": [],
        }
        self.tasks.append(new_task)
        await self._log_history(new_id, "Created task")
        self.show_add_task_modal = False
        yield rx.toast.success(f"Task '{new_task['title']}' added.")

    @rx.event
    async def move_task(self, task_info: dict, new_status: str):
        task_id = task_info["item"]["id"]
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                old_status = task["status"]
                if old_status != new_status:
                    self.tasks[i]["status"] = new_status
                    await self._log_history(
                        task_id, f"Moved from {old_status} to {new_status}"
                    )
                    yield rx.toast.info(f"Task moved to {new_status}")
                return

    @rx.event
    async def update_task(self, form_data: dict):
        if self.editing_task_id is None:
            return
        for i, task in enumerate(self.tasks):
            if task["id"] == self.editing_task_id:
                self.tasks[i]["title"] = form_data["title"]
                self.tasks[i]["description"] = form_data["description"]
                self.tasks[i]["assignee"] = form_data["assignee"]
                self.tasks[i]["due_date"] = form_data["due_date"]
                self.tasks[i]["priority"] = form_data["priority"]
                self.tasks[i]["tags"] = (
                    [tag.strip() for tag in form_data["tags"].split(",")]
                    if form_data["tags"]
                    else []
                )
                await self._log_history(self.editing_task_id, "Updated task details")
                yield rx.toast.success("Task updated.")
                self.close_edit_task_modal()
                return

    @rx.event
    async def delete_task(self, task_id: int):
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        yield rx.toast.error("Task deleted.")

    @rx.event
    async def duplicate_task(self, task_id: int):
        for task in self.tasks:
            if task["id"] == task_id:
                new_id = max((t["id"] for t in self.tasks)) + 1 if self.tasks else 1
                new_task = task.copy()
                new_task["id"] = new_id
                new_task["title"] = f"{task['title']} (Copy)"
                new_task["history"] = []
                self.tasks.append(new_task)
                await self._log_history(new_id, "Created task from duplicate")
                yield rx.toast.info(f"Task '{task['title']}' duplicated.")
                return

    @rx.event
    async def add_comment(self, form_data: dict):
        if self.editing_task_id is None or not form_data["comment_text"].strip():
            return
        from app.states.auth_state import AuthState

        auth_state = await self.get_state(AuthState)
        for i, task in enumerate(self.tasks):
            if task["id"] == self.editing_task_id:
                new_comment = {
                    "author": auth_state.current_user_email,
                    "text": form_data["comment_text"],
                    "timestamp": datetime.datetime.now().isoformat(),
                }
                self.tasks[i]["comments"].append(new_comment)
                await self._log_history(self.editing_task_id, "Added a comment")
                yield rx.toast.success("Comment added.")
                return

    @rx.var
    def due_today_count(self) -> int:
        today = datetime.date.today().isoformat()
        return sum(
            (
                1
                for task in self.tasks
                if task["due_date"] == today and task["status"] != "Done"
            )
        )