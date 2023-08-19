from flask import Flask,render_template,request,redirect, session,url_for,flash
from flask_mysqldb import MySQL
from functools import wraps

app= Flask(__name__,static_folder='static',template_folder='templates')

app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="dbcentromedico"

app.secret_key='mysecretkey'

mysql=MySQL(app)

@app.route('/')
def index():
    return render_template('login.html')

def login_required(f):
    @wraps(f)
    def decorated_fuction(*args, **kwargs):
        if 'rfc_user' not in session:
            return render_template('login.html')
        return f(*args, **kwargs)
    return decorated_fuction


@app.route('/iniciar', methods=['POST'])
def iniciar():
    if request.method == 'POST':
        txtrfc2 = request.form['txtrfc2']
        txtpassword2 = request.form['txtpassword2']
        CS = mysql.connection.cursor()

        consulta = 'select rfcmed from admedicos where rfcmed = %s and contrasena = %s'
        CS.execute(consulta, (txtrfc2, txtpassword2))
        resultado = CS.fetchone()
        
        if resultado is not None:
            session['rfc_user'] = txtrfc2
            flash('BIENVENIDO')
            return redirect(url_for('registrarMedico'))
        else:
            return redirect(url_for('login'))

        
@app.route('/irarp')
def irarp():
    return render_template('registrarPaciente.html')

        
@app.route('/guardarpaciente',methods=['POST'])
@login_required
def guardar():
    
    if request.method == 'POST':
        nombre= request.form['txtpac']
        fecha= request.form['fecha']
        enfermedades= request.form['enfermedades']
        alergias= request.form['alergias']
        antecedentes= request.form['antecedentes']
        medico= request.form['medicoAtendio']
        CS = mysql.connection.cursor()
        CS.execute('insert into adpac (nombreP,fecha_nac,encronias,alergias,antecedentes,medicoAtendio) values(%s,%s,%s,%s,%s,%s)',(nombre,fecha,enfermedades,alergias,antecedentes,medico))
        mysql.connection.commit()

    flash('Usuario guardado')
    return render_template('registrarPaciente.html')

@app.route('/editarpaciente')
@login_required
def editarpaciente():
    return render_template('editarPaciente.html')

@app.route('/cambiarPaciente',methods=['POST'])
@login_required
def cambiarPaciente():
    if request.method == 'POST':
        nombreEdit= request.form['pacEdit']
        newnombre= request.form['newnombre']
        newfecha= request.form['newfecha']
        newenfermedades= request.form['newenfermedades']
        newalergias= request.form['newalergias']
        newantecedentes= request.form['newantecedentes']
        newmedico= request.form['newmedicoAtendio']
        CS= mysql.connection.cursor()
        CS.execute("UPDATE adpac SET nombreP=%s, fecha_nac=%s, encronias=%s, alergias=%s, antecedentes=%s, medicoAtendio=%s WHERE nombreP=%s", (newnombre,newfecha,newenfermedades,newalergias,newantecedentes,newmedico,nombreEdit))
        
    flash('Usuario modificado')
    return render_template('registrarPaciente.html')

@app.route('/eliminarpaciente')
@login_required
def eliminarpaciente():
    return render_template('eliminarPaciente.html')

@app.route('/delete',methods=['POST'])
@login_required
def delate():
    if request.method == 'POST':
        pacEli= request.form['pacEli']
        curactualizar = mysql.connection.cursor()
        curactualizar.execute('delete from adpac where nombreP=%s', (pacEli, ))
        mysql.connection.commit()

    flash('Usuario eliminado')
    return render_template('registrarPaciente.html')

#CONFIGURACION DE MEDICO

@app.route('/registrarMedico')
@login_required
def registrarMedico():
    return render_template('registrarMedico.html')

@app.route('/guardarmedico',methods=['POST'])
@login_required
def guardarmedico():
    if request.method == 'POST':
        rfcmed= request.form['rfcMed']
        nombremed= request.form['nombreMed']
        cedulamed= request.form['cedulaMed']
        correomed= request.form['correoMed']
        contrasenamed= request.form['contraMed']
        rolmed= request.form['Rol']
        CS = mysql.connection.cursor()
        CS.execute('insert into admedicos(rfcmed,nombre,cedula,correo,contrasena,rol) values(%s,%s,%s,%s,%s,%s)',(rfcmed,nombremed,cedulamed,correomed,contrasenamed,rolmed))
        mysql.connection.commit()
    flash('Medico Modificado Correctamente')
    return render_template('registrarPaciente.html')

@app.route('/eliminarmedico')
@login_required
def eliminarmedico():
    return render_template('eliminarMedico.html')

@app.route('/deletemedico',methods=['POST'])
@login_required
def delatemedico():
    if request.method == 'POST':
        medEli= request.form['medEli']
        curactualizar = mysql.connection.cursor()
        curactualizar.execute('delete from admedicos where nombre=%s', (medEli, ))
        mysql.connection.commit()

    flash('Medico Eliminado Correctamente')
    return render_template('registrarPaciente.html')

@app.route('/editarmedico')
@login_required
def editarmedico():
    return render_template('editarMedico.html')

@app.route('/cambiarMedico',methods=['POST'])
@login_required
def cambiarMedico():
    if request.method == 'POST':
        medEdit= request.form['medEdit']
        newnombremed= request.form['newnombreMed']
        newcedulamed= request.form['newcedulaMed']
        newcorreomed= request.form['newcorreoMed']
        newcontrasenamed= request.form['newcontraMed']
        newrolmed= request.form['newRol']
        CS= mysql.connection.cursor()
        CS.execute("UPDATE admedicos SET nombre=%s, cedula=%s, correo=%s, contrasena=%s, rol=%s WHERE nombre=%s", (newnombremed,newcedulamed,newcorreomed,newcontrasenamed,newrolmed,medEdit))
        
    flash('Usuario modificado correctamente')
    return render_template('registrarPaciente.html')

@app.route('/realizarconsulta')
@login_required
def realizarconsulta():
    return render_template('generarConsulta.html')

@app.route('/guardarconsulta',methods=['POST'])
@login_required
def guardarconsulta():
    if request.method == 'POST':
        nombrepaciente= request.form['namepa']
        fechap= request.form['fechap']
        pesop= request.form['pesop']
        alturap= request.form['alturap']
        temperaturap= request.form['temperaturap']
        latidos= request.form['latidos']
        glucosa= request.form['glucosa']
        sintomas= request.form['sintomas']
        diagnostico= request.form['diagnostico']
        tratamiento= request.form['tratamiento']
        medicoate= request.form['medicoate']
        CS = mysql.connection.cursor()
        CS.execute('insert into pacconsultas (nombre,fecha,peso,altura,temperatura,latidos,glucosa,sintomas,diagnostico,tratamiento,medico) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(nombrepaciente,fechap,pesop,alturap,temperaturap,latidos,glucosa,sintomas,diagnostico,tratamiento,medicoate))
        mysql.connection.commit()

    flash('Consulta guardada')
    return render_template('registrarPaciente.html')

@app.route('/buscarcon')
@login_required
def buscarcon():
    return render_template('buscarPacientes.html')


@app.route('/consultarPaciente', methods=['POST'])
@login_required
def consultarPaciente():
    if request.method == 'POST':
        nommedi= request.form['nommedi']
        curselect=mysql.connection.cursor()
        curselect.execute('select * from pacconsultas where medico=%s', (nommedi, ))
        consulta=curselect.fetchall()
        return render_template('consultas.html',consultam=consulta)

@app.route('/iracerrar')
@login_required
def iracerrar():
    return render_template('cerrarSesion.html')

@app.route('/cerrarsesion',methods=['POST'])
def cerrarsesion():
    if request.method == 'POST':
        session.pop('rfc_user', None)
        return redirect(url_for('index'))



if __name__== '__main__':
    app.run(port= 8000, debug=True)