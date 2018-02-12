# dependency-graph

A python script to show the "include" dependency of C++ classes.

It is useful to check the presence of circular dependencies.

## Manual

```
usage: dependency_graph.py [-h] [-f {bmp,gif,jpg,png,pdf,svg}] [-v] [-c]
                           folder output

positional arguments:
  folder                Path to the folder to scan
  output                Path of the output file without the extension

optional arguments:
  -h, --help            show this help message and exit
  -f {bmp,gif,jpg,png,pdf,svg}, --format {bmp,gif,jpg,png,pdf,svg}
                        Format of the output
  -v, --view            View the graph
  -c, --cluster         Create a cluster for each subfolder
```

## Examples

Example of a graph produced by the script:

![Example 1](https://github.com/pvigier/dependency-graph/raw/master/examples/example1.png)

Graph produced for the same project with clusters (`-c`):

![Example 2](https://github.com/pvigier/dependency-graph/raw/master/examples/example2.png)