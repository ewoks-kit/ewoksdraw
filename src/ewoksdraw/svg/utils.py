import re
from pathlib import Path
from xml.etree.ElementTree import Element

CSS_DIR = Path(__file__).parent.parent / "css_styles"


def _add_variable_fallbacks(css_content: str) -> str:
    if "var(" not in css_content:
        return css_content

    variables = dict(
        re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", (CSS_DIR / "root.css").read_text())
    )

    def convert_rule(rule: re.Match[str]) -> str:
        checks = " and ".join(
            f"({name}: {value.strip()})"
            for name, value in re.findall(r"([\w-]+)\s*:\s*([^;]+);", rule[2])
            if "var(" in value
        )
        if not checks:
            return rule[0]
        fallback = re.sub(
            r"var\(\s*(--[\w-]+)\s*\)",
            lambda variable: variables[variable[1]].strip(),
            rule[2],
        )
        return f"{rule[1]}{{{fallback}}}\n@supports {checks} {{\n{rule[0]}\n}}"

    return re.sub(r"([^{}]+)\{([^{}]*)\}", convert_rule, css_content)


def generate_style_element(css_file_name: str) -> Element:
    css_file_path = CSS_DIR / css_file_name
    style = Element("style")
    css_content = _add_variable_fallbacks(css_file_path.read_text())
    style.text = f"<![CDATA[\n{css_content}\n]]>"
    return style
