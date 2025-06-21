from typing import Any
from typing import Dict
from typing import List

from .svg_group import SvgElement
from .svg_group import SvgGroup
from .svg_task_anchor_link import SvgTaskAnchorLink
from .svg_text import SvgText


class SvgTaskIO(SvgGroup):
    """
    Represents a single SVG task input or output element with text and an anchor link.

    This class inherits from SvgGroup and contains a text element representing
    the IO name and a circular anchor link. It supports positioning and styling
    based on whether it is an input or output.

    :param io_txt: The label text for the IO element.
    :param io_type: The type of IO, typically "Input" or "Output".
    """

    def __init__(self, io_txt: str, io_type: str):
        """
        Initializes the SvgTaskIO element with given text and type, then
        creates and adds the SVG text and anchor elements.
        """
        super().__init__()
        self.io_txt = io_txt
        self.io_type = io_type
        self.anchor_text_spacing: int = 5
        self.init_elements()

    def init_elements(self) -> None:
        """
        Initializes and adds the internal SVG elements: text label and anchor link.

        The text alignment and positioning depend on the IO type.
        """

        txt = SvgText(
            self.io_txt,
            x=self.anchor_text_spacing,
            y=0,
            css_class="task_text_io",
        )
        anchor = SvgTaskAnchorLink(cx=0, cy=0, radius=2.0)

        if self.io_type == "Output":
            txt.set_text_anchor("end")
            txt.set_position(x=-self.anchor_text_spacing)

        self.add_elements([txt, anchor])

    def set_font_size(self, font_size: float):
        """
        Sets the font size of the text element inside this IO.

        :param font_size: The new font size to apply.
        """
        self.elements[0].set_font_size(font_size)

    def _truncate_text_by_one(self):
        """
        Truncates the displayed text by one character. This is typically
        used to reduce width to fit constraints.
        """
        self.elements[0]._truncate_text_by_one()

    @property
    def font_size(self) -> float:
        """
        Returns the current font size of the text element.
        """
        return self.elements[0].font_size

    @property
    def width(self) -> float:
        """
        Returns the total width of this IO element, including text and spacing.
        """
        width_txt = self.elements[0].width
        return width_txt + (self.anchor_text_spacing) * 2

    @property
    def height(self) -> float:
        """
        Returns the height, max of diameter of anchor or txt.
        """
        return max(self.elements[0].height, self.elements[1].attr["r"] * 2)


class SvgTaskIOGroup(SvgGroup):
    """
    Represents a group of SVG task IO elements arranged vertically.

    This class manages a list of SvgTaskIO objects, controlling layout,
    font size, and vertical spacing.

    :param list_io: A list of strings representing IO labels.
    :param io_type: The IO type for all elements in the group ("Input" or "Output").
    :param vertical_spacing: Vertical space between elements (default is 10).
    """

    def __init__(self, list_io: list, io_type: str, vertical_spacing: float = 10):
        """
        Initializes the SvgTaskIOGroup by creating SvgTaskIO elements
        for each label and arranging them vertically.
        """
        super().__init__()
        self.io_type = io_type
        self.list_io = list_io
        self.vertical_spacing = vertical_spacing
        self.init_elements()

    def init_elements(self) -> None:
        """
        Creates SvgTaskIO elements from the list of IO labels and adds them
        to the group. Sets vertical spacing between elements.
        """

        list_svg_io = []
        for io in self.list_io:
            list_svg_io.append(SvgTaskIO(io_txt=io, io_type=self.io_type))

        self.add_elements(list_svg_io)
        self.set_vertical_spacing(self.vertical_spacing)

    def set_font_size(self, font_size: float) -> None:
        """
        Sets the font size for all contained SvgTaskIO elements.

        :param font_size: The font size to set.
        """
        for element in self.elements:
            element.set_font_size(font_size)

    def set_vertical_spacing(self, vertical_spacing):
        """
        Adjusts the vertical spacing between the IO elements.

        :param vertical_spacing: The vertical distance between elements.
        """
        self.vertical_spacing = vertical_spacing
        for i, element in enumerate(self.elements):
            pos = i * vertical_spacing
            element.set_translation(y=pos)

    @property
    def width(self) -> float:
        """
        Returns the maximum width among all contained IO elements,
        or 0 if empty.
        """
        list_width = []
        if self.elements:
            for element in self.elements:
                list_width.append(element.width)
            return max(list_width)
        else:
            return 0.0

    @property
    def height(self) -> float:
        """
        Returns the total height of the group based on vertical spacing
        and number of elements.
        """

        return len(self.elements) * self.vertical_spacing

    @property
    def font_size(self) -> float:
        """
        Returns the font size of the first IO element or 0 if empty.
        """
        if self.elements:
            return self.elements[0].font_size
        else:
            return 0

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

    def modify_size_to_fit_width(self, target_width, min_font_size=5):
        """
        Adjusts font size and truncates text as needed to fit the group
        within a target width.

        The font size will not be reduced below `min_font_size`.

        :param target_width: The maximum allowed width for the group.
        :param min_font_size: The minimum font size allowed.
        """
        if self.elements:
            current_width = self.width

            while (target_width < current_width) and (self.font_size >= min_font_size):
                self.set_font_size(self.font_size - 1)
                current_width = self.width

            while target_width < current_width:
                self._truncate_text_by_one()
                current_width = self.width
