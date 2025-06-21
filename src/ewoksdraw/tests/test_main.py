import subprocess
from pathlib import Path


def test_basic_use(tmp_path):
    output_path = Path(tmp_path) / "output.svg"
    subprocess.run(("ewoksdraw", f"{output_path}"))

    assert output_path.is_file()
