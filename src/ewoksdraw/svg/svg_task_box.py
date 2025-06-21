from typing import Optional

from .svg_element import SvgElement


class SvgTaskBox(SvgElement):
    """
    Represents a box element in SVG.

    :param x: The x-coordinate of the box.
    :param y: The y-coordinate of the box.
    """

    def __init__(self, x: float = 0, y: float = 0):
        """
        Initializes the SvgTaskBox with default min/max dimensions and position.

        :param x: Initial x-coordinate of the box. Defaults to 0.
        :param y: Initial y-coordinate of the box. Defaults to 0.
        """
        self._min_width = 20
        self._min_height = 200
        self._max_width = 75
        self._max_height = 400

        attr = {
            "x": str(x),
            "y": str(y),
            "width": str(self._min_width),
            "height": str(self._min_height),
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
            self.attr["width"] = str(width)
        if height is not None:
            self.attr["height"] = str(height)
        self.update_attribute()

    @property
    def width(self) -> float:
        return float(self.attr["width"])
