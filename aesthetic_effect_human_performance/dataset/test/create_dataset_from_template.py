import os
import sys
from xml.etree import ElementTree as ET

T1_GT2 = {
    1: {"node_pair": ("E", "H"), "answer": 2, "ground_truth": [["E", "B", "H"]]},
    2: {"node_pair": ("R", "P"), "answer": 2, "ground_truth": [["R", "Q", "P"]]},
    3: {"node_pair": ("S", "T"), "answer": 2, "ground_truth": [["S", "F", "T"]]},
    4: {
        "node_pair": ("H", "C"),
        "answer": 2,
        "ground_truth": [["H", "G", "C"], ["C", "B", "H"]],
    },
    5: {"node_pair": ("A", "N"), "answer": 2, "ground_truth": [["A", "B", "N"]]},
}

T1_GT3 = {
    1: {"node_pair": ("A", "I"), "answer": 3, "ground_truth": [["A", "B", "H", "I"]]},
    2: {
        "node_pair": ("F", "I"),
        "answer": 3,
        "ground_truth": [["F", "B", "H", "I"], ["F", "G", "H", "I"]],
    },
    3: {
        "node_pair": ("R", "H"),
        "answer": 3,
        "ground_truth": [["R", "Q", "I", "H"], ["R", "J", "I", "H"]],
    },
    4: {
        "node_pair": ("E", "O"),
        "answer": 3,
        "ground_truth": [["E", "B", "N", "O"], ["E", "B", "C", "O"]],
    },
    5: {"node_pair": ("B", "Q"), "answer": 3, "ground_truth": [["B", "H", "I", "Q"]]},
}

T1_GT4 = {
    1: {
        "node_pair": ("A", "J"),
        "answer": 4,
        "ground_truth": [["A", "B", "H", "I", "J"]],
    },
    2: {
        "node_pair": ("C", "P"),
        "answer": 4,
        "ground_truth": [["C", "B", "H", "I", "P"], ["C", "G", "H", "I", "P"]],
    },
    3: {
        "node_pair": ("I", "O"),
        "answer": 4,
        "ground_truth": [
            ["I", "H", "B", "N", "O"],
            ["I", "H", "G", "C", "O"],
            ["I", "H", "B", "C", "O"],
        ],
    },
    4: {
        "node_pair": ("A", "P"),
        "answer": 4,
        "ground_truth": [["A", "B", "H", "I", "P"]],
    },
    5: {
        "node_pair": ("E", "Q"),
        "answer": 4,
        "ground_truth": [["E", "B", "H", "I", "Q"]],
    },
}

T1_GT5 = {
    1: {
        "node_pair": ("A", "R"),
        "answer": 5,
        "ground_truth": [
            ["A", "B", "H", "I", "J", "R"],
            ["A", "B", "H", "I", "Q", "R"],
        ],
    },
    2: {
        "node_pair": ("N", "R"),
        "answer": 5,
        "ground_truth": [
            ["N", "B", "H", "I", "J", "R"],
            ["N", "B", "H", "I", "Q", "R"],
        ],
    },
    3: {
        "node_pair": ("S", "Q"),
        "answer": 5,
        "ground_truth": [
            ["S", "F", "B", "H", "I", "Q"],
            ["S", "F", "G", "H", "I", "Q"],
        ],
    },
    4: {
        "node_pair": ("O", "J"),
        "answer": 5,
        "ground_truth": [
            ["O", "C", "B", "H", "I", "J"],
            ["O", "C", "G", "H", "I", "J"],
        ],
    },
    5: {
        "node_pair": ("E", "R"),
        "answer": 5,
        "ground_truth": [
            ["E", "B", "H", "I", "J", "R"],
            ["E", "B", "H", "I", "Q", "R"],
        ],
    },
}

T2_GT1 = {
    1: {"node_pair": ("A", "I"), "answer": 1, "ground_truth": [["H"]]},
    2: {"node_pair": ("E", "J"), "answer": 1, "ground_truth": [["H"], ["I"]]},
    3: {"node_pair": ("Q", "N"), "answer": 1, "ground_truth": [["H"], ["I"]]},
    4: {"node_pair": ("S", "R"), "answer": 1, "ground_truth": [["H"], ["I"]]},
    5: {"node_pair": ("R", "H"), "answer": 1, "ground_truth": [["I"]]},
}

T2_GT2 = {
    1: {
        "node_pair": ("S", "O"),
        "answer": 2,
        "ground_truth": [["N", "C"], ["B", "C"], ["B", "G"]],
    },
    2: {"node_pair": ("A", "H"), "answer": 2, "ground_truth": [["B", "G"], ["B", "F"]]},
    3: {"node_pair": ("N", "G"), "answer": 2, "ground_truth": [["B", "C"]]},
    4: {"node_pair": ("P", "J"), "answer": 2, "ground_truth": [["I", "Q"]]},
    5: {"node_pair": ("E", "T"), "answer": 2, "ground_truth": [["B", "F"]]},
}

T3_GT1 = {
    1: {"node_pair": ("A", "I"), "answer": 1, "ground_truth": [[["H", "I"]]]},
    2: {"node_pair": ("E", "J"), "answer": 1, "ground_truth": [[["H", "I"]]]},
    3: {"node_pair": ("Q", "N"), "answer": 1, "ground_truth": [[["H", "I"]]]},
    4: {"node_pair": ("S", "R"), "answer": 1, "ground_truth": [[["H", "I"]]]},
    5: {"node_pair": ("O", "H"), "answer": 1, "ground_truth": [[["H", "I"]]]},
}

T3_GT2 = {
    1: {
        "node_pair": ("S", "O"),
        "answer": 2,
        "ground_truth": [[["N", "O"], ["S", "O"]]],
    },
    2: {
        "node_pair": ("P", "R"),
        "answer": 2,
        "ground_truth": [[["J", "R"], ["Q", "R"]], [["P", "I"], ["P", "Q"]]],
    },
    3: {
        "node_pair": ("A", "H"),
        "answer": 2,
        "ground_truth": [[["B", "H"], ["G", "H"]]],
    },
    4: {
        "node_pair": ("I", "R"),
        "answer": 2,
        "ground_truth": [[["J", "R"], ["Q", "R"]]],
    },
    5: {
        "node_pair": ("H", "B"),
        "answer": 2,
        "ground_truth": [[["H", "B"], ["H", "G"]]],
    },
}

T3_GT3 = {
    1: {
        "node_pair": ("J", "R"),
        "answer": 3,
        "ground_truth": [[["J", "R"], ["J", "Q"], ["J", "I"]]],
    },
    2: {
        "node_pair": ("E", "N"),
        "answer": 3,
        "ground_truth": [
            [["N", "O"], ["N", "C"], ["N", "B"]],
            [["O", "C"], ["N", "C"], ["N", "B"]],
            [["N", "B"], ["C", "B"], ["C", "G"]],
        ],
    },
    3: {
        "node_pair": ("A", "T"),
        "answer": 3,
        "ground_truth": [
            [["A", "B"], ["A", "E"], ["A", "S"]],
            [["T", "F"], ["T", "B"], ["T", "G"]],
        ],
    },
    4: {
        "node_pair": ("F", "C"),
        "answer": 3,
        "ground_truth": [[["N", "B"], ["C", "B"], ["C", "G"]]],
    },
    5: {
        "node_pair": ("I", "Q"),
        "answer": 3,
        "ground_truth": [
            [["I", "J"], ["I", "P"], ["I", "Q"]],
            [["I", "J"], ["P", "Q"], ["I", "Q"]],
        ],
    },
}


def modify_graphml_file(graphml_file, node_pair, output_graph_name):
    with open(graphml_file, "r", encoding="utf-8") as file:
        tree = ET.parse(file)
        root = tree.getroot()
        ns = {"y": "http://www.yworks.com/xml/graphml"}

        def find_shapenode_by_label(label):
            for shapenode in root.findall(".//y:ShapeNode", ns):
                nodelabel = shapenode.find("y:NodeLabel", ns)
                if nodelabel is not None and nodelabel.text == label:
                    return shapenode
            return None

        node1_label, node2_label = node_pair
        shapenode1 = find_shapenode_by_label(node1_label)
        shapenode2 = find_shapenode_by_label(node2_label)

        if shapenode1 is None or shapenode2 is None:
            raise Exception(
                f"Error: Could not find shape nodes for labels '{node1_label}' and '{node2_label}' in the graphml file."
            )

        for shapenode in [shapenode1, shapenode2]:
            fill = shapenode.find("y:Fill", ns)
            if fill is not None:
                fill.set("color", "#000000")
            nodelabel = shapenode.find("y:NodeLabel", ns)
            if nodelabel is not None:
                nodelabel.set("textColor", "#FFFFFF")

        tree.write(output_graph_name, encoding="utf-8", xml_declaration=True)


def create_dataset_from_template(template_file):
    file_name = os.path.basename(template_file)
    graph_name = file_name.removesuffix(".graphml")

    tasks = {
        "task1": [T1_GT2, T1_GT3, T1_GT4, T1_GT5],
        "task2": [T2_GT1, T2_GT2],
        "task3": [T3_GT1, T3_GT2, T3_GT3],
    }
    for task_name, task_gts in tasks.items():
        for task_gt in task_gts:
            for task_variation, task_data in task_gt.items():
                node_pair = task_data["node_pair"]
                answer = task_data["answer"]
                # ground_truth = task_data["ground_truth"]

                graph_file_name = (
                    f"{graph_name}_{task_name}_gt{answer}_PAIR{task_variation}.graphml"
                )

                modify_graphml_file(template_file, node_pair, graph_file_name)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python create_dataset_from_template.py FILE...\n - create dataset files from [multiple] .graphml files"
        )
        sys.exit(1)

    input_files = sys.argv[1:]
    for input_file in input_files:
        if not input_file.endswith(".graphml"):
            print("Error: no .graphml file provided")
            sys.exit(1)

    for input_file in input_files:
        try:
            create_dataset_from_template(input_file)
        except Exception as e:
            print(f"Error processing file {input_file}: {e}")
            sys.exit(1)
