import pyodbc
from datetime import datetime
import random

def poblar_facturacion_masiva():
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

    print("Iniciando facturación masiva de alta velocidad...")

    # 1. CARGAR PRECIOS EN MEMORIA (Para no consultar la BD en cada vuelta)
    # Creamos un diccionario: id_examen -> [(precio, fecha_inicio, fecha_fin), ...]
    print("Cargando catálogo de precios...")
    cursor.execute("SELECT id_examen, precio, fecha_inicio, ISNULL(fecha_fin, '2099-12-31') FROM examen_precio")
    precios_db = cursor.fetchall()
    mapa_precios = {}
    for id_ex, precio, f_ini, f_fin in precios_db:
        if id_ex not in mapa_precios:
            mapa_precios[id_ex] = []
        mapa_precios[id_ex].append({'p': float(precio), 'i': f_ini, 'f': f_fin})

    # 2. OBTENER ÓRDENES Y CONVENIOS
    print("Consultando órdenes pendientes de facturación...")
    cursor.execute("""
        SELECT 
            ol.id_orden_lab, 
            ol.fecha_orden, 
            doe.id_examen,
            c.porcentaje_descuento
        FROM orden_laboratorio ol
        JOIN detalle_orden_examen doe ON ol.id_orden_lab = doe.id_orden_lab
        JOIN cliente cl ON ol.id_cliente = cl.id_cliente
        JOIN convenio c ON cl.id_convenio = c.id_convenio
    """)
    
    ordenes_procesadas = {}
    
    # 3. PROCESAMIENTO EN MEMORIA
    for id_orden, fecha_o, id_ex, pct_desc in cursor.fetchall():
        # Lógica de búsqueda de precio manual (mucho más rápido que SQL en bucle)
        precio_v = 50.0 # Default
        if id_ex in mapa_precios:
            for rango in mapa_precios[id_ex]:
                if rango['i'] <= fecha_o <= rango['f']:
                    precio_v = rango['p']
                    break

        if id_orden not in ordenes_procesadas:
            ordenes_procesadas[id_orden] = {
                'fecha': fecha_o,
                'detalles': [],
                'subtotal_gral': 0.0,
                'desc_gral': 0.0,
                'pct': float(pct_desc) / 100
            }
        
        monto_desc = precio_v * ordenes_procesadas[id_orden]['pct']
        sub_linea = precio_v - monto_desc
        
        ordenes_procesadas[id_orden]['detalles'].append((precio_v, monto_desc, sub_linea, id_ex))
        ordenes_procesadas[id_orden]['subtotal_gral'] += precio_v
        ordenes_procesadas[id_orden]['desc_gral'] += monto_desc

    # 4. INSERCIÓN MASIVA (BATCHES)
    id_f_cont = 1
    id_df_cont = 1
    f_batch = []
    df_batch = []
    
    est_opciones = [1, 2, 3] # 1:Pagado, 2:Pendiente, 3:Anulado
    est_pesos = [0.85, 0.10, 0.05]

    print(f"Insertando {len(ordenes_procesadas)} facturas...")

    for id_orden, data in ordenes_procesadas.items():
        sub = data['subtotal_gral']
        desc = data['desc_gral']
        total = sub - desc
        
        f_batch.append((id_f_cont, data['fecha'], sub, desc, total, 
                        random.choices(est_opciones, weights=est_pesos)[0], 
                        id_orden, random.randint(1, 4)))

        for p_u, d_l, s_l, id_ex in data['detalles']:
            df_batch.append((id_df_cont, p_u, d_l, s_l, id_f_cont, id_ex))
            id_df_cont += 1
        
        id_f_cont += 1

        if len(f_batch) >= 1000:
            cursor.executemany("INSERT INTO factura VALUES (?,?,?,?,?,?,?,?)", f_batch)
            cursor.executemany("INSERT INTO detalle_factura VALUES (?,?,?,?,?,?)", df_batch)
            con.commit()
            f_batch, df_batch = [], []

    # Remanentes
    if f_batch:
        cursor.executemany("INSERT INTO factura VALUES (?,?,?,?,?,?,?,?)", f_batch)
        cursor.executemany("INSERT INTO detalle_factura VALUES (?,?,?,?,?,?)", df_batch)
        con.commit()

    con.close()
    print(f"Éxito: {id_f_cont-1} facturas creadas correctamente.")

if __name__ == "__main__":
    poblar_facturacion_masiva()