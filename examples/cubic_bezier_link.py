import copy
from pathlib import Path

from ewoksdraw.geometry.cubic_bezier_path import CubicBezierPath
from ewoksdraw.geometry.cubic_bezier_path import CubicBezierSegment
from ewoksdraw.svg.svg_canvas import SvgCanvas
from ewoksdraw.svg.svg_group import SvgGroup
from ewoksdraw.svg.svg_link_cubic_bezier import SvgLinkCubicBezier

output_path = Path(__file__).with_suffix(".svg")

letter_e = CubicBezierPath(
    start=(10, 130),
    segments=[
        CubicBezierSegment((40, 115), (75, 95), (105, 90)),
        CubicBezierSegment((125, 75), (55, 50), (25, 115)),
        CubicBezierSegment((0, 165), (70, 170), (115, 140)),
    ],
)
letter_w = CubicBezierPath(
    start=(135, 84),
    segments=[
        CubicBezierSegment((142, 124), (145, 154), (158, 156)),
        CubicBezierSegment((169, 158), (176, 102), (187, 102)),
        CubicBezierSegment((198, 102), (196, 157), (210, 157)),
        CubicBezierSegment((224, 157), (236, 105), (244, 84)),
    ],
)

letter_o = CubicBezierPath(
    start=(302, 113),
    segments=[
        CubicBezierSegment((302, 86), (260, 80), (253, 112)),
        CubicBezierSegment((247, 141), (286, 155), (304, 128)),
        CubicBezierSegment((317, 108), (307, 89), (290, 87)),
    ],
)

letter_k = CubicBezierPath(
    start=(348, 70),
    segments=[
        CubicBezierSegment((342, 104), (340, 128), (338, 158)),
        CubicBezierSegment((353, 130), (374, 102), (394, 83)),
        CubicBezierSegment((373, 107), (369, 127), (394, 154)),
    ],
)

letter_s = CubicBezierPath(
    start=(469, 84),
    segments=[
        CubicBezierSegment((434, 72), (421, 102), (453, 115)),
        CubicBezierSegment((491, 130), (482, 162), (439, 151)),
        CubicBezierSegment((420, 146), (427, 130), (448, 133)),
    ],
)

underline = CubicBezierPath.from_points(
    points=[
        (40, 175),
        (240, 175),
        (240, 205),
        (480, 205),
        (480, 25),
        (320, 25),
        (320, 205),
    ],
    radius=30,
)
links_group = SvgGroup()
links_group.add_elements(
    [
        SvgLinkCubicBezier(letter_e),
        SvgLinkCubicBezier(
            letter_w,
            color="#00c2a8",
            stroke_width=4,
            stroke_dasharray="5 10",
        ),
        SvgLinkCubicBezier(
            letter_o,
            color="#ffcc00",
            stroke_width=6,
            stroke_dasharray="1 5",
        ),
        SvgLinkCubicBezier(letter_k, color="#7c5cff", stroke_width=4),
        SvgLinkCubicBezier(letter_s, color="#54a068", stroke_width=10),
        SvgLinkCubicBezier(
            underline,
            color="#ff00aa",
            stroke_width=3,
            stroke_dasharray="12 6",
        ),
    ]
)

links_group_2 = copy.copy(links_group)
links_group_2.translate(5, 5)

canvas = SvgCanvas(width=520, height=220)
canvas.add_background()
canvas.add_element(links_group)
canvas.add_element(links_group_2)

canvas.draw(output_path)
print(f"Wrote {output_path}")
