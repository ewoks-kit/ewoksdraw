from typing import Dict, List

from .svg_group import SvgElement, SvgGroup
from .svg_task_anchor_link import SvgTaskAnchorLink
from .svg_task_box import SvgTaskBox
from .svg_task_io import SvgTaskIOGroup
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

        print(self.params)

        title = SvgTaskTitle(text=self.params["task_id"], x=0, y=0)
        box = SvgTaskBox(x=0, y=0)
        inputs = SvgTaskIOGroup(
            self.params["inputs"], {"I/O": "Input", "width_box": box.width}
        )

        outputs = SvgTaskIOGroup(
            self.params["outputs"], {"I/O": "Output", "width_box": box.width}
        )

        inputs.translate(y=20)
        inputs.set_font_size(10)
        inputs.set_vertical_spacing(10)

        outputs.translate(y=80)
        outputs.set_font_size(10)
        outputs.set_vertical_spacing(10)

        self.add_elements([title, box, inputs, outputs])

        self._scale_elements_size()

    def _scale_elements_size(self) -> None:
        """
        Scale the size of the elements to fit the text.
        """
        title = self.elements[0]
        box = self.elements[1]
        inputs = self.elements[2]
        outputs = self.elements[3]

        target_width = max([title.width, inputs.width])

        if (target_width >= box._min_width) and (target_width <= box._max_width):
            box.set_size(width=target_width)

        elif target_width > box._max_width:
            box.set_size(width=box._max_width)
            if target_width == title.width:
                title.modify_text_to_fit_width(box._max_width)
            elif target_width == inputs.width:
                inputs.modify_size_to_fit_width(box._max_width)

        outputs.translate(x=box.width)
