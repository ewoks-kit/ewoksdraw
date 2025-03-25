from typing import Dict, List

from .svg_group import SvgGroup
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
        self.list_elements: List[SvgGroup] = []
        self.init_elements()
        super().__init__(self.list_elements)

    def init_elements(self) -> None:
        """
        Initialize the elements of the SvgTask, including the box and the title.
        """
        box = SvgTaskBox(x=100, y=100)
        text = SvgTaskTitle(text=self.params["title"], x=150, y=110)
        anchor = SvgTaskAnchorLink(cx=100, cy=150, radius=4)

        self.list_elements.append(box)
        self.list_elements.append(text)
        self.list_elements.append(anchor)
