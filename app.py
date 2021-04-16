from flask import Flask,render_template, redirect, request, make_response
from base64 import b64encode
import ast
import io
import networkx
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_svg import FigureCanvasSVG


app = Flask(__name__)

@app.route("/")
def route():
    return redirect("/index")

@app.route("/index")
def home():
    return render_template("index.html")

@app.route("/module-1")
def module1():
    return render_template("module1.html")


@app.route("/module-2-Java")
def module2Java():
    return render_template("module2Java.html")

@app.route("/module-2-Python")
def module2Python():
    return render_template("module2Python.html")

@app.route("/module-2-Cpp")
def module2Cpp():
    return render_template("module2Cpp.html")

@app.route("/module-3",methods=("GET","POST"))
def module3():
    if(request.method=="GET"):
        return render_template("module3.html")

    if(request.method=="POST"):
        AAA=request.files.get("file")
        if(AAA is not None):
            codePy=io.BytesIO()
            AAA.save(codePy)
            codePy.seek(0)
            purePy=codePy.read()
            code_ast=ast.parse(purePy)
            imgPy=graficar(code_ast)
            
            return render_template("module3_r.html",image=b64encode(imgPy).decode())
            
    return ""

def graficar(code_ast):
    g=networkx.Graph()
    node_number=1
    g.add_node(node_number,Type='module',Name="Script" )
    node_number+=1
    for node in code_ast.body:
        if type(node) is ast.ClassDef:
            g.add_node(node_number,Type='class', Name=node.name)
            class_id=node_number
            node_number+=1
            g.add_edge(1,class_id)
            for node2 in node.body:
                ## dentro de este for
                if type(node2) is ast.FunctionDef:
                    g.add_node(node_number, Type='function', Name=node2.name)
                    function_id=node_number
                    node_number+=1
    
                    g.add_edge(class_id,function_id)
                    for node3 in node2.args.args:
                            g.add_node(node_number, Type='argument',Name=node3.arg)
                            g.add_edge(function_id,node_number)
                            node_number+=1
    
    
    module_nodes = [n for (n,ty) in \
    networkx.get_node_attributes(g,'Type').items() if ty == 'module']
    class_nodes = [n for (n,ty) in \
    networkx.get_node_attributes(g,'Type').items() if ty == 'class']
    function_nodes = [n for (n,ty) in \
    networkx.get_node_attributes(g,'Type').items() if ty == 'function']
    arg_nodes = [n for (n,ty) in \
    networkx.get_node_attributes(g,'Type').items() if ty == 'argument']
    
    fig=Figure(figsize=(12,12))
    axis=fig.add_subplot(1,1,1)
    pos = networkx.spring_layout(g)
    networkx.draw_networkx_nodes(g, pos, nodelist=module_nodes, \
    node_color='red', node_shape='o',ax=axis)
    networkx.draw_networkx_nodes(g, pos, nodelist=class_nodes, \
    node_color='blue', node_shape='o',ax=axis)
    networkx.draw_networkx_nodes(g, pos, nodelist=function_nodes, \
    node_color='purple', node_shape='s',ax=axis)
    networkx.draw_networkx_nodes(g, pos, nodelist=arg_nodes, \
    node_color='green', node_shape='s',ax=axis)
    networkx.draw_networkx_edges(g, pos, nodelist=arg_nodes, \
    ax=axis)
    labels={}

    for node in g.nodes(data=True):
        print(node)
        labels[node[0]]=node[1]["Name"]


    
    networkx.draw_networkx_labels(g,pos,labels,ax=axis)

    buffer=io.BytesIO()
    FigureCanvasSVG(fig).print_svg(buffer)
    buffer.seek(0)
    return buffer.read()

app.run(debug=True)

