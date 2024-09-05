from flask import Flask, jsonify, request
from supabase import create_client, Client

app = Flask(__name__)

# Configuración de Supabase
SUPABASE_URL = "https://fwmiqngtgctfgnyjjxae.supabase.co"  # Sustituye con tu URL de Supabase
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3bWlxbmd0Z2N0ZmdueWpqeGFlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjUzOTAwNjIsImV4cCI6MjA0MDk2NjA2Mn0.VBHEMLJ5Phn6jyVAySu0TokveqEL0kCs6-VmFihS76E"  # Sustituye con tu clave de API de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

