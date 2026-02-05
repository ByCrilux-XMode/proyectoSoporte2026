import pyodbc
from faker import Faker
import random

fake = Faker(['es_ES'])

def poblar_clientes_y_convenios():
    conn_str = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'
        'DATABASE=LabX2;'
        'Trusted_Connection=yes;'
    )
    
    try:
        con = pyodbc.connect(conn_str)
        cursor = con.cursor()
    except Exception as e:
        print(f"Error de conexión: {e}")
        return

    # 1. Configuración de Universos Regionales
    config_regiones = [
        {"nombre": "Santa Cruz", "reg": 89764, "provs": list(range(1, 16)), "pesos": [0.65, 0.08, 0.03, 0.04, 0.02, 0.02, 0.03, 0.01, 0.01, 0.06, 0.02, 0.005, 0.005, 0.01, 0.01]},
        {"nombre": "La Paz", "reg": 41123, "provs": list(range(16, 36)), "pesos": [0.02, 0.005, 0.01, 0.04, 0.02, 0.01, 0.005, 0.05, 0.02, 0.005, 0.02, 0.01, 0.03, 0.02, 0.005, 0.015, 0.03, 0.01, 0.65, 0.025]},
        {"nombre": "Cochabamba", "reg": 30547, "provs": list(range(36, 52)), "pesos": [0.01, 0.005, 0.02, 0.005, 0.02, 0.05, 0.60, 0.06, 0.03, 0.02, 0.01, 0.01, 0.03, 0.11, 0.005, 0.015]},
        {"nombre": "Chuquisaca", "reg": 10121, "provs": list(range(90, 100)), "pesos": [0.02, 0.06, 0.07, 0.03, 0.12, 0.55, 0.05, 0.04, 0.04, 0.02]},
        {"nombre": "Potosí", "reg": 12438, "provs": [67, 68, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83], "pesos": [0.02, 0.08, 0.01, 0.04, 0.10, 0.05, 0.01, 0.005, 0.04, 0.05, 0.06, 0.01, 0.12, 0.06, 0.005, 0.34]},
        {"nombre": "Oruro","reg": 13291,"provs": [52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66],"pesos": [0.60, 0.05, 0.03, 0.01, 0.02, 0.05, 0.02, 0.03, 0.01, 0.03, 0.03, 0.02, 0.03, 0.02, 0.05]},
        {"nombre": "Pando","reg": 2716,"provs": [108, 109, 110, 111, 112],"pesos": [0.05, 0.05, 0.15, 0.10, 0.65]}
    ]

    # 2. Configuración de Clientes Corporativos (Seguros/Empresas)
    # Formato: (id_tipo_cliente, id_convenio, nombre_entidad, nit)
    pool_corporativos = [
        (2, 2, "Caja Petrolera de Salud", "10203040"),
        (2, 3, "Bisa Seguros", "50607080"),
        (3, 4, "YPFB Transporte", "90010020"),
        (4, 5, "Campaña Preventiva Gob", "33445566")
    ]

    id_cliente_cont = 1
    id_paciente_cont = 1

    for region in config_regiones:
        clientes_batch = []
        pacientes_batch = []
        print(f"Procesando {region['nombre']}...")

        for _ in range(region['reg']):
            # Datos base del Paciente
            gen_p = random.choice([1, 2])
            nom_p = fake.first_name_male() if gen_p == 1 else fake.first_name_female()
            ape_p = fake.last_name()
            ape_m = fake.last_name()
            ci_p = str(random.randint(4000000, 9000000))
            edad_p = random.randint(0, 90)

            # --- Lógica de Cliente ---
            # 80% son Personas Naturales, 20% son Corporativos/Seguros
            tipo_azar = random.random()
            
            if tipo_azar < 0.80:
                # CASO 1: PERSONA NATURAL (Tipo 1, Convenio 1)
                es_mismo = random.random() < 0.85 # 85% el mismo paciente paga
                
                if es_mismo:
                    cli_data = (id_cliente_cont, nom_p, ape_p, ape_m, ci_p, fake.ascii_free_email(), 
                                str(random.randint(60000000, 79999999)), 1, 1)
                else:
                    # Paga un familiar
                    cli_data = (id_cliente_cont, fake.first_name(), fake.last_name(), fake.last_name(), 
                                str(random.randint(1000000, 3000000)), fake.ascii_free_email(), 
                                str(random.randint(60000000, 79999999)), 1, 1)
            else:
                # CASO 2: CORPORATIVO (Seguros, Empresas, etc.)
                corp = random.choice(pool_corporativos)
                cli_data = (id_cliente_cont, corp[2], "S.A.", "INSTITUCIONAL", corp[3], 
                            "administracion@correo.com", "33445566", corp[0], corp[1])

            # Añadir a las listas
            clientes_batch.append(cli_data)
            pacientes_batch.append((
                id_paciente_cont, nom_p, ape_p, ape_m, str(random.randint(60000000, 79999999)),
                fake.ascii_free_email(), f"{fake.street_name()} #{fake.building_number()}",
                ci_p, gen_p, random.choices(region['provs'], weights=region['pesos'], k=1)[0], edad_p
            ))

            id_cliente_cont += 1
            id_paciente_cont += 1

        # Inserción por región
        try:
            cursor.executemany("INSERT INTO cliente VALUES (?,?,?,?,?,?,?,?,?)", clientes_batch)
            cursor.executemany("INSERT INTO paciente VALUES (?,?,?,?,?,?,?,?,?,?,?)", pacientes_batch)
            con.commit()
            print(f"Insertados {region['reg']} registros de {region['nombre']}.")
        except Exception as e:
            print(f"Error insertando {region['nombre']}: {e}")
            con.rollback()

    con.close()
    print("--- Proceso finalizado exitosamente ---")

if __name__ == "__main__":
    poblar_clientes_y_convenios()