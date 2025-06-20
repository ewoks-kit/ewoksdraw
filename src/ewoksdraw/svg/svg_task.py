from typing import Dict, List

from .svg_group import SvgElement, SvgGroup
from .svg_task_anchor_link import SvgTaskAnchorLink
from .svg_task_box import SvgTaskBox
from .svg_task_io import SvgTaskIO
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

        title = SvgTaskTitle(text=self.params["task_id"], x=0, y=0)
        box = SvgTaskBox(x=0, y=0)
        io1 = SvgTaskIO({"io_txt": "Input", "pos_y": 50})
        io2 = SvgTaskIO({"io_txt": "Input", "pos_y": 70})
        self.add_elements([title, io1, box, io2])
        self._scale_elements_size()

    def _scale_elements_size(self) -> None:
        """
        Scale the size of the elements to fit the text.
        """
        title = self.elements[0]
        box = self.elements[2]

        if isinstance(title, SvgTaskTitle) and isinstance(box, SvgTaskBox):

            target_width = int(title.width) + title.width_margin

            if (target_width >= box._min_width) and (target_width <= box._max_width):
                box.set_size(width=target_width)

            elif target_width > box._max_width:
                box.set_size(width=box._max_width)
                title.modify_text_to_fit_width(box._max_width)
