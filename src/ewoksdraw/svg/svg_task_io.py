from typing import Literal

from ..utils.utils_tasks import get_task_config_param
from .svg_group import SvgGroup
from .svg_task_anchor_link import SvgTaskAnchorLink
from .svg_text import SvgText


class SvgTaskIO(SvgGroup):
    """
    Represents a single SVG task input or output element with text and an anchor link.

    :param _io_txt: The label text for the IO element.
    :param _io_type: The type of IO, typically "Input" or "Output".
    """

    def __init__(self, io_txt: str, io_type: str):
        super().__init__()

        if io_type not in ("input", "output"):
            raise ValueError(f"io_type must be 'input' or 'output', got '{io_type}'")
        self._io_type: Literal["input", "output"] = io_type
        self._io_txt: str = io_txt
        self._anchor_text_spacing: int = get_task_config_param("io/anchor_text_margin")
        self._init_elements()

    def set_font_size(self, font_size: float):
        """
        Sets the font size of the text element inside this IO.

        :param font_size: The new font size to apply.
        """
        self.txt.set_font_size(font_size)

    @property
    def font_size(self) -> float:
        """
        Returns the current font size of the text element.
        """
        return self.txt.font_size

    @property
    def width(self) -> float:
        """
        Returns the total width of this IO element, including text and spacing.
        """
        width_txt = self.txt.width
        return width_txt + (self._anchor_text_spacing) * 2

    @property
    def height(self) -> float:
        """
        Returns the height, max of diameter of anchor or txt.
        """
        radius_attr = float(self.anchor.get_attr("r") or "0")

        return max(self.txt.height, radius_attr * 2)

    def _init_elements(self) -> None:
        """
        Initializes and adds the internal SVG elements: text label and anchor link.

        The text alignment and positioning depend on the IO type.
        """

        self.txt = SvgText(
            self._io_txt,
            x=self._anchor_text_spacing,
            y=0,
            css_class="task_text_io",
        )
        self.anchor = SvgTaskAnchorLink(
            cx=0, cy=0, radius=get_task_config_param("anchor_links/radius")
        )

        if self._io_type == "output":
            self.txt.set_text_anchor("end")
            self.txt.set_position(x=-self._anchor_text_spacing)

        self.add_elements([self.txt, self.anchor])
        font_size = get_task_config_param("io/target_font_size")
        self.set_font_size(font_size)

    def _truncate_text_by_one(self):
        """
        Truncates the displayed text by one character. This is typically
        used to reduce width to fit constraints.
        """
        self.txt._truncate_text_by_one()


class SvgTaskIOGroup(SvgGroup):
    """
    Represents a group of SVG task IO elements arranged vertically.

    :param list_io: A list of strings representing IO labels.
    :param io_type: The IO type for all elements in the group ("Input" or "Output").
    :param vertical_spacing: Vertical space between elements (default is 10).
    """

    def __init__(self, list_io: list, io_type: str, vertical_spacing: float = 10):
        super().__init__()

        if io_type not in ("input", "output"):
            raise ValueError(f"io_type must be 'input' or 'output', got '{io_type}'")
        self._io_type: Literal["input", "output"] = io_type
        self._list_io: list[str] = list_io
        self._vertical_spacing = vertical_spacing
        self._init_elements()

    def set_font_size(self, font_size: float) -> None:
        """
        Sets the font size for all contained SvgTaskIO text elements.

        :param font_size: The font size to set.
        """
        for element in self.elements:
            element.set_font_size(font_size)

    def set_vertical_spacing(self, vertical_spacing):
        """
        Adjusts the vertical spacing between the IO elements.

        :param vertical_spacing: The vertical distance between elements.
        """
        self._vertical_spacing = vertical_spacing
        for i, element in enumerate(self.elements):
            pos = i * vertical_spacing
            element.set_translation(y=pos)

    def decrease_size_to_fit_width(self, target_width):
        """
        Adjusts font size and truncates text as needed to fit the group
        within a target width.

        The font size will not be reduced below `min_font_size`.
        :param target_width: The maximum allowed width for the group.
        """

        min_font_size = get_task_config_param("io/min_font_size")

        if self.elements:
            current_width = self.width

            while (target_width < current_width) and (self.font_size >= min_font_size):
                self.set_font_size(self.font_size - 1)
                current_width = self.width

            while target_width < current_width:
                self._truncate_text_by_one()
                current_width = self.width

    @property
    def width(self) -> float:
        """
        Returns the maximum width among all contained IO elements,
        or 0 if empty.
        """
        if not self.elements:
            return 0.0

        list_width = []
        for element in self.elements:
            list_width.append(element.width)
        return max(list_width)

    @property
    def height(self) -> float:
        """
        Returns the total height of the group based on vertical spacing
        and number of elements.
        """

        return len(self.elements) * self._vertical_spacing

    @property
    def font_size(self) -> float:
        """
        Returns the font size of the first IO element or 0 if empty.
        """
        if self.elements:
            return self.elements[0].font_size
        else:
            return 0.0

    def _init_elements(self) -> None:
        """
        Creates SvgTaskIO elements from the list of IO labels and adds them
        to the group. Sets vertical spacing between elements.
        """

        list_svg_io = [
            SvgTaskIO(io_txt=io, io_type=self._io_type) for io in self._list_io
        ]

        self.add_elements(list_svg_io)
        self.set_vertical_spacing(self._vertical_spacing)

    def _truncate_text_by_one(self):
        """
        Finds the widest text element and truncates it by one character
        to help fit layout constraints.
        """
        if self.elements:
            max_width = -1
            for element in self.elements:
                if element.width > max_width:
                    max_width = element.width
                    max_width_elem = element

            max_width_elem._truncate_text_by_one()
