from pathlib import Path

import pytest

from ewoksdraw.svg import utils


@pytest.fixture
def css_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    (tmp_path / "root.css").write_text(
        ".ewoksdraw { --link-color: #b093ff; "
        "--stroke-color: #ffffff; --error: #ff0000; }"
    )
    monkeypatch.setattr(utils, "CSS_DIR", tmp_path)
    return tmp_path


def test_variable_generates_fallback_and_supports(css_dir: Path) -> None:
    result = utils._add_variable_fallbacks(".anchor { fill: var(--link-color); }")

    assert " ".join(result.split()) == (
        ".anchor { fill: #b093ff; } "
        "@supports (fill: var(--link-color)) { "
        ".anchor { fill: var(--link-color); } }"
    )


def test_css_without_variables_is_unchanged(css_dir: Path) -> None:
    css = ".anchor {\n  fill: purple;\n  stroke-width: 2;\n}\n"

    assert utils._add_variable_fallbacks(css) == css


def test_multiple_variable_properties_combine_support_checks(css_dir: Path) -> None:
    result = utils._add_variable_fallbacks(
        ".anchor { fill: var(--link-color); "
        "stroke: var(--stroke-color); stroke-width: 2; }"
    )

    assert " ".join(result.split()) == (
        ".anchor { fill: #b093ff; stroke: #ffffff; stroke-width: 2; } "
        "@supports (fill: var(--link-color)) and (stroke: var(--stroke-color)) { "
        ".anchor { fill: var(--link-color); "
        "stroke: var(--stroke-color); stroke-width: 2; } }"
    )


def test_import_error_selector_and_rule_order_are_preserved(css_dir: Path) -> None:
    result = utils._add_variable_fallbacks(
        ".task_box { stroke: var(--stroke-color); }\n"
        ".task_box[data-import-error=''] { stroke: var(--error); }"
    )

    assert " ".join(result.split()) == (
        ".task_box { stroke: #ffffff; } "
        "@supports (stroke: var(--stroke-color)) { "
        ".task_box { stroke: var(--stroke-color); } } "
        ".task_box[data-import-error=''] { stroke: #ff0000; } "
        "@supports (stroke: var(--error)) { "
        ".task_box[data-import-error=''] { stroke: var(--error); } }"
    )


def test_undefined_variable_raises_error(css_dir: Path) -> None:
    with pytest.raises(KeyError, match="missing-color"):
        utils._add_variable_fallbacks(".anchor { fill: var(--missing-color); }")
