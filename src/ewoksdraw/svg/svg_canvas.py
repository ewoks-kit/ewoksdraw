from pathlib import Path
from typing import List
from typing import Optional
from typing import Union
from xml.dom import minidom
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring

from .svg_element import SvgElement
from .svg_group import SvgGroup


class SvgCanvas:
    """
    Class representing the SVG drawing canvas.
    """

    def __init__(self, width: int, height: int):
        """
        Initialize the SVG drawing canvas.

        :param width: The width of the canvas.
        :param height: The height of the canvas.
        """
        self.width = width
        self.height = height
        self.elements: List[Union[SvgElement, SvgGroup]] = []

    def add_element(self, element: Union[SvgElement, SvgGroup]) -> None:
        """
        Adds an element or group to the drawing.

        :param element: The element or group to be added.
        """
        self.elements.append(element)

    def gather_styles(
        self, element: Union[SvgElement, SvgGroup], style_list: List[Optional[Element]]
    ) -> List[Optional[Element]]:
        """
        Recursively gathers styles from elements and groups.

        :param element: The element or group to gather styles from.
        :param style_list: The list to store gathered styles.
        :return: The list of gathered styles.
        """
        if isinstance(element, SvgElement):
            style_list.append(element.get_style_element())
        elif isinstance(element, SvgGroup):
            for child in element.elements:
                style_list = self.gather_styles(child, style_list)
        return style_list

    def generate_svg(self, filename: Union[Path, str]) -> None:
        """
        Generates the SVG XML file with all elements and styles, and writes it to disk.

        This method collects styles from all elements and groups, removes duplicate styles,
        appends all elements to the root SVG element, and outputs a pretty-printed SVG file.

        :param filename: The path or filename where the SVG file will be saved.
        """
        svg = Element(
            "svg",
            xmlns="http://www.w3.org/2000/svg",
            width=str(self.width),
            height=str(self.height),
        )
        style_elements: List[Optional[Element]] = []
        for element in self.elements:
            if isinstance(element, SvgElement):
                style = element.get_style_element()
                if style is not None:
                    style_elements.append(style)
            elif isinstance(element, SvgGroup):
                style_elements = self.gather_styles(element, style_elements)

        list_style_str = set()
        for style in style_elements:
            if style is not None and (style.text not in list_style_str):
                svg.append(style)
                list_style_str.add(style.text)

        for element in self.elements:
            svg.append(element.get_xml_element())
        svg_string = tostring(svg, encoding="unicode", method="xml")
        svg_string = svg_string.replace("&lt;![CDATA[", "<![CDATA[").replace(
            "]]&gt;", "]]>"
        )
        dom = minidom.parseString(svg_string)
        pretty_svg_string = dom.toprettyxml(indent="  ")
        with open(filename, "w") as file:
            file.write(pretty_svg_string)
