from typing import Dict, List

from .svg_group import SvgElement, SvgGroup
from .svg_task_anchor_link import SvgTaskAnchorLink
from .svg_task_box import SvgTaskBox
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
        self.params = params
        self.list_elements: List[SvgElement | SvgGroup] = []
        self._init_elements()
        super().__init__(self.list_elements)

    def _init_elements(self) -> None:
        """
        Initialize the elements of the SvgTask, including the box and the title.
        """

        text = SvgTaskTitle(text=self.params["task_id"], x=0, y=0)
        box = SvgTaskBox(x=0, y=0)

        # box.set_size(width=int(text.width), height=int(text.height))
        # print("text.width", text.width)
        # print("text.height", text.height)

        # anchor = SvgTaskAnchorLink(cx=100, cy=150, radius=4)

        self.list_elements.append(box)
        self.list_elements.append(text)
        # self.list_elements.append(anchor)
        self._scale_elements_size()

    def _scale_elements_size(self) -> None:
        """
        Scale the size of the elements to fit the text.
        """
        text = self.list_elements[1]
        box = self.list_elements[0]

        if isinstance(text, SvgTaskTitle) and isinstance(box, SvgTaskBox):

            target_width = int(text.width) + text.width_margin
            if (target_width >= box._min_width) and (target_width <= box._max_width):
                box.set_size(width=target_width)
            elif target_width > box._max_width:
                box.set_size(width=box._max_width)
                font_size = text.reduce_font_size_to_fit_width(box._max_width)
                print("font_size", font_size)
