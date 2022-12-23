import os
import re
import codecs
from collections import defaultdict
from graphviz import Digraph

include_regex = re.compile('#include\s+["<"](.*)[">]')
valid_headers = [['.h', '.hpp'], 'red']
valid_sources = [['.c', '.cc', '.cpp'], 'blue']
valid_extensions = valid_headers[0] + valid_sources[0]

def normalize(path):
	""" Return the name of the node that will represent the file at path. """
	filename = os.path.basename(path)
	end = filename.rfind('.')
	end = end if end != -1 else len(filename)
	return filename[:end]

def get_extension(path):
	""" Return the extension of the file targeted by path. """
	return path[path.rfind('.'):]

def find_all_files(path, recursive=True):
	"""
	Return a list of all the files in the folder.
	If recursive is True, the function will search recursively.
	"""
	files = []
	for entry in os.scandir(path):
		if entry.is_dir() and recursive:
			files += find_all_files(entry.path)
		elif get_extension(entry.path) in valid_extensions:
			files.append(entry.path)
	return files

def find_neighbors(path):
	""" Find all the other nodes included by the file targeted by path. """
	f = codecs.open(path, 'r', "utf-8", "ignore")
	code = f.read()
	f.close()
	return [normalize(include) for include in include_regex.findall(code)]

def create_graph(folder, create_cluster, label_cluster, strict):
	""" Create a graph from a folder. """
	# Find nodes and clusters
	files = find_all_files(folder)
	folder_to_files = defaultdict(list)
	for path in files:
		folder_to_files[os.path.dirname(path)].append(path)
	nodes = {normalize(path) for path in files}
	# Create graph
	graph = Digraph(strict=strict)
	# Find edges and create clusters
	for folder in folder_to_files:
		with graph.subgraph(name='cluster_{}'.format(folder)) as cluster:
			for path in folder_to_files[folder]:
				color = 'black'
				node = normalize(path)
				ext = get_extension(path)
				if ext in valid_headers[0]:
					color = valid_headers[1]
				if ext in valid_sources[0]:
					color = valid_sources[1]
				if create_cluster:
					cluster.node(node)
				else:
					graph.node(node)
				neighbors = find_neighbors(path)
				for neighbor in neighbors:
					if neighbor != node and neighbor in nodes:
						graph.edge(node, neighbor, color=color)
			if create_cluster and label_cluster:
				cluster.attr(label=folder)
	return graph
