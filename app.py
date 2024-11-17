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
  if "user" in session:       
    desired_value = id
    response = supabase.table('clientes').select('*').eq('id', desired_value).limit(1).execute()
    data = response.data
    alias = data[0]['alias']
    timestampz = data[0]['created_at']
    timestampz_obj = parser.isoparse(timestampz)
    formatted_timestamp = timestampz_obj.strftime("%Y-%m-%d %H:%M:%S %Z")
    if not data:
      return "Not Found", 404
    return render_template('disp_cliente.html', data=data, timestamp=formatted_timestamp, alias =alias)
  return redirect ('/')

##AÑADIR CLIENTE
@app.route ('/addcliente', methods = ['POST', 'GET'])
def add_cliente():
 if "user" in session: 
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
 return redirect ('/')
   
##EDITAR CLIENTE
@app.route ('/cliente/edit/<id>', methods = ['POST', 'GET'])
def cliente_edit (id):
  if "user" in session:
   formid = request.form.get('form_id')
   print (formid)
   if formid == 'form1':
      nombre = request.form.get ('nombre')
      alias = request.form.get ('alias')
      rfc = request.form.get ('rfc')
      response = (
      supabase.table("clientes")
      .update({
          "nombre": nombre,
          "alias" : alias,
          "rfc" : rfc
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
         return render_template ('/disp_cliente.html', data=data, timestamp=formatted_timestamp )
   if formid == 'form2':
      calle = request.form.get ('calle')
      numeroExterior = request.form.get ('numeroExterior')
      numeroInterior = request.form.get ('numeroInterior')
      colonia = request.form.get ('colonia')
      ciudad = request.form.get ('ciudad')
      estado = request.form.get ('estado')
      codigoPostal = request.form.get ('codigoPostal')
      pais = request.form.get ('pais')
      response = (
      supabase.table("clientes")
      .update({
          'calle' : calle,
          'numeroExterior' : numeroExterior,
          'numeroInterior' : numeroInterior,
          'colonia' : colonia,
          'ciudad' : ciudad,
          'estado' : estado,
          'codigoPostal' : codigoPostal,
          'pais' : pais,
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
         return render_template ('/disp_cliente.html', data=data, timestamp=formatted_timestamp )
   if formid == 'form3':
      adminNombre = request.form.get ('adminNombre')
      adminEmail = request.form.get ('adminEmail')
      adminTelefono = request.form.get ('adminTelefono')
      response = (
      supabase.table("clientes")
      .update({
          'adminNombre' : adminNombre,
          'adminEmail' : adminEmail,
          'adminTelefono' : adminTelefono,
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
         return render_template ('/disp_cliente.html', data=data, timestamp=formatted_timestamp )
   if formid == 'form4':
      tecnicoNombre = request.form.get ('tecnicoNombre')
      tecnicoEmail = request.form.get ('tecnicoEmail')
      tecnicoTelefono = request.form.get ('tecnicoTelefono')
      response = (
      supabase.table("clientes")
      .update({
          'tecnicoNombre' : tecnicoNombre,
          'tecnicoEmail' : tecnicoEmail,
          'tecnicoTelefono' : tecnicoTelefono 
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
         return render_template ('/disp_cliente.html', data=data, timestamp=formatted_timestamp )
  return redirect ('/')
      

## BORRAR CLIENTE
@app.route('/cliente/delete/<id>', methods = ['POST', 'GET'])
def disp_delete (id):
  if "user" in session: 
   response = supabase.table('clientes').delete().eq('id', id).execute()
   if not response:
      return "Not Found", 404
   else:
      return redirect ('/dashboard')
  return redirect ('/') 

## VER DISPOSITIVOS DE CLIENTE 
@app.route ('/cliente/dispositivos/<id>', methods = ['POST', 'GET'])
def cliente_dispositivos (id):
 if "user" in session:  
   data = supabase.table ('clientes').select('nombre').eq('id', id).execute()
   cliente = data.data[0]['nombre']
   response = supabase.table ('dispositivos').select('*').eq('cliente_id', id).execute()
   data = response.data
   return render_template ('/dispositivos.html', data = data, cliente = cliente, clienteid = id)
 return redirect ('/')

## AÑADIR DISPOSITIVOS DE CLIENTE
@app.route ('/cliente/dispositivos/add/<id>', methods = ['POST', 'GET'])
def add_dispositivos (id):
 if "user" in session:  
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
 return redirect ("/")

##VER DISPOSITIVO ESPECíFICO   
@app.route ('/cliente/dispositivos/ver/<clienteid>/<id>', methods = ['POST', 'GET'])
def ver_dispositivo (clienteid, id):
 if 'user' in session:  
   response = supabase.table ('clientes').select('nombre').eq('id', clienteid).execute()
   cliente = response.data[0]['nombre']
   dispositivo_id = id
   response = supabase.table('dispositivos').select('*').eq('id', dispositivo_id).limit(1).execute()
   data = response.data
   timestampz = data[0]['created_at']
   timestampz_obj = parser.isoparse(timestampz)
   formatted_timestamp = timestampz_obj.strftime("%Y-%m-%d %H:%M:%S %Z")
   return render_template ('/ver_dispositivo.html', cliente = cliente,clienteid = clienteid , data = data, timestamp=formatted_timestamp)
 return redirect ('/')

##BORRAR DISPOSITIVO
@app.route ('/cliente/dispositivos/ver/<clienteid>/delete/<id>', methods = ['POST', 'GET'])
def delete_dispositivo (clienteid, id):
 if 'user' in session:  
   response = supabase.table('dispositivos').delete().eq('id', id).execute()
   if not response:
      return "Not Found", 404
   else:
      return redirect (url_for('cliente_dispositivos', id  = clienteid)) 
 return redirect ('/')  
   
##EDITAR DISPOSITIVO
@app.route ('/cliente/dispositivos/ver/<clienteid>/edit/<id>', methods = ['POST', 'GET'])
def edit_dispositivo (clienteid, id):
  if 'user' in session:  
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
  return redirect ('/')
 
##VER USUARIOS
@app.route ('/verusuarios', methods = ['POST', 'GET'])
def ver_usuarios ():
      if "user" in session:
         response = supabase.table("usuarios").select("*").execute()
         data = response.data
         response = supabase.table("clientes").select("*").execute()
         data_clientes = response.data
         id = session ['user_cliente_id']
         return render_template ('ver_usuarios.html', data = data, data_clientes = data_clientes)
      return redirect ('/')
      
#VER USUARIO
@app.route('/usuario/<id>', methods=['GET'])
def get_usuario(id):
  if 'user' in session:       
    desired_value = id
    response = supabase.table('usuarios').select('*').eq('id', desired_value).limit(1).execute()
    data = response.data
    clienteid = data [0]['user_cliente_id']
    if clienteid == 0:
       cliente = 'NA'
    else:
      response = supabase.table('clientes').select('nombre').eq('id', clienteid).execute()
      cliente = response.data[0]['nombre']
    timestampz = data[0]['created_at']
    timestampz_obj = parser.isoparse(timestampz)
    formatted_timestamp = timestampz_obj.strftime("%Y-%m-%d %H:%M:%S %Z")
    if not data:
      return "Not Found", 404
    return render_template('disp_usuario.html', data=data, timestamp=formatted_timestamp, cliente = cliente, id = id, clienteid = clienteid)
  return redirect ('/')
##EDITAR USUARIO
@app.route ('/usuario/editar/<id>/<clienteid>', methods = ['POST', 'GET'])
def editar_usuario(id, clienteid):
 if "user" in session:  
   username = request.form.get ('Username')
   password = request.form.get ('Password')
   password = generate_password_hash (password)
   role = request.form.get ('Role')
   if role == "admin":
      user_cliente_id = 0
   else:
      user_cliente_id = clienteid
   print (user_cliente_id)
   nombre = request.form.get ('Nombre')
   apellido = request.form.get ('Apellido')
   email = request.form.get ('Email')
   telefono = request.form.get ('Telefono')
   response = (
      supabase.table("usuarios")
      .update({
          'username' : username,
          'password' : password,
          'role' : role,
          'user_cliente_id' : user_cliente_id,
          'Nombre' : nombre,
          'Apellido' :  apellido,
          'Email' : email,
          'Telefono' : telefono
         })
      .eq("id", id)
      .execute())
   return redirect (url_for('get_usuario', id = id ))
 return redirect ('/')

##VER USUARIOS DE CLIENTE
@app.route ('/cliente/verusuarioscliente/<id>', methods = ['POST', 'GET'])
def ver_usuarios_cliente (id):
 if "user" in session:  
   data = supabase.table ('clientes').select('nombre').eq('id', id).execute()
   cliente = data.data[0]['nombre']
   response = supabase.table ('usuarios').select('*').eq('user_cliente_id', id).execute()
   data = response.data
   return render_template ('/ver_usuarios_cliente.html', data = data, cliente = cliente, clienteid = id)
 return redirect ("/")

##VER USUARIO ESPECÍFICO DE CLIENTE
@app.route('/cliente/verusuarioscliente/usuario/<id>', methods=['GET'])
def get_usuario_cliente(id):
  if "user" in session:       
    desired_value = id
    response = supabase.table('usuarios').select('*').eq('id', desired_value).limit(1).execute()
    data = response.data
    clienteid = data [0]['user_cliente_id']
    if clienteid == 0:
       cliente = 'NA'
    else:
      response = supabase.table('clientes').select('nombre').eq('id', clienteid).execute()
      cliente = response.data[0]['nombre']
    timestampz = data[0]['created_at']
    timestampz_obj = parser.isoparse(timestampz)
    formatted_timestamp = timestampz_obj.strftime("%Y-%m-%d %H:%M:%S %Z")
    if not data:
      return "Not Found", 404
    return render_template('disp_usuario_cliente.html', data=data, timestamp=formatted_timestamp, cliente = cliente, id = id, clienteid = clienteid)
  return redirect ("/")

##EDITAR USUARIO ESPECÍFICO DE CLIENTE
@app.route ('/cliente/verusuarioscliente/usuario/edit/<id>/<clienteid>', methods = ['POST', 'GET'])
def editar_usuario_cliente(id, clienteid):
 if "user" in session:  
   username = request.form.get ('Username')
   password = request.form.get ('Password')
   password = generate_password_hash (password)
   role = request.form.get ('Role')
   if role == "admin":
      user_cliente_id = 0
   else:
      user_cliente_id = clienteid
   print (user_cliente_id)
   nombre = request.form.get ('Nombre')
   apellido = request.form.get ('Apellido')
   email = request.form.get ('Email')
   telefono = request.form.get ('Telefono')
   response = (
      supabase.table("usuarios")
      .update({
          'username' : username,
          'password' : password,
          'role' : role,
          'user_cliente_id' : user_cliente_id,
          'Nombre' : nombre,
          'Apellido' :  apellido,
          'Email' : email,
          'Telefono' : telefono
         })
      .eq("id", id)
      .execute())
   return redirect (url_for('get_usuario_cliente', id = id ))
 return redirect ("/")

##ELIMINAR USUARIO ESPECÍFICO DE CLIENTE
@app.route('/cliente/verusuarioscliente/usuario/delete/usuario/<id>/<clienteid>' , methods = ['POST', 'GET'])
def delete_usuario_cliente (id, clienteid):
 if "user" in session:  
   source_page = request.form.get('source_page')
   if source_page == 'pagina_de_cliente':
      response = supabase.table('usuarios').delete().eq('id', id).execute()
      if not response:
         return "Not Found", 404
      else:
         return redirect (url_for('ver_usuarios_cliente', id  = clienteid))
   if source_page == 'pagina_de_admin':
      response = supabase.table('usuarios').delete().eq('id', id).execute()
      if not response:
         return "Not Found", 404
      else:
         return redirect (url_for('verusuarios'))
 return redirect ("/")     


@app.route('/usuario/delete/<id>' , methods = ['POST', 'GET'])
def delete_usuario (id):
 if "user" in session:  
   source_page = request.form.get('source_page')
   if source_page == 'pagina_de_admin':
      response = supabase.table('usuarios').delete().eq('id', id).execute()
      if not response:
         return "Not Found", 404
      else:
         return redirect (url_for('ver_usuarios'))
 return redirect ("/")     
      
## AÑADIR USUARIO DE CLIENTE
@app.route ('/addusuario/<id>', methods = ['POST', 'GET'])
def add_usuario (id):
 if "user" in session:  
   source_page = request.form.get ('source_page')
   data = supabase.table ('clientes').select('nombre').eq('id', id).execute()
   cliente = data.data[0]['nombre']
   if source_page == 'pagina_de_cliente':
         Nombre = request.form.get('Nombre')
         if not Nombre:
            return  render_template('/add_usuario_cliente.html', cliente = cliente, clienteid = id)
         else:
            Apellido = request.form.get('Apellido')
            Email = request.form.get ('Email')
            Username = request.form.get ('Username')
            Password = request.form.get ('Password')
            Password = generate_password_hash (Password)
            Telefono = request.form.get ('Telefono')
            Role = request.form.get ('Role')
            response = supabase.table('usuarios').insert({
            'username': Username,
            'password': Password,
            'role' : Role,
            'user_cliente_id' : id,
            'Nombre' : Nombre,
            'Apellido' : Apellido,
            'Email' : Email,
            'Telefono' : Telefono
          }).execute()
            return redirect (url_for ('ver_usuarios_cliente', id = id))
   return render_template('/add_usuario_cliente.html', cliente = cliente, clienteid = id)
 return redirect ("/")


if __name__ == "__main__":
  app.run(host='0.0.0.0',debug=True)