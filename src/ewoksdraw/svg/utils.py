from pathlib import Path
from xml.etree.ElementTree import Element

CSS_DIR = Path(__file__).parent.parent / "css_styles"
ROOT_CSS_PATH = CSS_DIR / "root.css"


def generate_style_element(css_file_name: str) -> Element:
    css = (CSS_DIR / css_file_name).read_text()
    css_with_fallback = _add_css_variable_fallback(css)
    style = Element("style")
    style.text = f"<![CDATA[\n{css_with_fallback}\n]]>"
    return style


def _add_css_variable_fallback(css: str) -> str:

    if "var(" not in css:
        return css

    theme_values = _read_theme_values()
    css_with_plain_values = _replace_css_variables(css, theme_values)
    original_css_if_supported = f"@supports (--css: variables) {{\n{css}\n}}"
    return f"{css_with_plain_values}\n{original_css_if_supported}"


def _read_theme_values() -> dict[str, str]:
    """Read root.css into {"--link-color": "rgb(176, 147, 255)", ...}."""
    root_css = ROOT_CSS_PATH.read_text()
    theme_values: dict[str, str] = {}
    for line in root_css.splitlines():
        declaration = line.strip().removesuffix(";")
        if declaration.startswith("--"):
            name, value = declaration.split(": ")
            theme_values[name] = value
    return theme_values


def _replace_css_variables(css: str, theme_values: dict[str, str]) -> str:
    """Replace each "var(--link-color)" by its value, e.g. "rgb(176, 147, 255)"."""
    for name, value in theme_values.items():
        css = css.replace(f"var({name})", value)
    return css
