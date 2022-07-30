from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#mysql inicializacion de la coneccion

app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= 'flaskcontacs'
mysql= MySQL(app)

#configuraciones
app.secret_key = 'mysecretkey'


@app.route('/')
def index():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data=cur.fetchall()
    return render_template('index.html', contactos = data)

@app.route('/add_contact', methods=['POST'])
def contactos():
    if request.method == 'POST':
       nombre=request.form['nombre']
       telefono=request.form['telefono']
       email=request.form['email']
       cur= mysql.connection.cursor()
       cur.execute("INSERT INTO contacts (NombreCompleto, telefono, email) VALUES (%s,%s,%s)", (nombre, telefono, email))
       mysql.connection.commit()
       flash('Contacto Agregado')
    return redirect(url_for('index'))

    

@app.route('/editar/<id>', methods= ['POST','GET'])
def edit(id):
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data=cur.fetchall()
    print(data[0])
    return render_template('editar.html', contact=data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['nombre']
        phone = request.form['telefono']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET NombreCompleto = %s,
                email = %s,
                telefono = %s
            WHERE id = %s
        """, (fullname, email, phone, id))
        flash('Actualizacion Completada')
        mysql.connection.commit()
        return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def delete(id):
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    cur.execute('alter table contacts AUTO_INCREMENT=1')
    mysql.connection.commit()
    flash('contacto removido')
    return redirect(url_for('index'))




if __name__== '__main__':
    app.run(debug=True)
