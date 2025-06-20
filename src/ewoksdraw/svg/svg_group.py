from typing import List, Optional, Union
from xml.etree.ElementTree import Element

from .svg_element import SvgElement


class SvgGroup:
    """
    Class representing a group of SVG elements.
    """

    def __init__(self):
        """
        Initialize a group to hold multiple elements or other groups.

        :param elements: A list of elements or groups to be included in the group.
        """
        self.elements = []
        self.tag = "group"
        self.xml_element = Element("g")

    def populate_group(self) -> None:
        """
        Populates the group with child elements or other groups.
        """
        for element in self.elements:
            self.xml_element.append(element.get_xml_element())

    def add_elements(self, elements: List[Union[SvgElement, "SvgGroup"]]) -> None:
        """
        Adds elements (SvgElement or SvgGroup) to the group.

        :param elements: The elements to be added.
        """
        for element in elements:
            self.elements.append(element)
        self.populate_group()

    # def translate(self, x: int = 0, y: int = 0) -> None:

    #     current_transform = self.xml_element.get("transform")
    #     print("---")
    #     print(current_transform)

    #     transform = f"translate({x},{y})"
    #     self.xml_element.set("transform", transform)

    def translate(self, x: int = 0, y: int = 0) -> None:

        new_transform = f"translate({x},{y})"
        current_transform = self.xml_element.get("transform", "")
        if current_transform:
            updated_transform = f"{current_transform} {new_transform}"
        else:
            updated_transform = new_transform
        self.xml_element.set("transform", updated_transform)

    def get_xml_element(self) -> Element:
        """
        Returns the XML element for the group.

        :return: The XML element.
        """

        return self.xml_element
