from typing import Dict, List

from .svg_group import SvgElement, SvgGroup
from .svg_task_anchor_link import SvgTaskAnchorLink
from .svg_task_box import SvgTaskBox
from .svg_task_io import SvgTaskIOGroup
from .svg_task_line import SvgTaskLine
from .svg_task_title import SvgTaskTitle


class SvgTask(SvgGroup):
    """
    SvgTask represents a task in SVG format, composed of a box and a title.
    """

    def __init__(self, params: Dict[str, str]):
        """
        Initialize the SvgTask with parameters.

        :param params: Dictionary containing parameters for the task, including the title.
        """
        super().__init__()
        self.params = params
        self._init_elements()

    def _init_elements(self) -> None:
        """
        Initialize the elements of the SvgTask, including the box and the title.
        """

        self.spacer_title_input = 3
        self.spacer_input_output = 3

        title = SvgTaskTitle(text=self.params["task_id"], x=0, y=0)
        title.set_font_size(6)

        box = SvgTaskBox(x=0, y=0)
        inputs = SvgTaskIOGroup(
            self.params["inputs"], {"I/O": "Input", "width_box": box.width}
        )

        outputs = SvgTaskIOGroup(
            self.params["outputs"], {"I/O": "Output", "width_box": box.width}
        )

        inputs.set_font_size(6)
        inputs.set_vertical_spacing(8)

        outputs.set_font_size(6)
        outputs.set_vertical_spacing(8)

        line_title = SvgTaskLine(0, 0, 0, 0)

        self.add_elements([title, box, inputs, outputs, line_title])

        self._scale_vertical_direction()
        self._scale_horizontal_direction()

    def _scale_vertical_direction(self) -> None:
        """
        Scale the size of the elements to fit the text.
        """
        title = self.elements[0]
        box = self.elements[1]
        inputs = self.elements[2]
        outputs = self.elements[3]

        target_width = max([title.width, inputs.width, outputs.width])

        if (target_width >= box._min_width) and (target_width <= box._max_width):
            box.set_size(width=target_width)

        elif target_width > box._max_width:

            box.set_size(width=box._max_width)

            while target_width > box._max_width:

                target_width = max([title.width, inputs.width, outputs.width])

                if target_width == title.width:
                    title.modify_text_to_fit_width(box._max_width)
                elif target_width == inputs.width:
                    inputs.modify_size_to_fit_width(box._max_width)
                    outputs.set_font_size(inputs.font_size)
                elif target_width == outputs.width:
                    outputs.modify_size_to_fit_width(box._max_width)
                    inputs.set_font_size(outputs.font_size)

        outputs.translate(x=box.width)
        title.set_position(x=box.width / 2)

    def _scale_horizontal_direction(self):

        title = self.elements[0]
        box = self.elements[1]
        inputs = self.elements[2]
        outputs = self.elements[3]
        line_title = self.elements[4]

        total_height = (
            title.height
            + inputs.height
            + outputs.height
            + self.spacer_title_input
            + self.spacer_input_output
        )

        box.set_size(height=total_height)

        pos = title.height_margin
        title.set_position(y=pos)
        pos += title.height + self.spacer_title_input
        inputs.translate(y=pos)
        pos += inputs.height + self.spacer_input_output
        outputs.translate(y=pos)

        line_title.set_position(x1=0, y1=title.height, x2=box.width, y2=title.height)

        print(total_height)
