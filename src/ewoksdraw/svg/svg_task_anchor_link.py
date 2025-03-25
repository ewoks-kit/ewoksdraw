from .svg_element import SvgElement


class SvgTaskAnchorLink(SvgElement):

    def __init__(self, cx: int, cy: int, radius: int):

        attr = {"cx": str(cx), "cy": str(cy), "r": str(radius)}

        super().__init__(tag="circle", css_class="task_anchor_link", attr=attr)

    def set_position(self, x: int, y: int) -> None:

        self.attr["x"] = str(x)
        self.attr["y"] = str(y)
        self.update_attribute()
