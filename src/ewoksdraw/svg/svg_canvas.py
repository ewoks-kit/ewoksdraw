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


def pretty_print_xml(xml_svg: Element) -> str:
    """
    Converts an XML Element to a pretty-printed string.
    :param xml_svg: Xml Element in the svg format

    :return: string representation of the xml/svg element
    """
    svg_string = tostring(xml_svg, encoding="unicode", method="xml")

    svg_string = svg_string.replace("&lt;![CDATA[", "<![CDATA[").replace(
        "]]&gt;", "]]>"
    )

    dom = minidom.parseString(svg_string)
    return dom.toprettyxml(indent="  ")


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
        with open(filename, "w") as file:
            file.write(self._get_svg_string())

    @property
    def xml(self) -> Element:
        """
        Returns the XML representation of the SVG canvas.
        """
        return self._generate_xml_svg()

    @property
    def dict(self) -> dict:
        """
        Returns the SVG canvas as a dictionary.
        """
        return xmltodict.parse(self._get_svg_string())

    def _get_svg_string(self) -> str:
        """
        Helper method to get the final, pretty-printed SVG string.
        """
        return pretty_print_xml(self.xml)

    def _generate_xml_svg(self) -> Element:
        """
        Generates a fresh SVG Element from the current canvas state.
        """
        xml_svg = Element(
            "svg",
            xmlns="http://www.w3.org/2000/svg",
            width=str(self.width),
            height=str(self.height),
        )

        style_elements = self._gather_all_styles()
        seen_styles = set()
        for style in style_elements:
            if style.text not in seen_styles:
                xml_svg.append(style)
                seen_styles.add(style.text)

        for element in self.elements:
            xml_svg.append(element.xml_element)

        return xml_svg

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
