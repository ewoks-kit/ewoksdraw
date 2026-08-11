from .svg_element import SvgElement


class SvgLink(SvgElement):
    """
    Represents a routed SVG link path.
    """

    def __init__(
        self,
        points: list[dict],
        routing: str | None = None,
        color: str | None = None,
        link_id: str | None = None,
        source_node_id: str | None = None,
        source_output: str | None = None,
        target_node_id: str | None = None,
        target_input: str | None = None,
        map_all_data: bool = False,
    ):
        attr = {"d": self._path_data(points, routing)}
        if color:
            attr["style"] = f"stroke: {color};"
        semantic_attributes = {
            "data-ewoks-link-id": link_id,
            "data-ewoks-source-node-id": source_node_id,
            "data-ewoks-source-output": source_output,
            "data-ewoks-target-node-id": target_node_id,
            "data-ewoks-target-input": target_input,
        }
        attr.update(
            {
                name: value
                for name, value in semantic_attributes.items()
                if value is not None
            }
        )
        if map_all_data:
            attr["data-ewoks-map-all-data"] = "true"
        super().__init__(tag="path", css_class="link", attr=attr)

    def _path_data(self, points: list[dict], routing: str | None = None) -> str:
        if not points:
            return ""

        if routing == "SPLINES" and len(points) >= 3:
            return self._rounded_path_data(points)

        commands = [f"M {points[0]['x']} {points[0]['y']}"]
        commands.extend(f"L {point['x']} {point['y']}" for point in points[1:])
        return " ".join(commands)

    def _rounded_path_data(self, points: list[dict]) -> str:
        radius = 20.0
        commands = [f"M {points[0]['x']} {points[0]['y']}"]

        for index in range(1, len(points) - 1):
            previous = points[index - 1]
            current = points[index]
            following = points[index + 1]

            before = self._point_towards(current, previous, radius)
            after = self._point_towards(current, following, radius)
            commands.append(f"L {before['x']} {before['y']}")
            commands.append(self._curve_command(before, current, after))

        last = points[-1]
        commands.append(f"L {last['x']} {last['y']}")
        return " ".join(commands)

    def _point_towards(self, source: dict, target: dict, max_distance: float) -> dict:
        dx = target["x"] - source["x"]
        dy = target["y"] - source["y"]
        distance = (dx * dx + dy * dy) ** 0.5
        if distance == 0:
            return {"x": source["x"], "y": source["y"]}

        ratio = min(max_distance, distance / 2) / distance
        return {
            "x": source["x"] + dx * ratio,
            "y": source["y"] + dy * ratio,
        }

    def _curve_command(self, start: dict, control: dict, end: dict) -> str:
        c1 = {
            "x": start["x"] + (control["x"] - start["x"]) * 2 / 3,
            "y": start["y"] + (control["y"] - start["y"]) * 2 / 3,
        }
        c2 = {
            "x": end["x"] + (control["x"] - end["x"]) * 2 / 3,
            "y": end["y"] + (control["y"] - end["y"]) * 2 / 3,
        }
        return f"C {c1['x']} {c1['y']} {c2['x']} {c2['y']} {end['x']} {end['y']}"
