from flask import Flask,render_template, redirect, request, make_response
import ast
import io
import networkx
import matplotlib.pyplot as plt

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
            response=make_response(imgPy)
            response.headers.set("Content-Type","image/png")
            ##response.headers.set("Content-Type","image/png")
            return response
            
    return ""

def graficar(code_ast):
    g=networkx.Graph()
    for node in ast.walk(code_ast):
        if type(node) is ast.Module:
            g.add_node(1)
            
        if type(node) is ast.ClassDef:
            g.add_node(2)

        g.add_edge(1,2)
        ## logica
        ## Encontrar nodos y dependiendo su tipo lo grafico
    networkx.draw(g)
    buffer=io.BytesIO()
    plt.savefig(buffer,format="png")
    buffer.seek(0)
    return buffer.read()

app.run(debug=True)
## capturar el archivo y pasarlo a string, luego procesarlo con ast

## tag html input file
## request post flask
code = """
class Ejemplo:
    def __init__(self):
        pass
print(1 + 2)
"""

## Request
##code_ast = ast.parse(code)

##or node in ast.walk(code_ast):
##    print(node)
"""
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    g.add_edge(1,3)
    g.add_edge(1,2)
    g.add_edge(2,3)
    for node in ast.walk(code_ast):
        pass
        ## logica
        ## Encontrar nodos y dependiendo su tipo lo grafico
"""

