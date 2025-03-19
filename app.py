from flask import Flask,render_template,request,redirect
import mysql.connector

app = Flask(__name__)
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="citas"
    )

@app.route("/")
def Raiz():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM citas")
    datos = cursor.fetchall()
    Clientes =[
        {
            'Numero' : dato[0],
            'Cliente' : dato[1],
            'Cita' : dato[2],
            'Fecha' : dato[3],
            'Estado' : dato[4]
        }
        for dato in datos
    ]
    return render_template("index.html", Clientes = Clientes)

@app.route("/Editar", methods=["POST"])
def editar_producto():
    Numero = request.form["Numero"]
    Estado = request.form["Estado"]
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE citas SET Estado = %s WHERE Numero = %s",(Estado,Numero))
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/Eliminar/<Numero>")
def Eliminar(Numero):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM citas WHERE Numero = %s", (Numero,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/RegistrarCita", methods=["POST"])
def Solicitar():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO citas (Numero,Cliente,Cita,Fecha,Estado) VALUES (%s,%s,%s,%s,%s)",(request.form["Numero"], request.form["Nombre"],request.form["Cita"],request.form["Fecha"],"PENDIENTE"))
    conn.commit()
    conn.close()
    return redirect("/")

