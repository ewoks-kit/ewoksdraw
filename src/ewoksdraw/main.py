import sys

from .svg import SvgBackground, SvgCanvas, SvgTask


def main():
    filename = sys.argv[1]

    canvas_width = 500
    canvas_height = 500

    svg_background = SvgBackground(canvas_width, canvas_height)

    svg_task1 = SvgTask(
        params={
            "task_id": "My Task ID",
            "inputs": [
                "name_i_0",
                "name_i_1",
                "name_i_2",
                "name_i_3",
                "name_i_4",
            ],
            "outputs": [
                "output_0",
                "output_1",
                "output_2",
                "output_3",
                "output_4",
            ],
        }
    )
    svg_task1.translate(x=40, y=40)

    canvas = SvgCanvas(width=canvas_width, height=canvas_height)
    canvas.add_element(svg_background)
    canvas.add_element(svg_task1)
    canvas.generate_svg(filename)


if __name__ == "__main__":
    main()
