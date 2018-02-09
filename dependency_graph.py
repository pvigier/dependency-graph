import os
import re
import argparse
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

def create_graph(folder):
	files = find_all_files(folder)
	# Create graph
	graph = Digraph()
	# Add nodes
	nodes = [normalize(path) for path in files]
	for node in nodes:
		graph.node(node)
	# Add edges
	for path, node in zip(files, nodes):
		f = open(path)
		code = f.read()
		for include in include_regex.findall(code):
			neighbor = normalize(include)
			if neighbor != node and neighbor in nodes:
				graph.edge(node, neighbor)
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