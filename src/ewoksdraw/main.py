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
                "input_0",
                "input_1",
                "input_2",
                "input_3",
                "input_4",
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

    svg_task2 = SvgTask(
        params={
            "task_id": "My Task ID Again ",
            "inputs": [
                "input_0_TROOOOOPPPP_LLLLONNNNGGGG",
                "input_1",
            ],
            "outputs": [
                "output_0",
            ],
        }
    )
    svg_task2.translate(x=60, y=160)

    svg_task3 = SvgTask(
        params={
            "task_id": "3",
            "inputs": [
                "1",
                "2",
                "1",
                "2",
                "1",
                "2",
                "1",
                "2",
                "1",
                "2",
                "1",
                "2",
                "1",
                "2",
                "1",
                "2",
                "1",
                "2",
            ],
            "outputs": [
                "1",
            ],
        }
    )
    svg_task3.translate(x=150, y=10)

    canvas = SvgCanvas(width=canvas_width, height=canvas_height)
    canvas.add_element(svg_background)
    canvas.add_element(svg_task1)
    canvas.add_element(svg_task2)
    canvas.add_element(svg_task3)
    canvas.generate_svg(filename)


if __name__ == "__main__":
    main()
