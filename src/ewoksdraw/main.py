import random
import sys

from faker import Faker

from .svg import SvgBackground
from .svg import SvgCanvas
from .svg import SvgTask


def generate_random_names() -> list:
    nb_names = abs(int(random.gauss(mu=4, sigma=3)))
    fake = Faker()
    return [
        f"{'_'.join(fake.word() for _ in range(abs(int(random.gauss(mu=3, sigma=1)))))}"
        for _ in range(nb_names)
    ]


def generate_random_name() -> str:
    nb_words = abs(int(random.gauss(mu=4, sigma=3)))
    if nb_words < 1:
        nb_words = 1
    fake = Faker()
    name = ""
    for _ in range(nb_words):
        name += fake.word() + "_"
    return f"{'_'.join(fake.word() for _ in range(nb_words))}"


def main():
    filename = sys.argv[1]

    canvas_width = 500
    canvas_height = 500

    canvas = SvgCanvas(width=canvas_width, height=canvas_height)
    svg_background = SvgBackground(canvas_width, canvas_height)
    canvas.add_element(svg_background)

    nb_tasks = random.randint(1, 5)
    for i in range(nb_tasks):

        task_name = generate_random_name()
        task_inputs = generate_random_names()
        task_outputs = generate_random_names()
        svg_task = SvgTask(
            task_name=task_name,
            input_names=task_inputs,
            output_names=task_outputs,
        )

        svg_task.translate(x=random.randint(5, 400), y=random.randint(5, 400))

        canvas.add_element(svg_task)

    canvas.draw(filename)
    print(canvas.dict)
    print(canvas.xml)


if __name__ == "__main__":
    main()
