from .svg_element import SvgElement


class SvgTaskTitle(SvgElement):
    """
    Class representing a text element in SVG.
    """

    def __init__(self, text: str, x: int, y: int):
        """
        Initialize a text element with specific content and position.

        :param text: The text content.
        :param x: The x-coordinate of the text.
        :param y: The y-coordinate of the text.
        """
        attr = {"x": str(x), "y": str(y)}
        super().__init__(tag="text", css_class="task_title", attr=attr, text=text)

    def set_position(self, x: int, y: int) -> None:
        """
        Sets the position of the text element (updates x and y).

        :param x: The new x-coordinate of the text.
        :param y: The new y-coordinate of the text.
        """
        self.attr["x"] = str(x)
        self.attr["y"] = str(y)
        self.update_attribute()
