from ..geometry.cubic_bezier_path import CubicBezierPath
from .svg_element import SvgElement


class SvgLinkCubicBezier(SvgElement):
    """
    Represents an SVG path element for a cubic Bezier link.

    :param path: The cubic Bezier path coordinates.
    :param color: The stroke color of the link.
    :param stroke_width: The stroke width of the link.
    :param stroke_dasharray: The SVG stroke-dasharray value of the link.
    """

    def __init__(
        self,
        path: CubicBezierPath,
        color: str | None = None,
        stroke_width: float | None = None,
        stroke_dasharray: str | None = None,
    ):
        string_svg = self._convert_path_data_to_svg_attribute(path)

        attr = {"d": string_svg}
        styles = []

        if color is not None:
            styles.append(f"stroke:{color}")

        if stroke_width is not None:
            styles.append(f"stroke-width:{stroke_width:g}")

        if stroke_dasharray is not None:
            styles.append(f"stroke-dasharray:{stroke_dasharray}")

        if styles:
            attr["style"] = ";".join(styles)

        super().__init__(tag="path", css_class="link_cubic_bezier", attr=attr)

    def _convert_path_data_to_svg_attribute(self, path: CubicBezierPath) -> str:
        if not path.segments:
            raise ValueError("A cubic Bezier path needs at least one segment.")

        start_x, start_y = path.start
        commands = [f"M {start_x},{start_y}"]

        for segment in path.segments:
            control1_x, control1_y = segment.control1
            control2_x, control2_y = segment.control2
            end_x, end_y = segment.end
            commands.append(
                f"C {control1_x},{control1_y} {control2_x},{control2_y} {end_x},{end_y}"
            )

        return " ".join(commands)
