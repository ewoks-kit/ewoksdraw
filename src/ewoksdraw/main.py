import sys

from .svg import SvgCanvas, SvgTask


def main():
    filename = sys.argv[1]

    svg_task1 = SvgTask(params={"task_id": "My Task ID"})
    svg_task1.set_position(x=50, y=50)

    svg_task2 = SvgTask(params={"task_id": "My Task ID WAY TOO LONG"})
    svg_task2.set_position(x=150, y=150)

    canvas = SvgCanvas(width=500, height=500)
    canvas.add_element(svg_task1)
    canvas.add_element(svg_task2)
    canvas.generate_svg(filename)


if __name__ == "__main__":
    main()
