from typing import Optional

from ..utils.utils_tasks import get_task_config_param
from .svg_element import SvgElement


class SvgTaskBox(SvgElement):
    """
    Represents a box element in SVG.
    :param x: The x-coordinate of the box.
    :param y: The y-coordinate of the box.
    """

    def __init__(self, x: float, y: float):
        self._min_width = get_task_config_param("box/min_width")
        self._max_width = get_task_config_param("box/max_width")

        attr = {
            "x": str(x),
            "y": str(y),
            "width": str(self._min_width),
        }
        super().__init__(tag="rect", css_class="task_box", attr=attr)

    def set_size(
        self, width: Optional[float] = None, height: Optional[float] = None
    ) -> None:
        """
        Set the width and/or height of the box.

        :param width: New width to set. If None, width remains unchanged.
        :param height: New height to set. If None, height remains unchanged.
        """
        if width is not None:
            self.set_attr("width", str(width))
        if height is not None:
            self.set_attr("height", str(height))

    @property
    def width(self) -> float:
        width = float(self.get_attr("width") or "0")
        return width
