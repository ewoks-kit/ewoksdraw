from src.ewoksdraw.svg import SvgCanvas, SvgTask

if __name__ == "__main__":
    svg_task = SvgTask(params={"title": "My Task Title"})
    canvas = SvgCanvas(width=500, height=500)
    canvas.add_element(svg_task)
    canvas.generate_svg("output.svg")
