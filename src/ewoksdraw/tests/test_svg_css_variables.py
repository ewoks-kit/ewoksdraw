from pathlib import Path

import pytest

from ewoksdraw.svg import utils


@pytest.fixture
def css_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    (tmp_path / "root.css").write_text(
        ".ewoksdraw {\n"
        "  --link-color: #b093ff;\n"
        "  --stroke-color: #ffffff;\n"
        "  --error: #ff0000;\n"
        "}\n"
    )
    monkeypatch.setattr(utils, "CSS_DIR", tmp_path)
    return tmp_path


def test_variable_generates_fallback_and_supports(css_dir: Path) -> None:
    result = utils._add_css_variable_fallback(".anchor { fill: var(--link-color); }")

    assert " ".join(result.split()) == (
        ".anchor { fill: #b093ff; } "
        "@supports (--css: variables) { "
        ".anchor { fill: var(--link-color); } }"
    )


def test_css_without_variables_is_unchanged(css_dir: Path) -> None:
    css = ".anchor {\n  fill: purple;\n  stroke-width: 2;\n}\n"

    assert utils._add_css_variable_fallback(css) == css


def test_multiple_variables_are_replaced(css_dir: Path) -> None:
    result = utils._add_css_variable_fallback(
        ".anchor { fill: var(--link-color); "
        "stroke: var(--stroke-color); stroke-width: 2; }"
    )

    assert " ".join(result.split()) == (
        ".anchor { fill: #b093ff; stroke: #ffffff; stroke-width: 2; } "
        "@supports (--css: variables) { "
        ".anchor { fill: var(--link-color); "
        "stroke: var(--stroke-color); stroke-width: 2; } }"
    )


def test_import_error_rule_stays_after_normal_rule(css_dir: Path) -> None:
    result = utils._add_css_variable_fallback(
        ".task_box { stroke: var(--stroke-color); }\n"
        ".task_box[data-import-error=''] { stroke: var(--error); }"
    )

    assert " ".join(result.split()) == (
        ".task_box { stroke: #ffffff; } "
        ".task_box[data-import-error=''] { stroke: #ff0000; } "
        "@supports (--css: variables) { "
        ".task_box { stroke: var(--stroke-color); } "
        ".task_box[data-import-error=''] { stroke: var(--error); } }"
    )
