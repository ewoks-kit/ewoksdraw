from .svg_element import SvgElement


class SvgTaskLine(SvgElement):
    """
    Represents an SVG line element for task demarcation.

    This class extends SvgElement and initializes a line with specified
    start and end coordinates. It supports updating the coordinates
    after creation.

    :param x1: The x-coordinate of the start point of the line.
    :param y1: The y-coordinate of the start point of the line.
    :param x2: The x-coordinate of the end point of the line.
    :param y2: The y-coordinate of the end point of the line.
    """

    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
        Initializes the line element with the given start and end coordinates.

        Coordinates are converted to strings to match SVG attribute requirements.
        """
        attr = {"x1": str(x1), "y1": str(y1), "x2": str(x2), "y2": str(y2)}
        super().__init__(tag="line", css_class="task_line", attr=attr)

    def set_coordinates(self, x1: float, y1: float, x2: float, y2: float) -> None:
        """
        Updates the coordinates of the line element.

        The new coordinates replace the existing ones, and the SVG attributes
        are updated accordingly.

        :param x1: The new x-coordinate of the start point.
        :param y1: The new y-coordinate of the start point.
        :param x2: The new x-coordinate of the end point.
        :param y2: The new y-coordinate of the end point.
        """

        self.attr["x1"] = str(x1)
        self.attr["y1"] = str(y1)
        self.attr["x2"] = str(x2)
        self.attr["y2"] = str(y2)
        self.update_attribute()
