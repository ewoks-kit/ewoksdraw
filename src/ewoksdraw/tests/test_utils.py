from ..utils import get_edge_source_id
from ..utils import get_edge_target_id
from ..utils import get_task_id_from_source_id
from ..utils import get_task_id_from_target_id


def test_edge_source_task_id_roundtrip() -> None:
    task_id = "pipeline.output.normalize"
    output_name = "value"

    source_id = get_edge_source_id(task_id, output_name)
    assert get_task_id_from_source_id(source_id) == task_id


def test_edge_target_task_id_roundtrip() -> None:
    task_id = "pipeline.input.normalize"
    output_name = "value"

    target_id = get_edge_target_id(task_id, output_name)
    assert get_task_id_from_target_id(target_id) == task_id
