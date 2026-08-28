from pathlib import Path
from xml.etree.ElementTree import Element

CSS_DIR = Path(__file__).parent.parent / "css_styles"


def generate_style_element(css_file_name: str) -> None | Element:
    css_file_path = CSS_DIR / css_file_name
    if not css_file_path.exists():
        return None

    with open(css_file_path, "r") as css_file:
        css_content = css_file.read()
    style = Element("style")
    style.text = f"<![CDATA[\n{css_content}\n]]>"
    return style
