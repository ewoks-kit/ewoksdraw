from .svg_element import SvgElement


class SvgTaskAnchorLink(SvgElement):
    """
    Represents an SVG circle element used as a task anchor link.
    :param cx: The x-coordinate of the center of the circle.
    :param cy: The y-coordinate of the center of the circle.
    :param radius: The radius of the circle.
    """

    def __init__(self, cx: float, cy: float, radius: float):
        attr = {"cx": str(cx), "cy": str(cy), "r": str(radius)}
        super().__init__(tag="circle", css_class="task_anchor_link", attr=attr)
