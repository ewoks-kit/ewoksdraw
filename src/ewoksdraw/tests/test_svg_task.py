from ewoksdraw.svg.svg_task import SvgTask


def test_io_positions_keep_original_names() -> None:
    long_input_name = "input_name_" * 30
    task = SvgTask(
        task_name="task",
        input_names=[long_input_name],
        output_names=["result"],
    )

    positions = task.get_io_positions()

    assert [(position.name, position.io_type) for position in positions] == [
        (long_input_name, "input"),
        ("result", "output"),
    ]
