import pyodbc
import pandas as pd
import numpy as np
from faker import Faker
import random
# datos para cuando el cliente es una persona natural y paga su propio análisis de santa cruz y sus provincias
# 1. Configuración de Faker y Conexión
fake = Faker(['es_ES'])
#10000 registros santa cruz 0
#8921 registros para lapaz 1
#5331 registros para cochabamba 2
#2613 registros para chuquisaca 3
#potosi 512 registros para potosi 4
#n_registros = 27386

def poblar_tabla_cliente():

    try:
        conn_str = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost\SQLEXPRESS;'
        'DATABASE=LabX2;'
        'Trusted_Connection=yes;'
        )
        con = pyodbc.connect(conn_str)
        cursor = con.cursor()

    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return
    
    vueltas = 5
    valor_tope = 1

    for k in range(vueltas):      
        cantidad_registros_actual = 0
        provincias = []
        pesos = []
        if k == 0:
            #Santa Cruz
            cantidad_registros_actual = 10000
            provincias = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
            pesos = [0.65, 0.08, 0.03, 0.04, 0.02, 0.02, 0.03, 0.01, 0.01, 0.06, 0.02, 0.005, 0.005, 0.01, 0.01]
        elif k == 1:
            #laPaz
            cantidad_registros_actual = 8921
            provincias = [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
            pesos = [0.02, 0.005, 0.01, 0.04, 0.02, 0.01, 0.005, 0.05,0.02, 0.005,  0.02, 0.01,  0.03, 0.02, 0.005, 0.015, 0.03, 0.01, 0.65, 0.025 ]
        elif k == 2:
            #Cochabamba
            cantidad_registros_actual = 5331
            provincias = [36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51]
            pesos = [0.01, 0.005, 0.02, 0.005, 0.02, 0.05, 0.60,  0.06, 0.03,  0.02, 0.01, 0.01,  0.03, 0.11,  0.005, 0.015]
        elif k == 3:
            #chuquisaca
            cantidad_registros_actual = 2613
            provincias = [90, 91, 92, 93, 94, 95, 96, 97, 98, 99]
            pesos = [0.02, 0.06, 0.07, 0.03, 0.12,0.55, 0.05, 0.04, 0.04, 0.02]
        elif k == 4:
            #potosi
            cantidad_registros_actual = 512
            provincias = [67, 68, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83]
            pesos = [0.02, 0.08, 0.01, 0.04, 0.10, 0.05, 0.01, 0.005, 0.04, 0.05, 0.06, 0.01, 0.12, 0.06, 0.005, 0.34]

        # 3. Generación de Datos
        pacientes_list = []
        clientes_list = []

        print(f"Generando {cantidad_registros_actual} registros...")

        for i in range(valor_tope , cantidad_registros_actual + (valor_tope - 1) + 1):
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
        valor_tope = valor_tope + cantidad_registros_actual

        # Convertir a DataFrames
        df_clientes = pd.DataFrame(clientes_list)
        df_pacientes = pd.DataFrame(pacientes_list)

        # 4. Inserción en Base de Datos
        try:
            print("Insertando Clientes...")
            cursor.executemany("""
                INSERT INTO cliente (id_cliente, nombre, apellidoP, apellidoM, nit, email, telefono, id_tipo_cliente, id_convenio)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", [tuple(x) for x in df_clientes.values])
            
            print("Insertando Pacientes...")
            cursor.executemany("""
                INSERT INTO paciente (id_paciente, nombre, apellidoP, apellidoM, telefono, email, direccion, ci, id_genero, id_provincia)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", [tuple(x) for x in df_pacientes.values])
            
            con.commit()
            print(f"¡Éxito! Se han insertado {cantidad_registros_actual} personas que son Clientes y Pacientes a la vez.")

        except Exception as e:
            print(f"Error durante la inserción: {e}")
    con.close()
    print("Conexión cerrada proceso finalizado")


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
#provincias = [67, 68, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83]
#pesos = [0.02, 0.08, 0.01, 0.04, 0.10, 0.05, 0.01, 0.005, 0.04, 0.05, 0.06, 0.01, 0.12, 0.06, 0.005, 0.34]


if __name__ == "__main__":
    poblar_tabla_cliente()


