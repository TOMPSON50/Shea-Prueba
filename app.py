from flask import Flask, jsonify
from flask import render_template, redirect, url_for
from flask import Flask, jsonify, request, session
from supabase import create_client, Client
from datetime import datetime
from dateutil import parser
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_muy_segura'
# Configuración de Supabase
SUPABASE_URL = "https://fwmiqngtgctfgnyjjxae.supabase.co"  # Sustituye con tu URL de Supabase
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3bWlxbmd0Z2N0ZmdueWpqeGFlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjUzOTAwNjIsImV4cCI6MjA0MDk2NjA2Mn0.VBHEMLJ5Phn6jyVAySu0TokveqEL0kCs6-VmFihS76E"  # Sustituye con tu clave de API de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def set_password(self, password):
   self.password_hash = generate_password_hash (password)

def check_password(self, password):
   return check_password_hash(self.password_hash, password)

####LOGIN
@app.route('/', methods=['POST','GET'])
def login():
    if "user" in session:
         session.pop('user',None)
         return redirect ('/')
    username = request.form.get ('Username')
    password = request.form.get ('Password')
    response = supabase.table('usuarios').select('*').eq('username', username).execute()
    # Verificar si response.data contiene una lista no vacía
    if not response.data or len(response.data) == 0:
        return render_template ('login.html')
    # Extraer los datos del usuario (ya sabemos que la lista tiene al menos un elemento)
    user_data = response.data[0]
    hashed_password = user_data.get('password')  # Asegurarse de que 'password' exista
    # Verificar si hashed_password tiene un valor
    if hashed_password is None:
        return "Error: El usuario no tiene una contraseña registrada.", 400

    # Verificar la contraseña
    if check_password_hash(hashed_password, password):
        session['user'] = username
        session['role'] = user_data.get('role')
        session ['user_cliente_id'] = user_data.get ('user_cliente_id')
        return redirect('/dashboard')
    else:
        return "Contraseña incorrecta", 403
##REGISTER
@app.route('/register', methods = ['POST', 'GET'])
def register():
   if "user" not in session:
      return redirect ('/')
   response = supabase.table("clientes").select("*").execute()
   data = response.data
   username = request.form.get ('Username')
   if not username:
      return render_template ('register.html', data =data)
   else:
      password = request.form.get ('Password')
      password = generate_password_hash (password)
      role = request.form.get ('Role')
      if role == "admin":
         user_cliente_id = 0
      else:
         user_cliente_id = request.form.get ('clienteid')
      print (user_cliente_id)
      nombre = request.form.get ('Nombre')
      apellido = request.form.get ('Apellido')
      email = request.form.get ('Email')
      telefono = request.form.get ('Telefono')
      response = supabase.table('usuarios').insert({
          'username': username,
          'password': password,
          'role' : role,
          'user_cliente_id' : user_cliente_id,
          'Nombre' : nombre,
          'Apellido' : apellido,
          'Email' : email,
          'Telefono' : telefono
          }).execute()
      return redirect('/')

##DASHBOARD
@app.route('/dashboard', methods = ['POST', 'GET'])
def dashboard():
   if "user" in session:
      print (session ['user'])
      response = supabase.table("clientes").select("*").execute()
      data = response.data
      id = session ['user_cliente_id']
      if id != 0:
         response = supabase.table("clientes").select("nombre").eq('id', id).execute()
         print (response)
         cliente = response.data[0]['nombre']
         return render_template ('home.html', data = data, username = session ['user'], cliente = cliente)
      else:
          return render_template ('home.html', data = data, username = session ['user'], cliente = 0)
   return redirect ('/')

#LOGOUT
@app.route ('/logout')
def logout(): 
   session.pop('user',None)
   return redirect ('/')
#VER CLIENTE
@app.route('/cliente/<id>', methods=['GET'])
def get_disp(id):     
    desired_value = id
    response = supabase.table('clientes').select('*').eq('id', desired_value).limit(1).execute()
    data = response.data
    timestampz = data[0]['created_at']
    timestampz_obj = parser.isoparse(timestampz)
    formatted_timestamp = timestampz_obj.strftime("%Y-%m-%d %H:%M:%S %Z")
    if not data:
      return "Not Found", 404
    return render_template('disp.html', data=data, timestamp=formatted_timestamp)

##AÑADIR CLIENTE
@app.route ('/addcliente', methods = ['POST', 'GET'])
def add_cliente():
   nombre = request.form.get ('nombre')
   Alias = request.form.get ('Alias')
   rfc = request.form.get ('rfc')
   calle = request.form.get ('calle')
   numeroExterior = request.form.get ('numeroExterior')
   numeroInterior = request.form.get ('numeroInterior')
   colonia = request.form.get ('colonia')
   ciudad = request.form.get ('ciudad')
   estado = request.form.get ('estado')
   codigoPostal = request.form.get ('codigoPostal')
   pais = request.form.get ('pais')
   adminNombre = request.form.get ('adminNombre')
   adminEmail = request.form.get ('adminEmail')
   adminTelefono = request.form.get ('adminTelefono')
   tecnicoNombre = request.form.get ('tecnicoNombre')
   tecnicoEmail = request.form.get ('tecnicoEmail')
   tecnicoTelefono = request.form.get ('tecnicoTelefono')
   Alias = request.form.get ('Alias')
   Alias = request.form.get ('Alias')
   if not nombre:
      return render_template ('add_cliente.html')
   else: 
      response = supabase.table('clientes').insert({
          'nombre': nombre,
          'alias' : Alias,
          'rfc' : rfc,
          'calle' : calle,
          'numeroExterior' : numeroExterior,
          'numeroInterior' : numeroInterior,
          'colonia' : colonia,
          'ciudad' : ciudad,
          'estado' : estado,
          'codigoPostal' : codigoPostal,
          'pais' : pais,
          'adminNombre' : adminNombre,
          'adminEmail' : adminEmail,
          'adminTelefono' : adminTelefono,
          'tecnicoNombre' : tecnicoNombre,
          'tecnicoEmail' : tecnicoEmail,
          'tecnicoTelefono' : tecnicoTelefono    
          }).execute()
      return redirect('/dashboard')
   
##EDITAR CLIENTE
@app.route ('/cliente/edit/<id>', methods = ['POST', 'GET'])
def cliente_edit (id):
   nombre = request.form.get ('nombre')
   response = (
    supabase.table("clientes")
    .update({
       "nombre": nombre,
       })
    .eq("id", id)
    .execute())
   response = supabase.table('clientes').select('*').eq('id', id).limit(1).execute()
   data = response.data
   timestampz = data[0]['created_at']
   timestampz_obj = parser.isoparse(timestampz)
   formatted_timestamp = timestampz_obj.strftime("%Y-%m-%d %H:%M:%S %Z")
   if not response:
      return "Not Found", 404
   else:
      return render_template ('/disp.html', data=data, timestamp=formatted_timestamp )
## BORRAR CLIENTE
@app.route('/cliente/delete/<id>', methods = ['POST', 'GET'])
def disp_delete (id):
   response = supabase.table('clientes').delete().eq('id', id).execute()
   if not response:
      return "Not Found", 404
   else:
      return redirect ('/dashboard')

## VER DISPOSITIVOS DE CLIENTE 
@app.route ('/cliente/dispositivos/<id>', methods = ['POST', 'GET'])
def cliente_dispositivos (id):
   data = supabase.table ('clientes').select('nombre').eq('id', id).execute()
   cliente = data.data[0]['nombre']
   response = supabase.table ('dispositivos').select('*').eq('cliente_id', id).execute()
   data = response.data
   return render_template ('/dispositivos.html', data = data, cliente = cliente, clienteid = id)

## AÑADIR DISPOSITIVOS DE CLIENTE
@app.route ('/cliente/dispositivos/add/<id>', methods = ['POST', 'GET'])
def add_dispositivos (id):
   data = supabase.table ('clientes').select('nombre').eq('id', id).execute()
   cliente = data.data[0]['nombre']
   MAC_data = request.form.get('MAC')
   if not MAC_data:
       return  render_template('/add_disp.html', cliente = cliente, clienteid = id)
   else:
      MAC_data = str (MAC_data)
      MAC_data = MAC_data.upper()
      Location_data= request.form.get('Location')
      Status_data = request.form.get ('Status')
      Cliente_id = id
      print (Cliente_id)
      response = supabase.table('dispositivos').insert({
          'MAC': MAC_data,
          'Location': Location_data,
          'Status' : Status_data,
          'cliente_id' : Cliente_id   
          }).execute()
   return redirect (url_for('cliente_dispositivos', id  = Cliente_id)) 

##VER DISPOSITIVO ESPECíFICO   
@app.route ('/cliente/dispositivos/ver/<clienteid>/<id>', methods = ['POST', 'GET'])
def ver_dispositivo (clienteid, id):
   response = supabase.table ('clientes').select('nombre').eq('id', clienteid).execute()
   cliente = response.data[0]['nombre']
   dispositivo_id = id
   response = supabase.table('dispositivos').select('*').eq('id', dispositivo_id).limit(1).execute()
   data = response.data
   timestampz = data[0]['created_at']
   timestampz_obj = parser.isoparse(timestampz)
   formatted_timestamp = timestampz_obj.strftime("%Y-%m-%d %H:%M:%S %Z")
   return render_template ('/ver_dispositivo.html', cliente = cliente,clienteid = clienteid , data = data, timestamp=formatted_timestamp)

##BORRAR DISPOSITIVO
@app.route ('/cliente/dispositivos/ver/<clienteid>/delete/<id>', methods = ['POST', 'GET'])
def delete_dispositivo (clienteid, id):
   response = supabase.table('dispositivos').delete().eq('id', id).execute()
   if not response:
      return "Not Found", 404
   else:
      return redirect (url_for('cliente_dispositivos', id  = clienteid)) 
   
##EDITAR DISPOSITIVO
@app.route ('/cliente/dispositivos/ver/<clienteid>/edit/<id>', methods = ['POST', 'GET'])
def edit_dispositivo (clienteid, id):
    Location_data= request.form.get('Location')
    Status_data = request.form.get ('Status')
    response = (
    supabase.table("dispositivos")
    .update({
       "Location": Location_data,
       "Status" : Status_data
       })
    .eq("id", id)
    .execute())
    return redirect (url_for('ver_dispositivo', clienteid = clienteid, id = id))
   

if __name__ == "__main__":
  app.run(host='0.0.0.0',debug=True)