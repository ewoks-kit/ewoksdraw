from typing import Any, Dict, List

from .svg_group import SvgElement, SvgGroup
from .svg_task_anchor_link import SvgTaskAnchorLink
from .svg_text import SvgText


class SvgTaskIO(SvgGroup):

    def __init__(self, params: Dict[str, Any]):
        super().__init__()
        self.params = params
        self.anchor_text_spacing: int = 5
        self.init_elements()

    def init_elements(self) -> None:
        """
        Initialize the elements of the SvgTask, including the box and the title.
        """

        txt = SvgText(
            self.params["io_txt"],
            x=self.anchor_text_spacing,
            y=0,
            css_class="task_text_io",
        )
        anchor = SvgTaskAnchorLink(cx=0, cy=0, radius=2.0)

        if self.params["I/O"] == "Output":
            txt.set_text_anchor("end")
            txt.set_position(x=-self.anchor_text_spacing)

        self.add_elements([txt, anchor])

    def set_font_size(self, font_size: float):
        self.elements[0].set_font_size(font_size)

    def _truncate_text_by_one(self):
        self.elements[0]._truncate_text_by_one()

    @property
    def font_size(self) -> float:
        return self.elements[0].font_size

    @property
    def width(self) -> float:
        width_txt = self.elements[0].width
        return width_txt + (self.anchor_text_spacing) * 2

    @property
    def height(self) -> float:
        return self.elements[0].height


class SvgTaskIOGroup(SvgGroup):

    def __init__(self, list_io: list, params: Dict[str, Any]):
        super().__init__()
        self.params = params
        self.list_io = list_io
        self.vertical_spacing = 10
        self.init_elements()

    def init_elements(self) -> None:

        list_svg_io = []
        for i, io in enumerate(self.list_io):
            pos = i * self.vertical_spacing
            list_svg_io.append(SvgTaskIO({"io_txt": io, "pos_y": pos} | self.params))

        self.add_elements(list_svg_io)

    def set_font_size(self, font_size: float) -> None:
        for element in self.elements:
            element.set_font_size(font_size)

    def set_vertical_spacing(self, vertical_spacing):
        self.vertical_spacing = vertical_spacing
        for i, element in enumerate(self.elements):
            pos = i * vertical_spacing
            element.translate(y=pos)

    @property
    def width(self) -> float:
        list_width = []
        if self.elements:
            for element in self.elements:
                list_width.append(element.width)
            return max(list_width)
        else:
            return 0.0

    @property
    def height(self) -> float:
        return len(self.elements) * self.vertical_spacing

    @property
    def font_size(self) -> float:
        if self.elements:
            return self.elements[0].font_size
        else:
            return 0

    def _truncate_text_by_one(self):
        if self.elements:
            max_width = -1
            for element in self.elements:
                if element.width > max_width:
                    max_width = element.width
                    max_width_elem = element

            max_width_elem._truncate_text_by_one()

    def modify_size_to_fit_width(self, target_width, min_font_size=4):

        if self.elements:
            current_width = self.width

            while (target_width < current_width) and (self.font_size >= min_font_size):
                self.set_font_size(self.font_size - 1)
                current_width = self.width

            while target_width < current_width:
                self._truncate_text_by_one()
                current_width = self.width
