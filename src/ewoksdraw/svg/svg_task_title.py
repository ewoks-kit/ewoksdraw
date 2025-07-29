from ..config.constants import TITLE_HORIZONTAL_MARGIN
from ..config.constants import TITLE_MIN_FONT_SIZE
from ..config.constants import TITLE_TARGET_FONT_SIZE
from ..config.constants import TITLE_VERTICAL_MARGIN
from .svg_text import SvgText


class SvgTaskTitle(SvgText):
    """
    Represents the title of a task in an SVG Task.

    :param text: The text content of the task title.
    :param x: The x-coordinate of the task title in the SVG canvas.
    :param y: The y-coordinate of the task title in the SVG canvas.
    """

    def __init__(self, text: str, x: int, y: int):

        self.vertical_margin: int = TITLE_VERTICAL_MARGIN
        self.horizontal_margin: int = TITLE_HORIZONTAL_MARGIN
        super().__init__(text=text, x=x, y=y, css_class="task_title")
        self.set_dominant_baseline("hanging")
        self.set_text_anchor("middle")
        self.set_font_size(TITLE_TARGET_FONT_SIZE)

    def modify_text_to_fit_width(self, target_width: float) -> None:
        """
        Change the text font size to fit task box width.
        Will crop the title string if min_font_size is reach
        :param target_width: The x-coordinate of the task title in the SVG canvas.
        """

        min_font_size = TITLE_MIN_FONT_SIZE

        super().modify_text_to_fit_width(target_width, min_font_size=min_font_size)

    @property
    def width(self) -> float:
        return super().width + self.horizontal_margin

    @property
    def height(self) -> float:
        return super().height + self.vertical_margin
