import re

from reportlab.pdfbase.pdfmetrics import stringWidth

from .svg_element import SvgElement


class SvgText(SvgElement):
    """
    Represents a text element in an SVG document.
    :param text: The text content to be displayed.
    :param x: The new x-coordinate.
    :param y: The new y-coordinate.
    :param css_class: The CSS class to apply to the text element.
    """

    def __init__(self, text: str, x: int, y: int, css_class):
        attr = {
            "x": str(x),
            "y": str(y),
            "text-anchor": "start",
            "dominant-baseline": "middle",
            "font-size": "6px",
        }

        super().__init__(tag="text", css_class=css_class, attr=attr, text=text)

    def modify_text_to_fit_width(self, target_width, min_font_size=6):
        """
        Adjusts the font size and truncates the text to fit within a target width.
        """

        current_width = self.width

        while (target_width < current_width) and (self.font_size >= min_font_size):
            self.set_font_size(self.font_size - 1)
            current_width = self.width

        while target_width < current_width:
            self._truncate_text_by_one()
            current_width = self.width

    def set_font_size(self, font_size: float) -> None:
        self.set_attr("font-size", f"{font_size}px")

    def set_dominant_baseline(self, dominant_baseline: str) -> None:
        self.set_attr("dominant-baseline", dominant_baseline)

    def set_text_anchor(self, text_anchor: str) -> None:
        self.set_attr("text-anchor", text_anchor)

    @property
    def width(self) -> float:
        if self.text is not None:
            return self._compute_text_width(self.text, self.font_size, self.font_name)
        else:
            return 0

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
        Extracts the font size from the 'style_element' attribute.

        :return: The extracted font size in pixels.
        """
        font_size_attr = self.get_attr("font-size")
        if font_size_attr is not None:
            font_size = float(font_size_attr.rstrip("px"))
        else:
            font_size = 0
        return font_size

    def _extract_font_name(self) -> str:
        """
        Extracts the font name from the style element's CSS content.

        :return: The extracted font name or "Helvetica" if not found.
        """

        if self.style_element is None:
            return "Helvetica"

        css_content = self.style_element.text
        match = re.search(r"font-family:\s*([\w\s-]+)", css_content or "")
        if match:
            font_name = match.group(1).strip()
        return font_name

    def _compute_text_width(self, text: str, font_size: float, font_name: str) -> float:
        """
        Compute the width of a given text string based on the specified font size and
        font name.

        :param text: The text string whose width is to be calculated.
        :param font_size: The size of the font to be used for the text.
        :param font_name: The name of the font to be used for the text.

        :return: The computed width of the text in the specified font and size.
        """

        return stringWidth(text, font_name, font_size)

    def _compute_text_height(self, font_size: float) -> float:
        """
        Compute the height of text in millimeters based on the given font size.

        :param font_size: The font size in points.

        :return: The height of the text in millimeters.
        """
        return font_size

    def _truncate_text_by_one(self):
        """
        Truncate the text by removing the last character and adding an ellipsis.
        """
        if self.text is not None : 
            self.text = self.text.rstrip("…").rstrip()[:-1].rstrip() + "…"
