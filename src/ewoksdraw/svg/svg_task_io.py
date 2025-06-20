from typing import Any, Dict, List

from .svg_group import SvgElement, SvgGroup
from .svg_task_anchor_link import SvgTaskAnchorLink
from .svg_text import SvgText


class SvgTaskIO(SvgGroup):

    def __init__(self, params: Dict[str, Any]):
        super().__init__()
        self.params = params
        self.init_elements()
        self.position_io()

    def init_elements(self) -> None:
        """
        Initialize the elements of the SvgTask, including the box and the title.
        """
        txt = SvgText(self.params["io_txt"], x=5, y=0, css_class="task_text_io")
        txt.set_font_size(8)
        anchor = SvgTaskAnchorLink(cx=0, cy=0, radius=2.5)

        self.add_elements([txt, anchor])

    def position_io(self) -> None:
        self.set_position(y=self.params["pos_y"])
