from .svg_element import SvgElement


class SvgTaskBox(SvgElement):
    """
    Class representing a box element in SVG.
    """

    def __init__(self, x: int = 0, y: int = 0):
        """
        Initialize a box element with a specific position.

        :param x: The x-coordinate of the box.
        :param y: The y-coordinate of the box.
        """

        self._min_width = 100
        self._min_height = 100
        self._max_width = 200
        self._max_height = 200

        attr = {
            "x": str(x),
            "y": str(y),
            "width": str(self._min_width),
            "height": str(self._min_height),
        }
        super().__init__(tag="rect", css_class="task_box", attr=attr)

    def set_position(self, x: int | None = None, y: int | None = None) -> None:
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

    def set_size(self, width: int | None = None, height: int | None = None) -> None:
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
