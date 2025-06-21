from typing import Optional

from .svg_element import SvgElement


class SvgTaskBox(SvgElement):
    """
    Class representing a box element in SVG.
    :param x: The x-coordinate of the box.
    :param y: The y-coordinate of the box.
    """

    def __init__(self, x: float = 0, y: float = 0):

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

    def set_position(
        self, x: Optional[float] = None, y: Optional[float] = None
    ) -> None:
        """
        Sets the position of the box (updates x and y).

        :param x: The new x-coordinate of the box.
        :param y: The new y-coordinate of the box.
        """
        if x is not None:
            self.attr["x"] = str(x)
        if y is not None:
            self.attr["y"] = str(y)
        self.update_attribute()

    def set_size(
        self, width: Optional[float] = None, height: Optional[float] = None
    ) -> None:
        """
        Sets the size of the box (updates width and height).

        :param width: The new width of the box.
        :param height: The new height of the box.
        """
        if width is not None:
            self.attr["width"] = str(width)
        if height is not None:
            self.attr["height"] = str(height)
        self.update_attribute()

    @property
    def width(self) -> float:
        return float(self.attr["width"])
