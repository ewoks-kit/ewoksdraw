from .svg_element import SvgElement


class SvgTaskLine(SvgElement):
    """
    Class representing a line element in SVG.
    """

    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        """
        Initialize a line object with the given start and end coordinates.

        Parameters:
            x1 (int): The x-coordinate of the start point of the line.
            y1 (int): The y-coordinate of the start point of the line.
            x2 (int): The x-coordinate of the end point of the line.
            y2 (int): The y-coordinate of the end point of the line.
        """

        attr = {"x1": str(x1), "y1": str(y1), "x2": str(x2), "y2": str(y2)}
        super().__init__(tag="line", css_class="task_line", attr=attr)

    def set_position(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
        Sets the position of the box (updates x and y).

        :param x: The new x-coordinate of the box.
        :param y: The new y-coordinate of the box.
        """
        self.attr["x1"] = str(x1)
        self.attr["y1"] = str(y1)
        self.attr["x2"] = str(x2)
        self.attr["y2"] = str(y2)
        self.update_attribute()
