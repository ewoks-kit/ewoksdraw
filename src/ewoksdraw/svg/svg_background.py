from typing import Optional

from .svg_element import SvgElement


class SvgBackground(SvgElement):
    """
    Represents a background rectangle element in SVG.

    :param width: The width of the background rectangle.
    :param height: The height of the background rectangle.
    """

    def __init__(self, width: float = 0, height: float = 0):
        """
        Initialize the background rectangle with specified width and height.

        :param width: Width of the background. Defaults to 0.
        :param height: Height of the background. Defaults to 0.
        """

        attr = {
            "width": str(width),
            "height": str(height),
        }

        super().__init__(tag="rect", css_class="background", attr=attr)
