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

def is_authenticated():
    return 'authenticated' in session

@app.route('/')
def index():
    if is_authenticated():
        return render_template('dashboard.html')  # Change this to your authenticated page
    else:
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
    nombre = request.form['txtrfc']
    contrasena = request.form['txtpassword']
    CS = mysql.connection.cursor()
    CS.execute('select * from admedicos where rfcmed=(%s) and contrasena=(%s)', (nombre, contrasena))
    if CS.rowcount == 1:
        session['authenticated'] = True
        flash('Acceso correcto')
        return redirect(url_for('registrarp'))  # Redirect to authenticated page
    else:
        flash('Usuario o contraseña incorrecta')
        return render_template('login.html')

        



        
@app.route('/guardarpaciente',methods=['POST'])
def guardar():
    
    if is_authenticated():
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
   
    else:
        return render_template('login.html')
    


@app.route('/editarpaciente')
def editarpaciente():
    if is_authenticated():
        return render_template('editarPaciente.html')
       
    else:
        return render_template('login.html')




@app.route('/cambiarPaciente',methods=['POST'])
def cambiarPaciente():
    if is_authenticated():
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
    else:
        return render_template('login.html')
    


@app.route('/eliminarpaciente')
def eliminarpaciente():
    if is_authenticated():
        return render_template('eliminarPaciente.html')
    else:
        return render_template('login.html')
    
    


@app.route('/delete',methods=['POST'])




def delate():
    
    if is_authenticated():

        if request.method == 'POST':
            pacEli= request.form['pacEli']
            curactualizar = mysql.connection.cursor()
            curactualizar.execute('delete from adpac where nombreP=%s', (pacEli, ))
            mysql.connection.commit()

        flash('Usuario eliminado')
        return render_template('registrarPaciente.html')
    else:
        return render_template('login.html')


#CONFIGURACION DE MEDICO

@app.route('/registrarMedico')
def registrarMedico():
    return render_template('registrarMedico.html')

@app.route('/guardarmedico',methods=['POST'])
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
def eliminarmedico():
    return render_template('eliminarMedico.html')

@app.route('/deletemedico',methods=['POST'])
def delatemedico():
    if request.method == 'POST':
        medEli= request.form['medEli']
        curactualizar = mysql.connection.cursor()
        curactualizar.execute('delete from admedicos where nombre=%s', (medEli, ))
        mysql.connection.commit()

    flash('Medico Eliminado Correctamente')
    return render_template('registrarPaciente.html')

@app.route('/editarmedico')
def editarmedico():
    return render_template('editarMedico.html')

@app.route('/cambiarMedico',methods=['POST'])
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
def realizarconsulta():
    return render_template('generarConsulta.html')

@app.route('/guardarconsulta',methods=['POST'])
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
def buscarcon():
    return render_template('buscarPacientes.html')


@app.route('/consultarPaciente', methods=['POST'])
def consultarPaciente():
    if request.method == 'POST':
        nommedi= request.form['nommedi']
        curselect=mysql.connection.cursor()
        curselect.execute('select * from pacconsultas where medico=%s', (nommedi, ))
        consulta=curselect.fetchall()
        return render_template('consultas.html',consultam=consulta)

@app.route('/iracerrar')
def iracerrar():
    return render_template('cerrarSesion.html')

@app.route('/cerrarsesion',methods=['POST'])
def cerrarsesion():
    if request.method == 'POST':
        session.pop('rfc_user', None)
        return redirect(url_for('index'))



if __name__== '__main__':
    app.run(port= 8000, debug=True)