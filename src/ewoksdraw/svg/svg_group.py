import re
from typing import Iterable
from typing import Union
from xml.etree.ElementTree import Element

from .svg_element import SvgElement


class SvgGroup:
    """
    Represents a group of SVG elements.
    """

    _TRANSLATE_PATTERN = re.compile(r"translate\((\d+(?:.\d+)?),(\d+(?:.\d+)?)\)")

    def __init__(self):
        self.elements: list[Union[SvgElement, "SvgGroup"]] = []
        self._transform = ""

    def add_elements(self, elements: Iterable[Union[SvgElement, "SvgGroup"]]) -> None:
        """
        Adds elements (SvgElement or SvgGroup) to the group.

        :param elements: The elements to be added.
        """
        self.elements.extend(elements)

    def translate(self, x: float = 0, y: float = 0) -> None:
        """
        Adds a translation transform by appending it to the existing transform state.

        :param x: The translation distance along the x-axis (default is 0).
        :param y: The translation distance along the y-axis (default is 0).
        """
        new_transform = f"translate({x},{y})"
        if self._transform:
            match = self._TRANSLATE_PATTERN.match(self._transform)
            if match:
                self._transform = self._transform.replace(
                    match[0], f"translate({x + float(match[1])},{y + float(match[2])})"
                )
            else:
                self._transform += f" {new_transform}"
        else:
            self._transform = new_transform
        self._transform = self._transform.strip()

    def get_translation(self) -> tuple[float, float]:
        match = self._TRANSLATE_PATTERN.match(self._transform)
        if match is None:
            return 0, 0

        return float(match.group(1)), float(match.group(2))

    @property
    def xml_element(self) -> Element:
        """Returns the XML representation of the group element."""
        group_el = Element("g")
        if self._transform:
            group_el.set("transform", self._transform)
        for element in self.elements:
            group_el.append(element.xml_element)
        return group_el
