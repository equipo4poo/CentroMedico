from flask import Flask,render_template,request,redirect,url_for,flash,session
import pdfkit,bcrypt
from flask_mysqldb import MySQL
from functools import wraps



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
def is_authenticated():
    return 'authenticated' in session

def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'rfc' not in session:
            return render_template('login.html')
        elif 'rol' in session and session['rol'] =='admin':
            return f(*args, **kwargs)
        else:
            flash('Solo los médicos con rol admin pueden acceder')
            return render_template('registrarPac.html')
    return decorated_function
'''
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'rfc' not in session:
            return render_template('login.html')
        elif 'rol' in session and session['rol'] == 'admin' or 'medico':
            return f(*args, **kwargs)
        else:
            flash('Solo los médicos pueden acceder')
            return render_template('login.html')
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_fuction(*args, **kwargs):
        if 'rfc' not in session:
            return render_template('login.html')
        return f(*args, **kwargs)
        
        else:
            flash('Inicia sesion para continuar')
            return render_template('login.html')

    
    return decorated_fuction
    
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'rfc' not in session:
            flash('Inicia sesión para continuar')
            return render_template('login.html')
        else:
            return f(*args, **kwargs)
    return decorated_function'''

@app.route('/')
def index():
    return render_template('login.html')
    

@app.route('/registrarm')

def registrarm():

    if is_authenticated():
        return render_template('adMedicos.html')
    else:
        return render_template('login.html')
    
@app.route('/bf')

def bf():

    if is_authenticated():
        return render_template('buscarfecha.html')
    else:
        return render_template('login.html')


@app.route('/consultarm')
@admin_login_required

def consultarm():
    if is_authenticated():
        curEditar=mysql.connection.cursor()
        curEditar.execute('Select * from adpac where idPac=%s',(id,))
        consultid=curEditar.fetchall()
        return render_template('adMedicos.html',medicos=consultid)
    else:
        return render_template('login.html')


@app.route('/newcon/<id>')

def newcon(id):
    curEditar=mysql.connection.cursor()
    curEditar.execute('Select * from adpac where idPac=%s',(id,))
    consultid=curEditar.fetchone()

    return render_template('registrarCon2.html',album=consultid)



#@app.route('/registrarc/<id>')
#def registrarc(id):
#    return render_template('registrarCon.html',id)



@app.route('/registrarp')

def registrarp():
    if is_authenticated():
        return render_template('registrarPac.html')
    else:
        return redirect(url_for('index'))

@app.route('/conpac')

def concon():
    if is_authenticated():
        return render_template('consultarPac.html')
    else:
        return render_template('login.html')

@app.route('/editarp/<id>')

def editarp(id):
    curEditar=mysql.connection.cursor()
    curEditar.execute('Select * from adpac where idPac=%s',(id))
    consultid=curEditar.fetchone()

    return render_template("editarPac.html",album=consultid)


'''
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


@app.route('/guardarp',methods=['POST'])
def guardar():
    if is_authenticated():
        if request.method == 'POST':
            nombre= request.form['txtpac']
            fecha= request.form['fecha']
            enfermedades= request.form['enfermedades']
            alergias= request.form['alergias']
            antecedentes= request.form['antecedentes']
            CS = mysql.connection.cursor()
            CS.execute('insert into adpac (nombreP,fecha_nac,encronias,alergias,antecedentes,rfcmed) values(%s,%s,%s,%s,%s)',(nombre,fecha,enfermedades,alergias,antecedentes,session[0]))
            mysql.connection.commit()
        
            CS.execute('SELECT LAST_INSERT_ID()')
            inserted_id = CS.fetchone()[0]
    
        flash('Paciente guardado')
        return render_template("registrarCon.html", id=inserted_id)
    else:
        return render_template('login.html')'''
    


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


'''@app.route('/guardarc/<id>', methods=['POST'])
def guardarc(id):
    if request.method == 'POST':
        # ... (existing code)
        fecha= request.form['fecha']
        peso= request.form['peso']
        altura= request.form['altura']
        temperatura= request.form['temperatura']
        latidos= request.form['latidos']
        glucosa= request.form['glucosa']
        sintomas= request.form['sintomas']
        diagnostico= request.form['diagnostico']
        tratamiento= request.form['tratamiento']

        # Generate the HTML content for the PDF
        html_content = render_template('registrarCon.html', id=id, fecha=fecha, peso=peso, altura=altura, temperatura=temperatura, latidos=latidos, glucosa=glucosa, sintomas=sintomas, diagnostico=diagnostico, tratamiento=tratamiento)

        # Generate PDF using pdfkit
        pdf = pdfkit.from_string(html_content, False)

        # Save PDF to the database
        
        CS = mysql.connection.cursor()
        CS.execute('insert into adcon (cfecha, peso, altura, temperatura, latidos, glucosa, sintomas, diagnostico, tratamiento, idp, pdf_data) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (fecha, peso, altura, temperatura, latidos, glucosa, sintomas, diagnostico, tratamiento, id, pdf))
        mysql.connection.commit()

    flash('Consulta guardada')
    return render_template("registrarCon.html")
'''

@app.route('/consultarM')


def consultarM():

    curselect=mysql.connection.cursor()
    curselect.execute('select * from admedicos')
    consulta=curselect.fetchall()
    print(consulta)
    return render_template('consultarMed.html',consultam=consulta)

'''
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


Anterior verificada!!!
@app.route('/iniciar', methods=['POST'])
def iniciar():
    nombre = request.form['txtrfc']
    contrasena = request.form['txtpassword']
    CS = mysql.connection.cursor()
    CS.execute('select rfcmed, contrasena from admedicos where rfcmed = %s', (nombre,))
    user_data = CS.fetchone()
    
    
    provided_password = request.form['txtpassword']
    hashed_password_from_db = user_data[1]
    if bcrypt.checkpw(provided_password.encode('utf-8'), hashed_password_from_db.encode('utf-8')):
        session['authenticated'] = True
        flash('Acceso correcto')
        return redirect(url_for('registrarp'))  # Redirect to authenticated page
    else:
        flash('Usuario o contraseña incorrecta')
        return render_template('login.html')'''
        
@app.route('/iniciar', methods=['POST'])
def iniciar():
    
    nombre = request.form['txtrfc']
    contrasena = request.form['txtpassword']
    CS = mysql.connection.cursor()
    CS.execute('select rfcmed, contrasena from admedicos where rfcmed = %s', (nombre,))
    user_data = CS.fetchone()

    provided_password = request.form['txtpassword']
    hashed_password_from_db = user_data[1]
    if bcrypt.checkpw(provided_password.encode('utf-8'), hashed_password_from_db.encode('utf-8')):
        session['authenticated'] = True
        session['rfc'] = nombre  # Store RFC in the session
        flash('Acceso correcto')
        return redirect(url_for('registrarp'))  # Redirect to authenticated page
    else:
        flash('Usuario o contraseña incorrecta')
        return render_template('login.html')



@app.route('/guardarm', methods=['POST'])

def guardarm():
    if request.method == 'POST':
        rfc = request.form['rfc']
        nombre = request.form['nombre']
        cedula = request.form['cedula']
        correo = request.form['correo']
        password = request.form['password']
        rol = request.form['rol']
        
        # Hash the password using bcrypt
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        CS = mysql.connection.cursor()
        CS.execute('insert into admedicos (rfcmed,nombre,cedula,correo,contrasena,rol) values(%s,%s,%s,%s,%s,%s)',
                   (rfc, nombre, cedula, correo, hashed_password, rol))
        mysql.connection.commit()

    flash('Usuario guardado')
    return render_template("registrarCon.html")

@app.route('/guardarp',methods=['POST'])

def guardar():
    if is_authenticated():
        if request.method == 'POST':
            nombre= request.form['txtpac']
            fecha= request.form['fecha']
            enfermedades= request.form['enfermedades']
            alergias= request.form['alergias']
            antecedentes= request.form['antecedentes']
            
            rfc_medico = session['rfc']  # Retrieve RFC from the session
            
            CS = mysql.connection.cursor()
            CS.execute('insert into adpac (nombreP,fecha_nac,encronias,alergias,antecedentes,rfcmed) values(%s,%s,%s,%s,%s,%s)',
                       (nombre, fecha, enfermedades, alergias, antecedentes, rfc_medico))
            mysql.connection.commit()

            CS.execute('SELECT LAST_INSERT_ID()')
            inserted_id = CS.fetchone()[0]

        flash('Paciente guardado')
        return render_template("registrarCon.html", id=inserted_id)
    else:
        return render_template('login.html')





@app.route('/consultarp', methods=['POST'])

def consultarp():
    if request.method == 'POST':
        nombre= request.form['nombre']
        rfc_medico = session['rfc']  # Retrieve RFC from the session
        curselect=mysql.connection.cursor()
        curselect.execute('select * from adpac where nombreP like %s and rfcmed=%s',("%"+nombre+"%",rfc_medico,))
        consulta=curselect.fetchall()
        print(consulta)
        
        return render_template('consultarPac.html',consultap=consulta)
    
    
@app.route('/editarPaciente/<id>', methods=['POST'])

def editarPaciente(id):
    if request.method == 'POST':

        nombre= request.form['txtpac']
        fecha= request.form['fecha']
        enfermedades= request.form['enfermedades']
        alergias= request.form['alergias']
        antecedentes= request.form['antecedentes']
        CS= mysql.connection.cursor()
        CS.execute("UPDATE adpac SET nombreP=%s, fecha_nac=%s, encronias=%s, alergias=%s, antecedentes=%s WHERE idPac=%s", (nombre,fecha,enfermedades,alergias,antecedentes,id))
        

    return render_template('consultarPac.html')


@app.route('/concit/<id>')

def concit(id):

    curselect=mysql.connection.cursor()
    curselect.execute('select * from adcon where idp=%s',(id,))
    consulta=curselect.fetchall()
    print(consulta)
    return render_template('consultarTodo.html',consultap=consulta)


@app.route('/eliminar/<rfc>')

def eliminar(rfc):
    cursoeli = mysql.connection.cursor()
    cursoeli.execute('select * from admedicos where rfcmed=%s', (rfc, ))
    consulId = cursoeli.fetchone()
    return render_template('eliminarMedico.html', album = consulId)

@app.route('/delete/<rfc>',methods=['POST'])

def delate(rfc):
    if request.method == 'POST':
        curactualizar = mysql.connection.cursor()
        curactualizar.execute('delete from admedicos where rfcmed=%s', (rfc,) )
        mysql.connection.commit()

    flash('Album Eliminado Correctamente bro')
    return render_template('consultarMed.html')

@app.route('/editarm/<rfc>')

def editarm(rfc):
    cursoeli = mysql.connection.cursor()
    cursoeli.execute('select * from admedicos where rfcmed=%s', (rfc, ))
    consulId = cursoeli.fetchone()
    return render_template('editarMedico.html', album = consulId)

@app.route('/editm/<rfc>',methods=['POST'])
def editm(rfc):
    if request.method == 'POST':
        newerfcMed= request.form['RFC']
        newenombreMed= request.form['Nombre']
        newecedulaMed= request.form['Cedula']
        newecorreoMed= request.form['Correo']
        newecontraMed= request.form['Contraseña']
        neweRol= request.form['Rol']
        CS= mysql.connection.cursor()
        CS.execute("UPDATE admedicos SET rfcmed = %s, nombre=%s, cedula=%s, correo=%s, contrasena=%s, rol=%s WHERE rfcmed=%s", (newerfcMed,newenombreMed,newecedulaMed,newecorreoMed,newecontraMed,neweRol,rfc))
        
    flash('Usuario modificado')
    return redirect(url_for('consultarM'))

@app.route('/buscarfecha', methods=['POST'])
def buscarfecha():
    if request.method == 'POST':
        fechb= request.form['fechb']
        curselect=mysql.connection.cursor()
        curselect.execute('select * from adcon where cfecha=%s', (fechb, ))
        consulta=curselect.fetchall()
        return render_template('buscarfecha.html',consultam=consulta)
    print(consulta)

#ejecucion 
if __name__== '__main__':
    app.run(port= 5000, debug=True)

