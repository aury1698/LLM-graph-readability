import re
import sys
from xml.etree.ElementTree import Element, SubElement, ElementTree

CIRCLE_RADIUS = 15.0

def adjust_edge_coordinates(x, y):
    """
    Adjusts the coordinates of the edge points to match the center of the node.
    The adjustment is based on the radius of the circle (CIRCLE_RADIUS).
    This is necessary because the yEd graph editor uses the top-left corner of the node
    as the reference point for the edge coordinates.
    """
    return x + CIRCLE_RADIUS, y + CIRCLE_RADIUS

def parse_graphed_file(file_path):
    """
    Parses a .g file (GraphEd format) and extracts nodes and edges with their positions and bends.
    - Node positions (NP) are used as node coordinates.
    - Edge points (EL) are used for bends: only intermediate points are used as bends.
    """
    nodes = {}
    edges = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Regex for node and edge lines
    node_re = re.compile(r'^(\d+)\s+\{\$.*?NP\s+(\d+)\s+(\d+).*?\$\}"([^"]+)"')
    edge_re = re.compile(r'^\s*(\d+)\s+\{\$.*?EL\s+((?:\d+\s+)+)\$\}"')

    current_node = None
    for line in lines:
        line = line.strip()
        if not line or line == ';' or line == 'END':
            current_node = None
            continue
        node_match = node_re.match(line)
        if node_match:
            # Extract node id, position, and label
            node_id = int(node_match.group(1))
            x = float(node_match.group(2))
            y = float(node_match.group(3))
            label = node_match.group(4).replace("\\n", "\n")
            nodes[node_id] = {'label': label, 'x': x, 'y': y}
            current_node = node_id
            continue
        edge_match = edge_re.match(line)
        if edge_match and current_node is not None:
            # Extract edge target and all EL points
            target_id = int(edge_match.group(1))
            coords = list(map(int, edge_match.group(2).split()))
            bends = []
            # Only use intermediate points as bends (exclude first and last)
            if len(coords) > 4:
                for i in range(2, len(coords)-2, 2):
                    bends.append((coords[i], coords[i+1]))
            edges.append((current_node, target_id, bends))
    return nodes, edges

def write_graphml_yed_classic(nodes, edges, filename):
    """
    Writes a yEd-compatible GraphML file in the 'classic' format.
    - Node positions and labels are preserved.
    - Edges include bends if present.
    - Output is compatible with yEd Live and Desktop.
    """
    NS = {
        'xmlns': "http://graphml.graphdrawing.org/xmlns",
        'xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'y': "http://www.yworks.com/xml/graphml"
    }
    graphml = Element('graphml', {
        'xmlns': NS['xmlns'],
        'xmlns:xsi': NS['xsi'],
        'xmlns:y': NS['y'],
        'xsi:schemaLocation': NS['xmlns'] + " http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd"
    })
    # yEd keys for node and edge graphics
    SubElement(graphml, 'key', id="d0", attrib={'for':"node", 'yfiles.type':"nodegraphics"})
    SubElement(graphml, 'key', id="d1", attrib={'for':"edge", 'yfiles.type':"edgegraphics"})

    graph = SubElement(graphml, 'graph', edgedefault="undirected")

    for node_id, data in nodes.items():
        node = SubElement(graph, 'node', id=f"n{node_id}")
        data_el = SubElement(node, 'data', key="d0")
        shape_node = SubElement(data_el, '{%s}ShapeNode' % NS['y'])
        # Node geometry: position and size
        SubElement(shape_node, '{%s}Geometry' % NS['y'], x=str(data['x']), y=str(data['y']), width=str(CIRCLE_RADIUS * 2), height=str(CIRCLE_RADIUS * 2))
        # Node fill: white
        SubElement(shape_node, '{%s}Fill' % NS['y'], color="#FFFFFF", transparent="false")
        # Node border: black
        SubElement(shape_node, '{%s}BorderStyle' % NS['y'], color="#000000", type="line", width="2.0")
        # Node label: centered, bold, black
        SubElement(
            shape_node,
            '{%s}NodeLabel' % NS['y'],
            textColor="#000000",
            alignment="center",
            verticalTextPosition="center",
            fontSize="14",
            fontStyle="bold",
            layoutParameter="{x:Static yx:StretchNodeLabelModel.Center}"
        ).text = data['label']
        # Node shape: ellipse
        SubElement(shape_node, '{%s}Shape' % NS['y'], type="ellipse")

    for i, (src, tgt, bends) in enumerate(edges):
        edge = SubElement(graph, 'edge', id=f"e{i}", source=f"n{src}", target=f"n{tgt}")
        data_el = SubElement(edge, 'data', key="d1")
        polyline = SubElement(data_el, '{%s}PolyLineEdge' % NS['y'])
        # Add bends if present
        if bends:
            path = SubElement(polyline, '{%s}Path' % NS['y'])
            for x, y in bends:
                # they need to be adjusted to the center of the node
                # because yEd uses the top-left corner of the node as the reference point
                x, y = adjust_edge_coordinates(x, y)
                SubElement(path, '{%s}Point' % NS['y'], x=str(x), y=str(y))
        # Edge style: black line, no arrows
        SubElement(polyline, '{%s}LineStyle' % NS['y'], color="#000000", type="line", width="2.0")
        SubElement(polyline, '{%s}Arrows' % NS['y'], source="none", target="none")
        SubElement(polyline, '{%s}EdgeLabel' % NS['y']).text = ""

    tree = ElementTree(graphml)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    print(f"GraphML yEd (classic) file written to: {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_graph_to_yed.py FILE...\n - convert [multiple] .g graph files to yEd GraphML format")
        sys.exit(1)

    input_files = sys.argv[1:]
    for input_file in input_files:
        if not input_file.endswith(".g"):
            print("Error: no .g graph file provided")
            sys.exit(1)

    for input_file in input_files:
        file_name = input_file.removesuffix(".g")

        nodes, edges = parse_graphed_file(input_file)
        write_graphml_yed_classic(nodes, edges, f"{file_name}.graphml")
