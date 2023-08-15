
from flask import Flask,render_template,request,redirect,url_for,flash
from flask_mysqldb import MySQL



# inicializamos el servidor flask
app= Flask(__name__,static_folder='static',template_folder='templates')

#configuraciones para la conexion a la BD
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="dbcentromedico"

app.secret_key='mysecretkey'

mysql=MySQL(app)



#declaramos una ruta

#ruta index o principal http://localhost:5000
#la ruta se compone de nombre y la funcion
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/registrarm')
def registrarm():
    return render_template('adMedicos.html')

#@app.route('/registrarc/<id>')
#def registrarc(id):
#    return render_template('registrarCon.html',id)

@app.route('/guardarc/<id>', methods=['GET', 'POST'])
def guardarc(id):
    if request.method == 'POST':
        # ... (your existing POST handling code)
        flash('Consulta guardada')
        return render_template("registrarCon.html", id=id) 

@app.route('/registrarp')
def registrarp():
    return render_template('registrarPac.html')

@app.route('/conpac')
def concon():
    return render_template('consultarPac.html')

@app.route('/editar/<id>')
def editar(id):
    curEditar=mysql.connection.cursor()
    curEditar.execute('Select * from adpac where idPac=%s',(id,))
    consultid=curEditar.fetchone()

    return render_template("editarPac.html",album=consultid)



@app.route('/iniciar', methods=['POST'])
def iniciar():

        nombre= request.form['txtrfc']
        contrasena= request.form['txtpassword']
        CS = mysql.connection.cursor()
        CS.execute('select * from admedicos where rfcmed=(%s) and contrasena=(%s)', (nombre,contrasena))
       
        if (CS.rowcount == 1):
            
            flash('Acceso correcto')
            return render_template('registrarPac.html')
        else:
            flash('Usuario o contraseña incorrecta')
            return render_template('login.html')


@app.route('/guardarp',methods=['POST'])
def guardar():
    if request.method == 'POST':
        nombre= request.form['txtpac']
        fecha= request.form['fecha']
        enfermedades= request.form['enfermedades']
        alergias= request.form['alergias']
        antecedentes= request.form['antecedentes']
        CS = mysql.connection.cursor()
        CS.execute('insert into adpac (nombreP,fecha_nac,encronias,alergias,antecedentes) values(%s,%s,%s,%s,%s)',(nombre,fecha,enfermedades,alergias,antecedentes))
        mysql.connection.commit()
        
        CS.execute('SELECT LAST_INSERT_ID()')
        inserted_id = CS.fetchone()[0]
    
    flash('Paciente guardado')
    return render_template("registrarCon.html", id=inserted_id)


@app.route('/guardarc/<id>',methods=['POST'])
def guardarc(id):
    if request.method == 'POST':
        fecha= request.form['fecha']
        peso= request.form['peso']
        altura= request.form['altura']
        temperatura= request.form['temperatura']
        latidos= request.form['latidos']
        glucosa= request.form['glucosa']
        sintomas= request.form['sintomas']
        diagnostico= request.form['diagnostico']
        tratamiento= request.form['tratamiento']
        CS = mysql.connection.cursor()
        CS.execute('insert into adcon (cfecha,peso,altura,temperatura,latidos,glucosa,sintomas,diagnostico,tratamiento,idp) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(fecha,peso,altura,temperatura,latidos,glucosa,sintomas,diagnostico,tratamiento,id))
        mysql.connection.commit()

    flash('Consulta guardada')
    return render_template("registrarCon.html")


@app.route('/consultarM')
def consultarM():

    curselect=mysql.connection.cursor()
    curselect.execute('select * from admedicos')
    consulta=curselect.fetchall()
    print(consulta)
    return render_template('consultarMed.html',consultam=consulta)


@app.route('/guardarm',methods=['POST'])
def guardarm():
    if request.method == 'POST':
        rfc= request.form['rfc']
        nombre= request.form['nombre']
        cedula= request.form['cedula']
        correo= request.form['correo']
        password= request.form['password']
        rol= request.form['rol']
        CS = mysql.connection.cursor()
        CS.execute('insert into admedicos (rfcmed,nombre,cedula,correo,contrasena,rol) values(%s,%s,%s,%s,%s,%s)',(rfc,nombre,cedula,correo,password,rol))
        mysql.connection.commit()

    flash('Usuario guardado')
    return render_template("registrarCon.html")




@app.route('/consultarp', methods=['POST'])
def consultarp():
    if request.method == 'POST':
        nombre= request.form['nombre']
        curselect=mysql.connection.cursor()
        curselect.execute('select * from adpac where nombreP like %s',("%"+nombre+"%",))
        consulta=curselect.fetchall()
        print(consulta)
        return render_template('consultarPac.html',consultap=consulta)
    
    
@app.route('/editarPaciente/<id>', methods=['POST'])
def editarPaciente(id):
    if request.method == 'POST':
        nombreEdit= request.form['txtpacEdit']
        nombre= request.form['txtpac']
        fecha= request.form['fecha']
        enfermedades= request.form['enfermedades']
        alergias= request.form['alergias']
        antecedentes= request.form['antecedentes']
        CS= mysql.connection.cursor()
        CS.execute("UPDATE adpac SET nombreP=%s, fecha_nac=%s, encronias=%s, alergias=%s, antecedentes=%s WHERE nombreP=%s", (nombre,fecha,enfermedades,alergias,antecedentes,nombreEdit))
        

    return render_template('consultarPac.html')


@app.route('/concit/<id>')
def concit(id):

    curselect=mysql.connection.cursor()
    curselect.execute('select * from adcon where idp=%s',(id,))
    consulta=curselect.fetchall()
    print(consulta)
    return render_template('consultarTodo.html',consultap=consulta)

#ejecucion 
if __name__== '__main__':
    app.run(port= 5000, debug=True)

