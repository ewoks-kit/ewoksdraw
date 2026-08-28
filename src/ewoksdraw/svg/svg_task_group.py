from .svg_group import SvgGroup
from .svg_task import SvgTask
from .svg_task import TaskIOPosition
from .svg_task import TaskPosition
from .svg_task import TaskSize

TaskSizes = dict[str, TaskSize]
TaskPositions = list[TaskPosition]
TaskInputPositions = dict[str, list[TaskIOPosition]]
TaskOutputPositions = dict[str, list[TaskIOPosition]]


class SvgTaskGroup(SvgGroup[SvgTask]):
    """
    Represents a positioned collection of SvgTask elements.
    """

    def __init__(
        self,
        svg_tasks: dict[str, SvgTask],
        horizontal_gap: float = 5.0,
        group_id: str | None = None,
    ) -> None:
        super().__init__(group_id=group_id)
        self._svg_tasks = svg_tasks
        self._width = 0.0
        self.add_elements(svg_tasks.values())
        self._arrange_horizontally(gap=horizontal_gap)

    def _arrange_horizontally(self, gap: float) -> None:
        """
        Lays out the tasks left to right, each separated by `gap`.

        :param gap: The spacing before, between, and after the tasks.
        """
        if not self._svg_tasks:
            self._width = 0.0
            return

        x = gap
        for svg_task in self._svg_tasks.values():
            svg_task.translate(x=x, y=gap)
            x += svg_task.width + gap
        self._width = x

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        if not self._svg_tasks:
            return 0.0
        return max(svg_task.height for svg_task in self._svg_tasks.values())

    def extract_task_sizes(self) -> TaskSizes:
        return {
            task_id: TaskSize(width=svg_task.width, height=svg_task.height)
            for task_id, svg_task in self._svg_tasks.items()
        }

    def extract_input_positions(self) -> TaskInputPositions:
        return {
            task_id: svg_task.get_input_positions()
            for task_id, svg_task in self._svg_tasks.items()
        }

    def extract_output_positions(self) -> TaskOutputPositions:
        return {
            task_id: svg_task.get_output_positions()
            for task_id, svg_task in self._svg_tasks.items()
        }

    def set_task_positions(self, task_positions: TaskPositions) -> None:
        """Set each task's translation from absolute layout coordinates."""

        svg_task_ids = set(self._svg_tasks)
        positioned_task_ids = [position.name for position in task_positions]
        if svg_task_ids != set(positioned_task_ids) or len(positioned_task_ids) != len(
            svg_task_ids
        ):
            raise ValueError(
                f"task_positions {sorted(positioned_task_ids)} do not match SVG task "
                "ids "
                f"{sorted(svg_task_ids)}"
            )

        for position in task_positions:
            self._svg_tasks[position.name].set_translation(x=position.x, y=position.y)
