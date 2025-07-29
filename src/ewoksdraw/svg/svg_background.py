from .svg_element import SvgElement


class SvgBackground(SvgElement):
    """
    Represents a background rectangle element in SVG.
    Color can be set using the ./css_styles/css_background.css
    style.
    """

    def __init__(self, width: float, height: float):
        attr = {
            "width": str(width),
            "height": str(height),
        }
        super().__init__(tag="rect", css_class="background", attr=attr)
