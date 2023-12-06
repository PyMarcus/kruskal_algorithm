from flask import Flask, render_template, send_from_directory, request, redirect
from .graph import read_graph_from_file, visualize_graph, kruskal_mst
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('form.html')


@app.route('/upload', methods=["POST"])
def index_post():
    print(request.files)
    if "file" not in request.files:
        return
    file = request.files['file']
    file.save("input/" + file.filename)
    return redirect("/kruskal")


@app.route('/kruskal')
def kruskal():
    filename = "input/graph.txt"
    graph = read_graph_from_file(filename)
    visualize_graph(graph)
    kruskal_mst(graph)
    with open("static/weight.txt", 'r') as f:
        w = f.read()
    return render_template('index.html', weight=w)
