from .svg_text import SvgText


class SvgTaskTitle(SvgText):
    """
    A class representing the title of a task in an SVG diagram.

    Inherits from:
        SvgText: A base class for SVG text elements.

    Attributes:
        text (str): The text content of the task title.
        x (int): The x-coordinate of the task title in the SVG canvas.
        y (int): The y-coordinate of the task title in the SVG canvas.
        css_class (str): The CSS class applied to the task title, defaulting to "task_title".

    Methods:
        Inherits all methods from the SvgText class.
    """

    def __init__(self, text: str, x: int, y: int):
        self.width_margin: int = 10
        self.height_margin: int = 10
        super().__init__(text=text, x=x, y=y, css_class="task_title")
