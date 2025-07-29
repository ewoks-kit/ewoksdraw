from pathlib import Path
from typing import List
from typing import Optional
from typing import Sequence
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

    def add_elements(
        self, list_elements: Sequence[Union[SvgElement, SvgGroup]]
    ) -> None:
        """
        Adds a List of SvgElements or SvgGroups to the drawing.

        :param element: Lists element or/and groups to be added.
        """
        self.elements += list_elements

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

    def _gather_styles_from_svg_group(
        self, element: Union[SvgElement, SvgGroup], style_list: List[Optional[Element]]
    ) -> List[Optional[Element]]:
        """
        Recursively gathers styles from elements and groups.

        :param element: The element or group to gather styles from.
        :param style_list: The list to store gathered styles.
        :return: The list of gathered styles.
        """
        if isinstance(element, SvgElement):
            style_list.append(element.style_element)
        elif isinstance(element, SvgGroup):
            for child in element.elements:
                style_list = self._gather_styles_from_svg_group(child, style_list)
        return style_list

    def _gather_all_styles(self) -> List[Optional[Element]]:
        """
        Gathers all styles from the elements and groups in the canvas.
        :return: A list of style elements.
        """
        style_elements: List[Optional[Element]] = []
        for element in self.elements:
            if isinstance(element, SvgElement):
                style = element.style_element
                if style is not None:
                    style_elements.append(style)
            elif isinstance(element, SvgGroup):
                style_elements = self._gather_styles_from_svg_group(
                    element, style_elements
                )
        return style_elements

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
