import sys
from .svg import SvgCanvas, SvgTask


def main():
    filename = sys.argv[1]

    svg_task = SvgTask(params={"task_id": "My Task ID"})
    canvas = SvgCanvas(width=500, height=500)
    canvas.add_element(svg_task)
    canvas.generate_svg(filename)


if __name__ == "__main__":
    main()
