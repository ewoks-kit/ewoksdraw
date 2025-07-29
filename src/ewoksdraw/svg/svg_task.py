from ..config.constants import IO_INTER_IO_MARGIN
from ..config.constants import IO_TOP_MARGIN
from .svg_group import SvgGroup
from .svg_task_box import SvgTaskBox
from .svg_task_io import SvgTaskIOGroup
from .svg_task_line import SvgTaskLine
from .svg_task_title import SvgTaskTitle


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
        list_input_names: list[str],
        list_output_names: list[str],
    ):
        super().__init__()

        self._interspace_title_input = IO_TOP_MARGIN
        self._interspace_input_output = IO_INTER_IO_MARGIN
        self._title = SvgTaskTitle(text=task_name, x=0, y=0)
        self._box = SvgTaskBox(x=0, y=0)
        self._inputs = SvgTaskIOGroup(
            list_io=list_input_names, io_type="input", vertical_spacing=8
        )
        self._outputs = SvgTaskIOGroup(
            list_io=list_output_names, io_type="output", vertical_spacing=8
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
            self._box.set_size(width=target_width)

        elif target_width > self._box._max_width:

            self._box.set_size(width=self._box._max_width)

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

    def _scale_vertical(self):
        """
        Adjusts the vertical layout and sizes of elements within the task group.
        """

        total_height = (
            self._title.height
            + self._inputs.height
            + self._outputs.height
            + self._interspace_input_output
            + self._interspace_title_input
        )
        self._box.set_size(height=total_height)

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
