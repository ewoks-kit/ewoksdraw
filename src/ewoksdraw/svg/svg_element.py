from pathlib import Path
from typing import Literal
from typing import Optional
from xml.etree.ElementTree import Element


class SvgElement:
    """
    Represents generic SVG element.

    :param tag: The SVG tag (e.g., 'rect', 'circle', 'text').
    :param css_class: The CSS class to apply to the SVG element.
                       Should match a CSS file in the css_styles directory.
    :param attr: A dictionary of svg attributes
    """

    def __init__(
        self,
        tag: Literal["rect", "circle", "text", "line"],
        css_class: Optional[str] = None,
        attr: Optional[dict] = None,
        text: Optional[str] = None,
    ):

        if tag not in ["rect", "circle", "text", "line"]:
            raise ValueError(
                f"Invalid SVG tag: {tag}. Supported tags are 'rect', 'circle', 'text',"
                " 'line'."
            )
        self._tag = tag

        self._css_class = css_class
        self._attr = attr or {}
        self._text = text
        self._style_element = self._load_css_style()

    def set_position(
        self, x: Optional[float] = None, y: Optional[float] = None
    ) -> None:
        """
        Sets the position of the SVG element by updating its x and y attributes.
        :param x: The x-coordinate to set. If None, the x attribute is not changed.
        :param y: The y-coordinate to set. If None, the y attribute is not changed.
        """
        if self._tag == "circle":
            attr_x = "cx"
            attr_y = "cy"
        else:
            attr_x = "x"
            attr_y = "y"

        if x is not None:
            self.set_attr(attr_x, str(x))
        if y is not None:
            self.set_attr(attr_y, str(y))

    def set_attr(self, key: str, value: str) -> None:
        """
        Setter for any attribute key.
        :param key: The attribute key (string).
        :param value: The value to set.
        """
        self._attr[key] = value

    def get_attr(self, key: str) -> Optional[str]:
        """
        Getter for any attribute key.

        :param key: The attribute key (string).
        :return: The value for the key or None if not found.
        """
        if key not in self._attr:
            return None

        return self._attr.get(key)

    @property
    def text(self) -> Optional[str]:
        return self._text

    @property
    def xml_element(self) -> Element:
        return self._create_xml_element()

    @property
    def style_element(self) -> Optional[Element]:
        return self._style_element

    @text.setter
    def text(self, value: str) -> None:
        self._text = value

    def _create_xml_element(self) -> Element:
        """
        Creates the XML element for the SVG shape.

        :return: The XML element.
        """
        element = Element(self._tag, self._attr)
        if self.text is not None:
            element.text = self.text
        if self._css_class:
            element.set("class", self._css_class)
        return element

    def _load_css_style(self) -> Optional[Element]:
        """
        Loads the CSS style from a file and returns it as an XML <style> element.

        :return: The XML <style> element containing the CSS content.
        """
        if self._css_class:
            css_file_path = Path(f"src/ewoksdraw/css_styles/css_{self._css_class}.css")
            if css_file_path.exists():
                with open(css_file_path, "r") as css_file:
                    css_content = css_file.read()
                style = Element("style")
                style.text = f"<![CDATA[\n{css_content}\n]]>"
                return style
