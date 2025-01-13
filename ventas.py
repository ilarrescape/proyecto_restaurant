#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 23:40:13 2025

@author: mauricio
"""

import sqlite3

def join_ventas():
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    
    consulta = '''
        SELECT
            r.nombre_receta as "Nombre de la Receta",
            r.clasificación_receta as "Clasificación",
            v.fecha_venta as "Fecha",
            v.costo_unitario as "Costo",
            v.precio_unitario as "Precio de Venta",
            v.cantidad as "Cantidad Vendida"
        FROM
            receta as r
        INNER JOIN
            ventas as v
        ON r.id_receta = v.id_ventas
    
    '''
    
    cursor.execute(consulta)
    
    ventas = cursor.fetchall()
    
    columnas = [desc[0] for desc in cursor.description]
    
    lista_ventas = [dict(zip(columnas, venta)) for venta in ventas]
    
    conn.close()
    
    return lista_ventas