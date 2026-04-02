from flask import Flask, session, render_template, request, redirect, url_for
from flaskext.mysql import MySQL
from flask.helpers import send_from_directory
import re,os
from datetime import datetime

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

app = Flask(__name__)

mysql = MySQL()
app.secret_key = 'your secret key'

#Configuracion MySQL
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'final'

#AGREGAR CARPETA
CARPETA = os.path.join('static/imagenes/imagenes_productos/')  # al path del proyecto le adjunto ‘upload’
app.config['CARPETA'] = CARPETA


mysql.init_app(app)

@app.route('/')
def productos():
    sql="SELECT * FROM productos;"
    conn=mysql.connect() #Hacemos la conexion a mysql
    cursor=conn.cursor()
    cursor.execute(sql) #Ejecutamos el string sql 
    rows=cursor.fetchall()
    print(rows)
    #Mostrar cantidad de productos en el carrito
    if 'usuario' in session:
        usuario = session['usuario']
        cursor.execute("SELECT SUM(cantidad) FROM carrito WHERE username=%s",usuario)
        registro = cursor.fetchone()
        mostrarCuantos = registro[0]
        if mostrarCuantos == None:
            mostrarCantidad = 0
        else:
            mostrarCantidad = mostrarCuantos
        conn.commit()
        return render_template('productos.html',productos=rows, mostrarCantidad=mostrarCantidad)
    conn.commit()
    return render_template('productos.html',productos=rows) # Renderizo la pagina index.html

@app.route('/login', methods = ['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username_form = request.form['username']
        password_form = request.form['password']
   
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute("SELECT COUNT(1) FROM usuarios WHERE username = %s;", [username_form])
        if cursor.fetchone()[0]:
            cursor.execute("SELECT password FROM usuarios WHERE username = %s;", [username_form])
            for row in cursor.fetchall():
                if password_form == row[0]:
                    session['usuario'] = username_form 
                    #session['carrito'] = username_form
                    msg ="Se ha identificado correctamente"
                    return redirect('/')
                else:
                    msg = "Credenciales no validas"
        return render_template('login.html', msg=msg)
    return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect('/')

@app.route('/register', methods = ['GET','POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE username = %s', (username, ))
        user = cursor.fetchone()
        if user:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO usuarios VALUES (NULL,%s,%s,%s)',(username, password, email, ))
            conn.commit()
            msg = 'You have successfully registered!'
            return render_template('login.html', msg=msg) 
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg = msg)

@app.route('/add', methods=['POST'])
def add_product_to_cart():
    # Aca debemos hacer una validacion para no permitir que usuarios no indenficados generen ordenes de pedido
    if 'usuario' not in session:
        msg = 'Debe iniciar sesion para continuar'
        return render_template('login.html', msg=msg)
    else:
        if request.method == 'POST' and 'codigo' in request.form and 'cantidad' in request.form:
            codigo_form = request.form['codigo']
            cantidad_form = request.form['cantidad']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos WHERE codigo=%s",(codigo_form))
            
            itemCarrito = cursor.fetchall()
            for producto in itemCarrito:
                _codigo = producto[0]
                _descripcion = producto[1]
                _precio = producto[2]
                _foto = producto[4]

            # Deberiamos generar otra db e ir almacenando los productos seleccionados
            totalAbonar=float(_precio)*float(cantidad_form)
            usuario=session['usuario']

            # Deberiamo comprobar que el producto se encuentre en el carrito
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT codigo, cantidad, precio FROM carrito WHERE username=%s AND codigo=%s",(usuario,codigo_form))
            productosCarrito = cursor.rowcount
            print('Contenido del codigo_form')
            print(codigo_form)
            cantidadEnCarrito = cursor.fetchone()
            #cantidadExistente = cantidadEnCarrito[0]
            
            if cantidadEnCarrito == None:
                cantidadExistente = 0
            else:
                cantidadExistente = cantidadEnCarrito[1]
            #conn.commit()
            print(cantidadEnCarrito)
            print(cantidadExistente)
            if productosCarrito >0:
                #Como el producto ya esta en el carrito solo incrementamos la cantidad segun el valor que trae el formulario
                nuevaCantidad = cantidadExistente + int(cantidad_form)
                nuevoTotalAbonar = nuevaCantidad * cantidadEnCarrito[2]
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute("UPDATE carrito SET cantidad=%s, totalAbonar=%s ",(nuevaCantidad,nuevoTotalAbonar))
                conn.commit()
                msg = "El producto fua a;adido al carrito"
                print("Match")
                print(nuevaCantidad)
            else:
                #Si el producto no existe en el carrito del usuario, entonces lo agregamos como un nuevo registro
                conn = mysql.connect()
                cursor = conn.cursor()
                sql = "INSERT INTO `carrito`(`id`, `username`, `codigo`, `descripcion`, `precio`, `cantidad`, `foto`, `totalAbonar`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)"
                datos = (usuario, _codigo,_descripcion, _precio, cantidad_form, _foto, totalAbonar)         
                cursor.execute(sql,datos)
                conn.commit()
                print("Not Match")
            return redirect('/carrito') 

@app.route('/search', methods=['POST'])
def search():
    busqueda = request.form['txtSearch']
    sql="SELECT * FROM productos where descripcion like %s"
    conn=mysql.connect() #Hacemos la conexion a mysql
    cursor=conn.cursor()
    cursor.execute(sql,(('%' + busqueda + '%'))) #Ejecutamos el string sql junto al comodin
    rows=cursor.fetchall()
    
    if 'usuario' in session:
        usuario = session['usuario']
        cursor.execute("SELECT SUM(cantidad) FROM carrito WHERE username=%s",usuario)
        registro = cursor.fetchone()
        mostrarCuantos = registro[0]
        if mostrarCuantos == None:
            mostrarCantidad = 0
        else:
            mostrarCantidad = mostrarCuantos
        
        return render_template('productos.html',productos=rows, mostrarCantidad=mostrarCantidad)
    conn.commit()
    return render_template('productos.html',productos=rows)

@app.route('/carrito')
def carrito():
    if 'usuario' in session:
        usuario = session['usuario']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM carrito WHERE username=%s",usuario)
        itemCarrito = cursor.fetchall()
        #conn.commit()
        #Mostrar cantidad de productos en el carrito
        cursor.execute("SELECT SUM(cantidad) FROM carrito WHERE username=%s",usuario)
        registro = cursor.fetchone()
        mostrarCuantos = registro[0]
        if mostrarCuantos == None:
            mostrarCantidad = 0
        else:
            mostrarCantidad = mostrarCuantos

        #print(mostrarCantidad)

        cursor.execute("SELECT SUM(totalAbonar) FROM carrito WHERE username=%s",usuario)
        totalSuma = cursor.fetchone()
        total = (totalSuma[0])
        if total == None:
            mostrarTotal = 0
        else:
            mostrarTotal = total

        #print(total)
        conn.commit()

        return render_template('carrito.html', itemCarrito=itemCarrito, mostrarCantidad=mostrarCantidad, mostrarTotal=mostrarTotal) # Renderizo la pagina index.html
    
    else:
        msg = "Debe estar logueado"
        return render_template('login.html', msg=msg)

@app.route('/borrar/<int:id>')
def borrar(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM carrito WHERE id=%s",(id))
    conn.commit()
    return redirect('/carrito')

@app.route('/vaciar_carrito/<string:username>')
def vaciar_carrito(username):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM carrito WHERE username=%s",(username))
    conn.commit()
    return redirect('/carrito')

#Metodos ABM 

@app.route('/abm')
def abm():
    if session:    
        if session['usuario'] == 'admin' and session['usuario']:
            sql = "SELECT * FROM `productos`;"
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            # guarda el resultado del cursor del cursor en la variable productos
            productos = cursor.fetchall()

            #usuario = session['usuario']
            cursor.execute("SELECT SUM(cantidad) FROM carrito WHERE username=%s",'admin')
            registro = cursor.fetchone()
            mostrarCuantos = registro[0]
            if mostrarCuantos == None:
                mostrarCantidad = 0
            else:
                mostrarCantidad = mostrarCuantos

            conn.commit()
            # return render_template('abm.html')
            return render_template('abm.html', productos=productos, mostrarCantidad=mostrarCantidad)
    else:
            return redirect('/')

@app.route('/store',methods=['POST'])
def storage():
       # toma los datos que envio elformulario en txtNombre
    _nombre = request.form['txtDescripcion']
    _precio = request.form['txtPrecio']  # toma los datos del formulario
    _cantidad = request.form['txtCantidad']  # toma los datos del
    _foto = request.files['txtFoto']  # toma los datos del

    now = datetime.now()
    tiempo = now.strftime(("%Y%H%M%S"))
    if _foto.filename != '':  # distinto de vacio
        nuevoNombreFoto = tiempo+_foto.filename
        _foto.save("static/imagenes/imagenes_productos/"+nuevoNombreFoto)

    sql = "INSERT INTO `productos` (`codigo`,`descripcion`,`precio`,`cantidad`,`foto`) VALUES (null,%s,%s,%s,%s)"
    datos = (_nombre, _precio, _cantidad, nuevoNombreFoto)  # crea la sentencia sql
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)  # ejecuta la sentencia sql
    conn.commit()
    return redirect('/abm')

@app.route('/create')
def create():
    conn = mysql.connect()              # me conecto a la base de datos
    cursor = conn.cursor()  
    cursor.execute("SELECT SUM(cantidad) FROM carrito WHERE username=%s",'admin')
    registro = cursor.fetchone()
    mostrarCuantos = registro[0]
    if mostrarCuantos == None:
        mostrarCantidad = 0
    else:
        mostrarCantidad = mostrarCuantos    

    conn.commit()
    return render_template('create.html', mostrarCantidad=mostrarCantidad)

@app.route('/edit/<int:id>')
def edit(id):
    sql = "SELECT * FROM `productos` WHERE codigo=%s;"
    conn = mysql.connect()              # me conecto a la base de datos
    cursor = conn.cursor()              # almacenar informacion
    cursor.execute(sql, (id))               # ejecuto en MySQL la variable sql
    productos = cursor.fetchall()

    cursor.execute("SELECT SUM(cantidad) FROM carrito WHERE username=%s",'admin')
    registro = cursor.fetchone()
    mostrarCuantos = registro[0]
    if mostrarCuantos == None:
        mostrarCantidad = 0
    else:
        mostrarCantidad = mostrarCuantos    

    conn.commit()
    return render_template('edit.html', productos=productos, mostrarCantidad=mostrarCantidad)

@app.route('/update',  methods=['POST'])
# cuando formulario create.hmtl hace el submit envia los datos a /store
def update():
    _nombre = request.form['txtDescripcion']
    _precio = request.form['txtPrecio']  # toma los datos del formulario
    _cantidad = request.form['txtCantidad']  # toma los datos del
    _foto = request.files['txtFoto']  # toma los datos del
    _id = request.form['txtId']

    sql = "UPDATE `productos` SET `descripcion`=%s ,`precio`=%s ,`cantidad`=%s WHERE codigo=%s"
    datos = (_nombre, _precio,_cantidad, _id)  # crea la sentencia sql

    conn = mysql.connect()
    cursor = conn.cursor()

    # agregamos
    now = datetime.now()                        # igual que en /store
    tiempo = now.strftime("%Y%H%M%S")

    if _foto.filename != '':
        nuevoNombreFoto = tiempo+_foto.filename
        # guardo la foto en la carpeta ’uploads’
        _foto.save("static/imagenes/imagenes_productos/"+nuevoNombreFoto)
        cursor.execute(
            "SELECT foto FROM `productos` WHERE codigo=%s", (_id))
        fila = cursor.fetchall()   # fila va a tener un solo registro y 1 solo campo
        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        cursor.execute(
            "UPDATE `productos` SET foto=%s WHERE codigo=%s", (nuevoNombreFoto, _id))
        conn.commit()

    cursor.execute(sql, datos)               # ejecuta la sentencia sql
    conn.commit()
    return redirect('abm')  # y renderiza index.html

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    # entras al directorio y mostras ese nombre de foto
    return send_from_directory(app.config['CARPETA'], nombreFoto)

@app.route('/destroy/<int:id>')
def destroy(id):
    sql = "DELETE FROM `productos` WHERE codigo=%s;"
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT foto FROM `productos` WHERE codigo=%s", (id))
    fila = cursor.fetchall()   # fila va a tener un solo registro y 1 solo campo
    # remuevo la foto
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))

    cursor.execute(sql, (id))  # ejecuta la sentencia sql
    conn.commit()
    return redirect('/abm')  # y renderiza index.html
    
# Vamos a integrar un SDK que permita pagar electronicamente
@app.route('/comprar')
def comprar():    
    sdk = mercadopago.SDK("TEST-4568818446897296-072421-5818c719a4bccb5e20bd5b81c69450f1-89489605")
    #Obtener todos los medios de pago
    payment_methods_response = sdk.payment_methods().list_all()
    payment_methods = payment_methods_response["response"]
    #print(payment_methods)
    #Traemos de nuevo los productos del carrito para poder generar la orden de pago
    usuario = session['usuario']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM carrito WHERE username=%s",usuario)
    itemCarrito = cursor.fetchall()
    #conn.commit()
    #Mostrar cantidad de productos en el carrito
    cursor.execute("SELECT SUM(cantidad) FROM carrito WHERE username=%s",usuario)
    registro = cursor.fetchone()
    mostrarCuantos = registro[0]
    if mostrarCuantos == None:
        mostrarCantidad = 0
    else:
        mostrarCantidad = mostrarCuantos
    #Sumamos el total a abonar por los productos en el carrito
    cursor.execute("SELECT SUM(totalAbonar) FROM carrito WHERE username=%s",usuario)
    totalSuma = cursor.fetchone()
    total = (totalSuma[0])
    if total == None:
        mostrarTotal = 0
    else:
        mostrarTotal = total

    conn.commit()

    return render_template('comprar.html', mostrarCantidad=mostrarCantidad,mostrarTotal=mostrarTotal)

# Importamos el SDK de mercadopago
import mercadopago

@app.route('/process_payment', methods = ['POST'])
def process_payment():

    sdk = mercadopago.SDK("TEST-4568818446897296-072421-5818c719a4bccb5e20bd5b81c69450f1-89489605")

    transaction_amount = request.form['transactionAmount']
    description = request.form['productDescription']
    payment_method_id = request.form['paymentMethod']
    payer = request.form['payerEmail']
    
    payment_data = {
        "items": [
            {
            #"transaction_amount": transaction_amount,
            "description": description,
            "quantity": 1,
            "unit_price": float(transaction_amount),
            "payment_method_id": payment_method_id,
            "payer": {
            "email": payer
            }
            }
        ]
    }
    print(payment_data)

    payment_response = sdk.preference().create(payment_data)
    payment = payment_response["response"]["init_point"]
    
    print(payment)
   
    return redirect(payment)

if __name__ == '__main__':
    app.run(debug=True)
