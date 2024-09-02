from flask import Flask
from flask import render_template
app = Flask(__name__)

DISP = [
  {
    'id': 1,
    'MAC': '00:00:00:00:00:01',
    'location': 'CDMX',
    'status': '1'
  },
  {
    'id': 2,
    'MAC': '00:00:00:00:00:02',
    'location': 'GDL',
    'status': '0'
  },
  {
    'id': 3,
    'MAC': '00:00:00:00:00:03',
    'location': 'MTR',
    'status': '1'
  },
]

@app.route("/")
def hello_world():
    return render_template('home.html', disps= DISP)
  
if __name__ == "__main__":
  app.run(host='0.0.0.0',debug=True)