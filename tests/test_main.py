# tests/test_main.py
import subprocess
from pathlib import Path


def test_basic_use(tmp_path):
    output_path = Path(tmp_path) / "test.svg"

    # Modified call to capture output
    result = subprocess.run(
        ("ewoksdraw", f"{output_path}"), capture_output=True, text=True
    )

    # Print the captured output to the CI log for debugging
    print(f"--- Subprocess STDOUT ---\n{result.stdout}")
    print(f"--- Subprocess STDERR ---\n{result.stderr}")

    # Assert that the command ran successfully
    assert result.returncode == 0, f"Script failed with error:\n{result.stderr}"

    # Assert that the file was created
    assert output_path.is_file()
