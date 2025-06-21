import re
from typing import Iterable
from typing import List
from typing import Union
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

    def add_elements(self, elements: Iterable[Union[SvgElement, "SvgGroup"]]) -> None:
        """
        Adds elements (SvgElement or SvgGroup) to the group.

        :param elements: The elements to be added.
        """
        for element in elements:
            self.elements.append(element)
        self.populate_group()

    def translate(self, x: float = 0, y: float = 0) -> None:
        """
        Adds a translation transform by appending it to the existing transform attribute.

        :param x: The translation distance along the x-axis (default is 0).
        :param y: The translation distance along the y-axis (default is 0).
        :return: None
        """

        new_transform = f"translate({x},{y})"
        current_transform = self.xml_element.get("transform", "")
        if current_transform:
            updated_transform = f"{current_transform} {new_transform}"
        else:
            updated_transform = new_transform
        self.xml_element.set("transform", updated_transform)

    def set_translation(self, x: float = 0, y: float = 0) -> None:
        """
        Sets the translation transform, replacing any existing translate(...) in the transform attribute.

        :param x: The translation distance along the x-axis (default is 0).
        :param y: The translation distance along the y-axis (default is 0).
        :return: None
        """

        new_translate = f"translate({x},{y})"
        current_transform = self.xml_element.get("transform", "")

        if not current_transform:
            self.xml_element.set("transform", new_translate)
        translate_pattern = (
            r"translate\(\s*[-+]?\d*\.?\d+(?:[,\s]+[-+]?\d*\.?\d+)?\s*\)"
        )

        cleaned_transform = re.sub(translate_pattern, "", current_transform).strip()
        if cleaned_transform:
            updated_transform = f"{cleaned_transform} {new_translate}"
        else:
            updated_transform = new_translate

        self.xml_element.set("transform", updated_transform.strip())

    def get_xml_element(self) -> Element:
        """
        Returns the XML element for the group.

        :return: The XML element.
        """

        return self.xml_element
