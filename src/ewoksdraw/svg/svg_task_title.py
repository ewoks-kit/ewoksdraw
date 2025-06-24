from .svg_text import SvgText
from .utils_tasks import get_task_config_param

class SvgTaskTitle(SvgText):
    """
    Represents the title of a task in an SVG Task.

    :param text: The text content of the task title.
    :param x: The x-coordinate of the task title in the SVG canvas.
    :param y: The y-coordinate of the task title in the SVG canvas.
    """

    def __init__(self, text: str, x: int, y: int):
        self.vertical_margin: int = get_task_config_param("title/vertical_margin")
        self.horizontal_margin: int = get_task_config_param("title/horizontal_margin")
        super().__init__(text=text, x=x, y=y, css_class="task_title")
        self.set_dominant_baseline("hanging")
        self.set_text_anchor("middle")

    def modify_text_to_fit_width(self, target_width):
        super().modify_text_to_fit_width(target_width, min_font_size=10)

    @property
    def width(self) -> float:
        return super().width + self.horizontal_margin

    @property
    def height(self) -> float:
        return super().height + self.vertical_margin
