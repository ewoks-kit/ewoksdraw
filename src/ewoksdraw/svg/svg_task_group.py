from .svg_group import SvgGroup
from .svg_task import PortPosition
from .svg_task import SvgTask
from .svg_task import TaskSize

TaskSizes = dict[str, TaskSize]
TaskPortPositions = dict[str, list[PortPosition]]


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

    def extract_port_positions(self) -> TaskPortPositions:
        return {
            task_id: svg_task.get_port_positions()
            for task_id, svg_task in self._svg_tasks.items()
        }
