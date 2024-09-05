from flask import Flask, jsonify
from flask import render_template, redirect, url_for
from flask import Flask, jsonify, request
from supabase import create_client, Client

app = Flask(__name__)

# Configuración de Supabase
SUPABASE_URL = "https://fwmiqngtgctfgnyjjxae.supabase.co"  # Sustituye con tu URL de Supabase
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3bWlxbmd0Z2N0ZmdueWpqeGFlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjUzOTAwNjIsImV4cCI6MjA0MDk2NjA2Mn0.VBHEMLJ5Phn6jyVAySu0TokveqEL0kCs6-VmFihS76E"  # Sustituye con tu clave de API de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/', methods=['GET'])
def get_data():
    # Ejemplo de consulta a la base de datos
    response = supabase.table('dispositivos').select('*').order('id', desc = False).execute()
    data = response.data
    return render_template('home.html', data=data)

@app.route('/disp/<id>', methods=['GET'])
def get_disp(id):
    desired_value = id
    response = supabase.table('dispositivos').select('*').eq('id', desired_value).limit(1).execute()
    data = response.data
    if not data:
      return "Not Found", 404
    return render_template('disp.html', data=data)

@app.route('/add', methods =['POST', 'GET'])
def add():
    MAC_data = request.form.get('MAC')
    if not MAC_data:
       return  render_template('add_disp.html')
    else:
      MAC_data = str (MAC_data)
      MAC_data = MAC_data.upper()
      Location_data= request.form.get('Location')
      Status_data = request.form.get ('Status')
      response = supabase.table('dispositivos').insert({
          'MAC': MAC_data,
          'Location': Location_data,
          'Status' : Status_data    
          }).execute()
      return redirect('/')
    
      

if __name__ == "__main__":
  app.run(host='0.0.0.0',debug=True)