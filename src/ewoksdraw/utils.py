import warnings
from collections import defaultdict

from ewokscore.graph import TaskGraph

from .models import DataMapping


def get_valid_data_mappings(ewoks_graph: TaskGraph) -> list[DataMapping]:
    data_mappings: list[DataMapping] = []
    for source, target, link_attrs in ewoks_graph.graph.edges(data=True):
        if link_attrs.get("map_all_data", False):
            warnings.warn(
                f"Ewoks link {source!r} -> {target!r} uses 'map_all_data', which "
                "is not yet supported.",
                UserWarning,
                stacklevel=2,
            )

        for mapping in link_attrs.get("data_mapping", []):
            source_output = mapping.get("source_output")
            if source_output is None:
                warnings.warn(
                    f"Data mapping on Ewoks link {source!r} -> {target!r} has no "
                    "'source_output', which is not yet supported.",
                    UserWarning,
                    stacklevel=2,
                )
                continue

            data_mappings.append(
                DataMapping(
                    source=source,
                    target=target,
                    source_output=source_output,
                    target_input=mapping["target_input"],
                )
            )

    return data_mappings


def get_edge_sources_and_targets(
    graph: TaskGraph,
) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    data_mappings = get_valid_data_mappings(graph)
    sources: dict[str, list[str]] = defaultdict(list[str])
    targets: dict[str, list[str]] = defaultdict(list[str])
    for mapping in data_mappings:
        sources[mapping.source].append(mapping.source_output)
        targets[mapping.target].append(mapping.target_input)

    return sources, targets
