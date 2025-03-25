from .svg_element import SvgElement


class SvgTaskBox(SvgElement):
    """
    Class representing a box element in SVG.
    """

    def __init__(self, x: int, y: int):
        """
        Initialize a box element with a specific position.

        :param x: The x-coordinate of the box.
        :param y: The y-coordinate of the box.
        """
        attr = {"x": str(x), "y": str(y)}
        super().__init__(tag="rect", css_class="task_box", attr=attr)

    def set_position(self, x: int, y: int) -> None:
        """
        Sets the position of the box (updates x and y).

        :param x: The new x-coordinate of the box.
        :param y: The new y-coordinate of the box.
        """
        self.attr["x"] = str(x)
        self.attr["y"] = str(y)
        self.update_attribute()
