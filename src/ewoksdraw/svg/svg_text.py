import re

from reportlab.pdfbase.pdfmetrics import stringWidth

from .svg_element import SvgElement


class SvgText(SvgElement):
    """
    SvgText is a specialized SVG element representing a text element in an SVG document.

    This class provides functionality to create and manipulate text elements with specific
    content, position, and styling. It supports extracting font properties such as font size
    and font name from a CSS style element and calculating the width of the text based on
    these properties.

    Attributes:
        width (float): The computed width of the text based on its content, font size, and font name.
        font_name (str): The name of the font used for the text.
        font_size (float): The size of the font used for the text.

    Methods:
        set_position(x: int, y: int) -> None:
            Updates the position of the text element by setting new x and y coordinates.
    """

    def __init__(self, text: str, x: int, y: int, css_class):
        """
        Initialize a text element with specific content and position.

        :param text: The text content.
        :param x: The x-coordinate of the text.
        :param y: The y-coordinate of the text.
        """
        attr = {
            "x": str(x),
            "y": str(y),
            "text-anchor": "start",
            "dominant-baseline": "middle",
            "font-size": "6px",
        }

        super().__init__(tag="text", css_class=css_class, attr=attr, text=text)

    def set_font_size(self, font_size: float) -> None:
        self.attr["font-size"] = f"{font_size}px"
        self.update_attribute()

    def set_dominant_baseline(self, dominant_baseline: str) -> None:
        self.attr["dominant-baseline"] = dominant_baseline
        self.update_attribute()

    def set_text_anchor(self, text_anchor: str) -> None:
        self.attr["text-anchor"] = text_anchor
        self.update_attribute()

    @property
    def width(self) -> float:
        return self._compute_text_width(self.text, self.font_size, self.font_name)

    @property
    def height(self) -> float:
        return self._compute_text_height(self.font_size)

    @property
    def font_name(self) -> str:
        return self._extract_font_name()

    @property
    def font_size(self) -> float:
        return self._extract_font_size()

    def _extract_font_size(self) -> float:
        """
        Extracts the font size from the `style_element` attribute.
        This method parses the CSS content of the `style_element` to find the
        font size specified in pixels. If the font size is not found or the
        `style_element` is `None`, a default font size of 12 pixels is returned.
        Returns:
            float: The extracted font size in pixels.
        """

        if "font-size" in self.attr:
            return float(self.attr["font-size"].rstrip("px"))

    def _extract_font_name(self) -> str:
        """
        Extracts the font name from the style element's CSS content.

        This method attempts to retrieve the font-family property from the
        CSS content of the `style_element`. If the font-family is not found
        or the `style_element` is None, it defaults to "Arial".

        Returns:
            str: The extracted font name or "Arial" if not found.
        """

        if self.style_element is not None:
            css_content = self.style_element.text
            match = re.search(r"font-family:\s*([\w\s-]+)", css_content or "")
            if match:
                font_name = match.group(1).strip()
            else:
                font_name = "Helvetica"
        else:
            font_name = "Helvetica"
        return font_name

    def _compute_text_width(self, text: str, font_size: float, font_name: str) -> float:
        """
        Compute the width of a given text string based on the specified font size and font name.

        Args:
            text (str): The text string whose width is to be calculated.
            font_size (float): The size of the font to be used for the text.
            font_name (str): The name of the font to be used for the text.

        Returns:
            float: The computed width of the text in the specified font and size.
        """
        return stringWidth(text, font_name, font_size)

    def _compute_text_height(self, font_size: float) -> float:
        """
        Compute the height of text in millimeters based on the given font size.

        Args:
            font_size (float): The font size in points.

        Returns:
            float: The height of the text in millimeters.
        """
        return font_size

    def _truncate_text_by_one(self):

        self.set_text(self.text.rstrip("…").rstrip()[:-1].rstrip() + "…")

    def modify_text_to_fit_width(self, target_width, min_font_size=6):

        current_width = self.width

        while (target_width < current_width) and (self.font_size >= min_font_size):
            self.set_font_size(self.font_size - 1)
            current_width = self.width

        while target_width < current_width:
            self._truncate_text_by_one()
            current_width = self.width
