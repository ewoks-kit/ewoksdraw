import sys

from .svg import SvgBackground, SvgCanvas, SvgTask


def main():
    filename = sys.argv[1]

    canvas_width = 500
    canvas_height = 500

    svg_background = SvgBackground(canvas_width, canvas_height)

    svg_task1 = SvgTask(params={"task_id": "My Task ID"})
    svg_task1.set_position(x=50, y=50)

    svg_task2 = SvgTask(params={"task_id": "My LONG Task ID"})
    svg_task2.set_position(x=150, y=150)

    svg_task3 = SvgTask(params={"task_id": "My LOOOOOONNNG Task ID"})
    svg_task3.set_position(x=200, y=300)

    canvas = SvgCanvas(width=canvas_width, height=canvas_height)
    canvas.add_element(svg_background)
    canvas.add_element(svg_task1)
    canvas.add_element(svg_task2)
    canvas.add_element(svg_task3)
    canvas.generate_svg(filename)


if __name__ == "__main__":
    main()
