from pathlib import Path
from typing import Optional
from xml.etree.ElementTree import Element


class SvgElement:
    """
    Base class for all SVG elements.
    """

    def __init__(
        self,
        tag: str,
        css_class: Optional[str] = None,
        attr: Optional[dict] = None,
        text: Optional[str] = None,
    ):
        """
        Initialize an SVG element.

        :param tag: The SVG tag (e.g., 'rect', 'circle', 'text').
        :param css_class: The CSS class to be applied to the SVG element.
        :param attr: A dictionary of attributes for the SVG element.
        :param text: The text content for the SVG element, if applicable.
        """
        self.tag = tag
        self.css_class = css_class
        self.attr = attr or {}
        self.text = text
        self.style_element = self.load_css_style()
        self.xml_element = self.create_xml_element()

    def create_xml_element(self) -> Element:
        """
        Creates the XML element for the SVG shape.

        :return: The XML element.
        """
        element = Element(self.tag, self.attr)
        if self.text is not None:
            element.text = self.text
        if self.css_class:
            element.set("class", self.css_class)
        return element

    def set_text(self, text: str):
        self.text = text
        self.xml_element.text = text

    def load_css_style(self) -> Optional[Element]:
        """
        Loads the CSS style from a file and returns it as an XML <style> element.

        :return: The XML <style> element containing the CSS content.
        """
        if self.css_class:
            css_file_path = Path(f"src/ewoksdraw/css_styles/css_{self.css_class}.css")
            if css_file_path.exists():
                with open(css_file_path, "r") as css_file:
                    css_content = css_file.read()
                style_element = Element("style")
                style_element.text = f"<![CDATA[\n{css_content}\n]]>"
                return style_element
        return None

    def update_attribute(self) -> None:
        """
        Updates an attribute in the XML element.
        """
        for key in self.attr.keys():
            value = self.attr[key]
            self.xml_element.set(key, str(value))

    def get_xml_element(self) -> Element:
        """
        Returns the XML element for the SVG shape.

        :return: The XML element.
        """

        return self.xml_element

    def get_style_element(self) -> Optional[Element]:
        """
        Returns the CSS content loaded for the element (as XML <style> element).

        :return: The XML <style> element containing the CSS content.
        """
        return self.style_element
