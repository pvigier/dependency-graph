import argparse
from cpp_dependency_graph.graph import create_graph

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('folder', help='Path to the folder to scan')
	parser.add_argument('output', help='Path of the output file without the extension')
	parser.add_argument('-f', '--format', help='Format of the output', default='pdf', \
		choices=['bmp', 'gif', 'jpg', 'png', 'pdf', 'svg'])
	parser.add_argument('-v', '--view', action='store_true', help='View the graph')
	parser.add_argument('-c', '--cluster', action='store_true', help='Create a cluster for each subfolder')
	parser.add_argument('--cluster-labels', dest='cluster_labels', action='store_true', help='Label subfolder clusters')
	parser.add_argument('-s', '--strict', action='store_true', help='Rendering should merge multi-edges', default=False)
	args = parser.parse_args()
	graph = create_graph(args.folder, args.cluster, args.cluster_labels, args.strict)
	graph.format = args.format
	graph.render(args.output, cleanup=True, view=args.view)
