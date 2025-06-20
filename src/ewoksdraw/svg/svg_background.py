from .svg_element import SvgElement


class SvgBackground(SvgElement):

    def __init__(self, width: int = 0, height: int = 0):
        """
        Initialize a box element with a specific position.

        :param x: The x-coordinate of the box.
        :param y: The y-coordinate of the box.
        """

        attr = {
            "width": str(width),
            "height": str(height),
        }

        super().__init__(tag="rect", css_class="background", attr=attr)

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
