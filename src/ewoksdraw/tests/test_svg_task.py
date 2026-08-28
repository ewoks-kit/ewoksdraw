from ewoksdraw.svg.svg_task import SvgTask


def test_io_positions_keep_original_names() -> None:
    long_input_name = "input_name_" * 30
    task = SvgTask(
        task_name="task",
        input_names=[long_input_name],
        output_names=["result"],
    )

    input_positions = task.get_input_positions()
    output_positions = task.get_output_positions()

    assert [position.name for position in input_positions] == [long_input_name]
    assert [position.name for position in output_positions] == ["result"]
