import collections

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.path import Path

from ewoksdraw.dev_fake_workflow import complex_workflow_with_pos


def _find_and_break_cycles(tasks: list, links: list) -> list:
    """Finds and returns a list of links with cycle-causing back-edges removed."""
    task_ids = {task["id"] for task in tasks}
    graph = collections.defaultdict(list)
    for link in links:
        graph[link["source"]["task_id"]].append(link["target"]["task_id"])

    cut_edges = set()
    # A standard DFS to find back-edges
    path = set()
    visited = set()

    def dfs(node):
        visited.add(node)
        path.add(node)
        for neighbor in graph.get(node, []):
            if neighbor in path:
                cut_edges.add(tuple(sorted((node, neighbor))))
            if neighbor not in visited:
                dfs(neighbor)
        path.remove(node)

    for node in task_ids:
        if node not in visited:
            dfs(node)

    return [
        link
        for link in links
        if tuple(sorted((link["source"]["task_id"], link["target"]["task_id"])))
        not in cut_edges
    ]


def _calculate_layers(tasks: list, links: list) -> list[list[str]]:
    """Calculates layers for a guaranteed acyclic graph."""
    task_ids = {task["id"] for task in tasks}
    graph = collections.defaultdict(list)
    in_degree = {task_id: 0 for task_id in task_ids}

    for link in links:
        source, target = link["source"]["task_id"], link["target"]["task_id"]
        if source in task_ids and target in task_ids:
            graph[source].append(target)
            in_degree[target] += 1

    queue = collections.deque([tid for tid in task_ids if in_degree[tid] == 0])
    layers = []
    while queue:
        layer = sorted(list(queue))  # Sort for deterministic output
        queue.clear()
        for node in layer:
            for neighbor in graph.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        layers.append(layer)
    return layers


def calculate_final_layout(workflow_dict, width=800, padding=50):
    """
    Calculates a stable, deterministic, hierarchical layout, even for cyclic graphs.
    """
    tasks = workflow_dict["workflow"]["tasks"]
    links = workflow_dict["workflow"]["links"]
    task_map = {task["id"]: task for task in tasks}

    # 1. Create a temporary acyclic version of the graph
    acyclic_links = _find_and_break_cycles(tasks, links)

    # 2. Calculate column/layer structure
    layers = _calculate_layers(tasks, acyclic_links)

    # 3. Assign final positions based on the hierarchical structure
    pos = {}
    num_layers = len(layers)
    column_width = (
        (width - 2 * padding) / max(1, num_layers - 1) if num_layers > 1 else 0
    )

    for i, layer in enumerate(layers):
        # Calculate total height of the column for vertical centering
        layer_height = sum(task_map[tid].get("size_box", [0, 100])[1] for tid in layer)
        layer_height += (len(layer) - 1) * 50  # Padding between nodes

        current_y = -layer_height / 2
        for task_id in layer:
            task = task_map[task_id]
            task_height = task.get("size_box", [0, 100])[1]
            pos[task_id] = (padding + i * column_width, current_y + task_height / 2)
            current_y += task_height + 50

    return pos


def render_final_workflow(workflow_dict, pos):
    """
    Renders a final, clean workflow, routing back-edges over the top.
    """
    tasks = workflow_dict["workflow"]["tasks"]
    links = workflow_dict["workflow"]["links"]
    task_map = {task["id"]: task for task in tasks}

    fig, ax = plt.subplots(figsize=(16, 10))

    # --- Draw Task Boxes and Labels ---
    # (This part is unchanged)
    for task_id, task_pos in pos.items():
        task = task_map[task_id]
        width, height = task.get("size_box", [150, 60])
        x, y = task_pos
        ax.add_patch(
            patches.Rectangle(
                (x - width / 2, y - height / 2),
                width,
                height,
                facecolor="#d6f2d6",
                edgecolor="black",
                lw=1.5,
                zorder=5,
            )
        )
        ax.text(x, y, task["name"], ha="center", va="center", fontsize=10, zorder=10)

    # --- Find the highest point of the diagram for routing back-edges ---
    max_y = max(
        p[1] + task_map[tid].get("size_box", [0, 60])[1] / 2 for tid, p in pos.items()
    )

    # --- Draw Links with specialized routing ---
    for link in links:
        source_id = link["source"]["task_id"]
        target_id = link["target"]["task_id"]
        source_task = task_map[source_id]
        target_task = task_map[target_id]

        sx, sy = pos[source_id]
        tx, ty = pos[target_id]
        sw, sh = source_task.get("size_box", [150, 60])
        tw, th = target_task.get("size_box", [150, 60])

        is_back_edge = sx > tx

        if not is_back_edge:
            # --- STRATEGY 1: Standard S-Curve for Forward Links ---
            output_idx = source_task["outputs"].index(link["source"]["output_name"])
            start_y = sy - sh / 2 + source_task["outputs_pos"][output_idx] * sh
            start_pos = (sx + sw / 2, start_y)

            input_idx = target_task["inputs"].index(link["target"]["input_name"])
            end_y = ty - th / 2 + target_task["inputs_pos"][input_idx] * th
            end_pos = (tx - tw / 2, end_y)

            offset = abs(start_pos[0] - end_pos[0]) * 0.4
            control1 = (start_pos[0] + offset, start_pos[1])
            control2 = (end_pos[0] - offset, end_pos[1])

        else:
            # --- STRATEGY 2: "Over the Top" Arc for Back-Edges ---
            # Connect from the top-middle of the boxes
            start_pos = (sx, sy + sh / 2)
            end_pos = (tx, ty + th / 2)

            # Control points go high above the diagram
            vertical_offset = max_y + 80  # Adjust this for more/less arc height
            control1 = (start_pos[0], vertical_offset)
            control2 = (end_pos[0], vertical_offset)

        # Create the path and draw the arrow patch
        path_data = [
            (Path.MOVETO, start_pos),
            (Path.CURVE4, control1),
            (Path.CURVE4, control2),
            (Path.CURVE4, end_pos),
        ]
        codes, verts = zip(*path_data)
        path = Path(verts, codes)

        patch = patches.FancyArrowPatch(
            path=path,
            arrowstyle="-|>,head_length=0.6,head_width=0.3",
            facecolor="none",
            edgecolor="gray",
            lw=1.5,
        )
        ax.add_patch(patch)

    # Final plot setup
    ax.autoscale()
    ax.set_aspect("equal", adjustable="box")
    plt.title("Final Workflow Layout", size=15)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    plt.show()


# 1. Calculate positions using NetworkX
positions = calculate_final_layout(complex_workflow_with_pos)
print(positions)

# 2. Render the layout with our custom drawing function
render_final_workflow(complex_workflow_with_pos, positions)
