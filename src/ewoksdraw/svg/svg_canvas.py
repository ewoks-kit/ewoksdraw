from pathlib import Path
from typing import Iterator
from typing import List
from typing import Union
from xml.dom import minidom
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring

import xmltodict

from .svg_element import SvgElement
from .svg_group import SvgGroup


class SvgCanvas:
    """
    Represents the SVG drawing canvas.
    It's the first element in the SVG file and contains all other elements.
    SvgElement or SvgGroup can be added to the canvas.
    The SvgCanvas compile every css styles and elements to generate the final
    SVG XML file.
    """

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.elements: List[Union[SvgElement, SvgGroup]] = []
        self._xml_svg = Element(
            "svg",
            xmlns="http://www.w3.org/2000/svg",
            width=str(self.width),
            height=str(self.height),
        )

    def add_element(self, element: Union[SvgElement, SvgGroup]) -> None:
        """
        Adds an SvgElement or SvgGroup to the drawing.

        :param element: The element or group to be added.
        """
        self.elements.append(element)

    def draw(self, filename: Union[Path, str]) -> None:
        """
        Save the SVG canvas to a file.
        :param filename: The name of the file to save the SVG content.
        """
        self._populate_xml_svg()
        self._convert_xml_svg_to_string()
        with open(filename, "w") as file:
            file.write(self._convert_xml_svg_to_string())

    @property
    def xml(self) -> Element:
        """
        Returns the XML representation of the SVG canvas.
        """
        self._populate_xml_svg()
        return self._xml_svg

    @property
    def dict(self) -> dict:
        """
        Returns the SVG canvas as a dictionary.
        """
        xml_str = self._convert_xml_svg_to_string()
        return xmltodict.parse(xml_str)


    def _yield_styles(self, element: Union[SvgElement, SvgGroup]) -> Iterator[Element]:
        """
        Recursively walks through elements and yields their styles.
        This is a generator function.

        :param element: The root element or group to start from.
        """
        if isinstance(element, SvgElement):
            if element.style_element is not None:
                yield element.style_element
        elif isinstance(element, SvgGroup):
            for child in element.elements:
                yield from self._yield_styles(child)

    def _gather_all_styles(self) -> List[Element]:
        """
        Gathers all unique styles from the canvas elements.
        Uses the `_yield_styles` generator to walk the element tree.

        :return: A list of unique style elements.
        """
        all_styles: List[Element] = []
        for element in self.elements:
            all_styles.extend(self._yield_styles(element))

        return all_styles

    def _convert_xml_svg_to_string(self) -> str:
        """Converts the XML SVG element to a pretty-printed string."""

        for element in self.elements:
            self._xml_svg.append(element.xml_element)
        svg_string = tostring(self._xml_svg, encoding="unicode", method="xml")
        svg_string = svg_string.replace("&lt;![CDATA[", "<![CDATA[").replace(
            "]]&gt;", "]]>"
        )
        dom = minidom.parseString(svg_string)
        return dom.toprettyxml(indent="  ")

    def _populate_xml_svg(self) -> None:
        """Populates the XML SVG element with styles and elements."""

        if len(self._xml_svg) != 1:
            self._xml_svg = Element(
                "svg",
                xmlns="http://www.w3.org/2000/svg",
                width=str(self.width),
                height=str(self.height),
            )
        style_elements = self._gather_all_styles()

        list_style_str = set()
        for style in style_elements:
            if style is not None and (style.text not in list_style_str):
                self._xml_svg.append(style)
                list_style_str.add(style.text)
