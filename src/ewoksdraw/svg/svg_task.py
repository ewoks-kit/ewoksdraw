from typing import NamedTuple

from ..config.constants import IO_INTER_IO_MARGIN
from ..config.constants import IO_TOP_MARGIN
from .svg_group import SvgGroup
from .svg_task_box import SvgTaskBox
from .svg_task_io import SvgTaskIOGroup
from .svg_task_line import SvgTaskLine
from .svg_task_title import SvgTaskTitle


class TaskSize(NamedTuple):
    width: float
    height: float


class PortPosition(NamedTuple):
    id: str
    x: float
    y: float


class SvgTask(SvgGroup):
    """
    Represents a task as an SVG group containing title, input/output groups, box, and
    line.

    The task includes a title, input/output labels, bounding box and and one demarcation
    line, with automatic layout scaling and positioning.

    :param task_name: The name of the task (displayed as title).
    :param list_input_names: List of input names for the task.
    :param list_output_names: List of output names for the task.
    """

    def __init__(
        self,
        task_name: str,
        input_names: list[str],
        output_names: list[str],
    ):
        super().__init__(group_id=task_name)

        self._task_name = task_name
        self._interspace_title_input = IO_TOP_MARGIN
        self._interspace_input_output = IO_INTER_IO_MARGIN
        self._title = SvgTaskTitle(text=task_name, x=0, y=0)
        self._box = SvgTaskBox(x=0, y=0)
        self._inputs = SvgTaskIOGroup(
            list_io=input_names, io_type="input", vertical_spacing=8
        )
        self._outputs = SvgTaskIOGroup(
            list_io=output_names, io_type="output", vertical_spacing=8
        )
        self._line_title = SvgTaskLine(x1=0, y1=0, x2=0, y2=0)

        self._init_elements()

    def _init_elements(self) -> None:
        """
        Initializes the SVG task elements, setting their sizes and positions.
        """
        self.add_elements(
            [self._title, self._box, self._inputs, self._outputs, self._line_title]
        )

        self._scale_horizontal()
        self._scale_vertical()

    def _scale_horizontal(self) -> None:
        """
        Adjusts the widths of title, input/output groups, and box.

        """

        target_width = max([self._title.width, self._inputs.width, self._outputs.width])
        # If the box width is within the defined min and max bounds
        if (target_width >= self._box._min_width) and (
            target_width <= self._box._max_width
        ):
            self._box.set_width(target_width)

        elif target_width > self._box._max_width:
            self._box.set_width(self._box._max_width)

            max_iterations = 50
            iteration = 0

            while target_width > self._box._max_width and iteration < max_iterations:
                iteration += 1
                target_width = max(
                    [self._title.width, self._inputs.width, self._outputs.width]
                )

                if target_width == self._title.width:
                    self._title.modify_text_to_fit_width(self._box._max_width)
                elif target_width == self._inputs.width:
                    self._inputs.decrease_size_to_fit_width(self._box._max_width)
                    self._outputs.set_font_size(self._inputs.font_size)
                elif target_width == self._outputs.width:
                    self._outputs.decrease_size_to_fit_width(self._box._max_width)
                    self._inputs.set_font_size(self._outputs.font_size)

        self._outputs.translate(x=self._box.width)
        self._title.set_position(x=self._box.width / 2.0)

    def _scale_vertical(self) -> None:
        """
        Adjusts the vertical layout and sizes of elements within the task group.
        """

        self._box.set_height(self.height)

        self._title.set_position(y=self._title.vertical_margin // 2)

        pos = self._title.height + self._interspace_title_input
        self._inputs.translate(y=pos)
        pos += self._inputs.height + self._interspace_input_output
        self._outputs.translate(y=pos)

        self._line_title.set_coordinates(
            x1=0,
            y1=self._title.height - self._title.vertical_margin // 2,
            x2=self._box.width,
            y2=self._title.height - self._title.vertical_margin // 2,
        )

    @property
    def width(self) -> float:
        return self._box.width

    @property
    def height(self) -> float:
        return (
            self._title.height
            + self._inputs.height
            + self._outputs.height
            + self._interspace_input_output
            + self._interspace_title_input
        )

    def get_port_positions(self) -> list[PortPosition]:
        """Return task-relative ports position as ``[PortPosition(id, x, y), ...]``."""
        io_positions: list[PortPosition] = []

        for group in (self._inputs, self._outputs):
            for io in group.elements:
                port_id = f"{self._task_name}.{io._io_type}.{io.txt._text}"
                x = group._translation.x + io._translation.x
                y = group._translation.y + io._translation.y

                io_positions.append(PortPosition(id=port_id, x=x, y=y))

        return io_positions

    # def input_port_id(self, input_name: str) -> str:
    #     return f"{self._task_name}.inputs.{input_name}"

    # def output_port_id(self, output_name: str) -> str:
    #     return f"{self._task_name}.outputs.{output_name}"

    # def input_port_position(self, input_name: str) -> dict:
    #     index = self._input_names.index(input_name)
    #     return {
    #         "x": 0,
    #         "y": self._inputs_y + index * self._inputs._vertical_spacing,
    #     }

    # def output_port_position(self, output_name: str) -> dict:
    #     index = self._output_names.index(output_name)
    #     return {
    #         "x": self.width,
    #         "y": self._outputs_y + index * self._outputs._vertical_spacing,
    #     }

    # def elk_ports(self) -> list[dict]:
    #     ports = []
    #     port_size = 0

    #     for index, input_name in enumerate(self._input_names):
    #         position = self.input_port_position(input_name)
    #         ports.append(
    #             {
    #                 "id": self.input_port_id(input_name),
    #                 "x": position["x"],
    #                 "y": position["y"],
    #                 "width": port_size,
    #                 "height": port_size,
    #                 "layoutOptions": {
    #                     "org.eclipse.elk.port.side": "WEST",
    #                     "org.eclipse.elk.port.index": index,
    #                     "org.eclipse.elk.port.borderOffset": 0,
    #                 },
    #             }
    #         )

    #     for index, output_name in enumerate(self._output_names):
    #         position = self.output_port_position(output_name)
    #         ports.append(
    #             {
    #                 "id": self.output_port_id(output_name),
    #                 "x": position["x"],
    #                 "y": position["y"],
    #                 "width": port_size,
    #                 "height": port_size,
    #                 "layoutOptions": {
    #                     "org.eclipse.elk.port.side": "EAST",
    #                     "org.eclipse.elk.port.index": index,
    #                     "org.eclipse.elk.port.borderOffset": 0,
    #                 },
    #             }
    #         )

    #     return ports
