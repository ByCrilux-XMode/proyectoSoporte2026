import pyodbc
import pandas as pd
import numpy as np
from faker import Faker
import random
# datos para cuando el cliente es una persona natural y paga su propio análisis de santa cruz y sus provincias
# 1. Configuración de Faker y Conexión
fake = Faker(['es_ES'])
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-KSBD4JM\\SOPO2025;'
    'DATABASE=LabX2;'
    'Trusted_Connection=yes;'
)
#10000 registros santa cruz
#8921 registros para lapaz
#5331 registros para cochabamba
#2613 registros para chuquisaca
#potosi 512 registros para potosi
n_registros = 27386

# 2. Configuración de Provincias con Pesos (Prioridad poblacional)
# El peso determina la probabilidad de que salga esa ID

#Santa Cruz
#provincias = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
#pesos = [0.65, 0.08, 0.03, 0.04, 0.02, 0.02, 0.03, 0.01, 0.01, 0.06, 0.02, 0.005, 0.005, 0.01, 0.01]

#laPaz
#provincias = [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
#pesos = [0.02, 0.005, 0.01, 0.04, 0.02, 0.01, 0.005, 0.05,0.02, 0.005,  0.02, 0.01,  0.03, 0.02, 0.005, 0.015, 0.03, 0.01, 0.65, 0.025 ]

#Cochabamba
#provincias = [36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51]
#pesos = [0.01, 0.005, 0.02, 0.005, 0.02, 0.05, 0.60,  0.06, 0.03,  0.02, 0.01, 0.01,  0.03, 0.11,  0.005, 0.015]

#chuquisaca
#provincias = [90, 91, 92, 93, 94, 95, 96, 97, 98, 99]
#pesos = [0.02, 0.06, 0.07, 0.03, 0.12,0.55, 0.05, 0.04, 0.04, 0.02]

#potosi
provincias = [67, 68, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83]
pesos = [0.02, 0.08, 0.01, 0.04, 0.10, 0.05, 0.01, 0.005, 0.04, 0.05, 0.06, 0.01, 0.12, 0.06, 0.005, 0.34]

# 3. Generación de Datos
pacientes_list = []
clientes_list = []

print(f"Generando {n_registros} registros...")

for i in range(26866 , n_registros + 1):
    # Datos base
    genero_id = random.choice([1, 2])
    nombre = fake.first_name_male() if genero_id == 1 else fake.first_name_female()
    apellido_p = fake.last_name()
    apellido_m = fake.last_name()
    ci_nit = str(random.randint(4000000, 9000000))
    email = fake.ascii_free_email()
    telefono = str(random.randint(60000000, 79999999))
    
    # Llenamos lista de Clientes
    clientes_list.append({
        'id_cliente': i,
        'nombre': nombre,
        'apellidoP': apellido_p,
        'apellidoM': apellido_m,
        'nit': ci_nit,
        'email': email,
        'telefono': telefono,
        'id_tipo_cliente': 1, # Persona Natural
        'id_convenio': 1      # Particular
    })
    
    # Llenamos lista de Pacientes
    pacientes_list.append({
        'id_paciente': i,
        'nombre': nombre,
        'apellidoP': apellido_p,
        'apellidoM': apellido_m,
        'telefono': telefono,
        'email': email,
        'direccion': f"{fake.street_name()} {fake.building_number()}",
        'ci': ci_nit,
        'id_genero': genero_id,
        'id_provincia': random.choices(provincias, weights=pesos, k=1)[0]
    })

# Convertir a DataFrames
df_clientes = pd.DataFrame(clientes_list)
df_pacientes = pd.DataFrame(pacientes_list)

# 4. Inserción en Base de Datos
try:
    con = pyodbc.connect(conn_str)
    cursor = con.cursor()
    
    print("Insertando Clientes...")
    cursor.executemany("""
        INSERT INTO cliente (id_cliente, nombre, apellidoP, apellidoM, nit, email, telefono, id_tipo_cliente, id_convenio)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", [tuple(x) for x in df_clientes.values])
    
    print("Insertando Pacientes...")
    cursor.executemany("""
        INSERT INTO paciente (id_paciente, nombre, apellidoP, apellidoM, telefono, email, direccion, ci, id_genero, id_provincia)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", [tuple(x) for x in df_pacientes.values])
    
    con.commit()
    print(f"¡Éxito! Se han insertado {n_registros} personas que son Clientes y Pacientes a la vez.")

except Exception as e:
    print(f"Error durante la inserción: {e}")
finally:
    if 'con' in locals():
        con.close()