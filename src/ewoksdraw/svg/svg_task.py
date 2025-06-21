from .svg_group import SvgGroup
from .svg_task_box import SvgTaskBox
from .svg_task_io import SvgTaskIOGroup
from .svg_task_line import SvgTaskLine
from .svg_task_title import SvgTaskTitle


class SvgTask(SvgGroup):
    """
    Represents a task as an SVG group containing title, input/output groups, box, and line.

    The task includes a title, input/output labels, and a bounding box, with automatic
    layout scaling and positioning.

    :param name_task: The name of the task (displayed as title).
    :param list_inputs_names: List of input names for the task.
    :param list_outputs_names: List of output names for the task.
    """

    def __init__(
        self,
        name_task: str,
        list_inputs_names: list[str],
        list_outputs_names: list[str],
    ):
        """
        Initializes the SvgTask instance, sets task name, inputs and outputs, and
        initializes child elements.

        Calls layout scaling functions to position and size elements.
        """
        super().__init__()
        self.name_task = name_task
        self.list_inputs_names = list_inputs_names
        self.list_outputs_names = list_outputs_names
        self._init_elements()

    def _init_elements(self) -> None:
        """
        Initializes internal SVG elements: title, box, input/output groups, and line.

        Sets default font sizes and adds elements to the group.
        """
        self.spacer_title_input = 3
        self.spacer_input_output = 3

        self.title = SvgTaskTitle(text=self.name_task, x=0, y=0)
        self.title.set_font_size(6)

        self.box = SvgTaskBox(x=0, y=0)
        self.inputs = SvgTaskIOGroup(
            list_io=self.list_inputs_names, io_type="Input", vertical_spacing=8
        )

        self.outputs = SvgTaskIOGroup(
            list_io=self.list_outputs_names, io_type="Output", vertical_spacing=8
        )
        self.inputs.set_font_size(6)
        self.outputs.set_font_size(6)

        self.line_title = SvgTaskLine(x1=0, y1=0, x2=0, y2=0)

        self.add_elements(
            [self.title, self.box, self.inputs, self.outputs, self.line_title]
        )

        self._scale_horizontal_direction()
        self._scale_vertical_direction()

    def _scale_horizontal_direction(self) -> None:
        """
        Adjusts the widths of title, input/output groups, and box.

        Ensures the box width respects minimum and maximum bounds,
        modifying text or group sizes if necessary to fit the max width.

        Also translates outputs and centers the title horizontally.
        """
        target_width = max([self.title.width, self.inputs.width, self.outputs.width])

        if (target_width >= self.box._min_width) and (
            target_width <= self.box._max_width
        ):
            self.box.set_size(width=target_width)

        elif target_width > self.box._max_width:

            self.box.set_size(width=self.box._max_width)

            while target_width > self.box._max_width:

                target_width = max(
                    [self.title.width, self.inputs.width, self.outputs.width]
                )

                if target_width == self.title.width:
                    self.title.modify_text_to_fit_width(self.box._max_width)
                elif target_width == self.inputs.width:
                    self.inputs.modify_size_to_fit_width(self.box._max_width)
                    self.outputs.set_font_size(self.inputs.font_size)
                elif target_width == self.outputs.width:
                    self.outputs.modify_size_to_fit_width(self.box._max_width)
                    self.inputs.set_font_size(self.outputs.font_size)

        self.outputs.translate(x=self.box.width)
        self.title.set_position(x=self.box.width / 2.0)

    def _scale_vertical_direction(self):
        """
        Adjusts the vertical layout and sizes of elements within the task group.

        Sets total height for the bounding box based on summed heights and spacings,
        and positions title, inputs, outputs, and the connecting line vertically.
        """

        total_height = (
            self.title.height
            + self.inputs.height
            + self.outputs.height
            + self.spacer_title_input
            + self.spacer_input_output
        )
        self.box.set_size(height=total_height)

        pos = self.title.height_margin
        self.title.set_position(y=pos)
        pos += self.title.height + self.spacer_title_input
        self.inputs.translate(y=pos)
        pos += self.inputs.height + self.spacer_input_output
        self.outputs.translate(y=pos)

        self.line_title.set_coordinates(
            x1=0, y1=self.title.height, x2=self.box.width, y2=self.title.height
        )
