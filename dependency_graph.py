import os
import re
import argparse
from collections import defaultdict
from graphviz import Digraph

include_regex = re.compile('#include\s+["<"](.*)[">]')
valid_extensions = ['.cpp', '.h']

def normalize(path):
	filename = os.path.basename(path)
	end = filename.rfind('.')
	end = end if end != -1 else len(filename)
	return filename[:end]

def get_extension(path):
	return path[path.rfind('.'):]

def find_all_files(path, recursive=True):
	files = []
	for entry in os.scandir(path):
		if entry.is_dir() and recursive:
			files += find_all_files(entry.path)
		elif get_extension(entry.path) in valid_extensions:
			files.append(entry.path)
	return files

def find_neighbors(path):
	f = open(path)
	code = f.read()
	return [normalize(include) for include in include_regex.findall(code)]

def create_graph(folder):
	# Find nodes and clusters
	files = find_all_files(folder)
	folder_to_files = defaultdict(list)
	for path in files:
		folder_to_files[os.path.dirname(path)].append(path)
	nodes = {normalize(path) for path in files}
	# Create graph
	graph = Digraph()
	# Find edges and create clusters
	for folder in folder_to_files:
		with graph.subgraph(name='cluster_{}'.format(folder)) as cluster:
			cluster_edges = []
			for path in folder_to_files[folder]:
				node = normalize(path)
				cluster.node(node)
				neighbors = find_neighbors(path)
				for neighbor in neighbors:
					if neighbor != node and neighbor in nodes:
						graph.edge(node, neighbor)
			cluster.edges(cluster_edges)
	return graph

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('folder', help='Path to the folder to scan')
	parser.add_argument('output', help='Path of the output file without the extension')
	parser.add_argument('-f', '--format', help='Format of the output', default='pdf', \
		choices=['bmp', 'gif', 'jpg', 'png', 'pdf', 'svg'])
	parser.add_argument('-v', '--view', action='store_true', help='View the graph')
	args = parser.parse_args()
	graph = create_graph(args.folder)
	graph.format = args.format
	graph.render(args.output, cleanup=True, view=args.view)