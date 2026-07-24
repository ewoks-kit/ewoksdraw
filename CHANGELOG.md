# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- CLI entry point `ewoksdraw` that generates an SVG file from a single output path argument.
- Automatic mock workflow generation with a background and randomly positioned task blocks.
- SVG task rendering with:
  - task title text
  - task box and title separator line
  - input/output labels
  - circular anchor links for IO ports
- Adaptive task layout logic that scales/truncates text and adjusts font sizes to keep content within box width constraints.
- SVG canvas export helpers:
  - pretty-printed SVG file output
  - in-memory XML representation
  - dictionary representation via `xmltodict`
- Basic CLI smoke test ensuring `ewoksdraw` writes an SVG output file.
- Rounded cubic Bezier path geometry (`CubicBezierPath`/`CubicBezierSegment`) for connecting horizontal/vertical polyline points.
- `SvgLinkCubicBezier` SVG `path` component for rendering workflow links, with configurable color, stroke width, and dash array.
- `path` support in `SvgElement`'s supported SVG tags; `set_position()` now warns and no-ops for `path` elements since their position is defined by path data.
- `SvgTaskGroup`: a positioned collection of `SvgTask` elements, with horizontal arrangement and task size extraction for layout conversion.
- `convert_ewoks_to_elk_graph()` in `ewoksdraw.layout.elk_converter`, converting an Ewoks task graph and its task sizes into an ELK (`ElkGraph`) layout graph, validated against the source graph's task ids.
- `ELK_LAYOUT_OPTION` default layout options (layered algorithm, spline edge routing) for ELK graph conversion.
- `pyelk` dependency for ELK graph layout support.