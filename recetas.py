#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 23:28:49 2024

@author: mauricio
"""

import streamlit as st

import sqlite3

def insertar_receta(nombre, clasificacion, rendimiento_por_kg, rendimiento_raciones):
    # Conectar a la base de datos
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    
    # Insertar la receta
    cursor.execute('''
        INSERT INTO receta (nombre_receta, clasificación_receta, rendimiento_por_kg_receta, rendimiento_raciones)
        VALUES (?, ?, ?, ?)
    ''', (nombre, clasificacion, rendimiento_por_kg, rendimiento_raciones))
    
    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()
    print(f"Receta '{nombre}' agregada exitosamente.")

def consultar_recetas():
    # Conectar a la base de datos
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    
    # Consultar todas las recetas
    cursor.execute('SELECT * FROM receta')
    recetas = cursor.fetchall()
    
    # Obtener los nombres de las columnas
    columnas = [desc[0] for desc in cursor.description]
    
    # Convertir las filas a una lista de diccionarios
    lista_recetas = [dict(zip(columnas, receta)) for receta in recetas]
    
    # Cerrar la conexión
    conn.close()
    return lista_recetas

def modificar_receta(id_receta, nuevo_nombre, nueva_clasificacion, nuevo_rendimiento_por_kg, nuevo_rendimiento_raciones):
    # Conectar a la base de datos
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    
    # Actualizar la receta
    cursor.execute('''
        UPDATE receta
        SET nombre_receta = ?, clasificación_receta = ?, rendimiento_por_kg_receta = ?, rendimiento_raciones = ?
        WHERE id_receta = ?
    ''', (nuevo_nombre, nueva_clasificacion, nuevo_rendimiento_por_kg, nuevo_rendimiento_raciones, id_receta))
    
    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()
    print(f"Receta con ID {id_receta} modificada exitosamente.")

def eliminar_receta(id_receta):
    # Conectar a la base de datos
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    
    # Eliminar la receta
    cursor.execute('DELETE FROM receta WHERE id_receta = ?', (id_receta,))
    
    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()
    print(f"Receta con ID {id_receta} eliminada exitosamente.")


def consultar_ultima_receta():
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM receta ORDER BY id_receta DESC LIMIT 1")
    nueva_receta = cursor.fetchall()
    return nueva_receta

def consultar_subelaboracion():
    # Conectar a la base de datos
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    
    sub = 'Subelaboración'
    
    # Consultar todas las recetas
    cursor.execute("SELECT * FROM receta WHERE clasificación_receta = ?",(sub,))
    nuevas_recetas = cursor.fetchall()
    
    
    # Obtener los nombres de las columnas
    columnas = [desc[0] for desc in cursor.description]
    
    # Convertir las filas a una lista de diccionarios
    lista_recetas = [dict(zip(columnas, receta)) for receta in nuevas_recetas]
    
    # Cerrar la conexión
    conn.close()
    return lista_recetas


def consultar_ingredientes_subelaboracion(id_subelaboracion):
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    consulta = """
        SELECT
            ingrediente.id_ingrediente,
            ingrediente.nombre_ingrediente,
            ingrediente.precio_unitario_ingrediente,
            detalle_receta_ingrediente.cantidad_detalle,
            (ingrediente.precio_unitario_ingrediente * detalle_receta_ingrediente.cantidad_detalle) as subtotal
        FROM
            ingrediente
        INNER JOIN
            detalle_receta_ingrediente ON ingrediente.id_ingrediente = detalle_receta_ingrediente.ingrediente_detalle
        WHERE
            detalle_receta_ingrediente.receta_detalle = ?
    """
    
    cursor.execute(consulta,(id_subelaboracion,))
    subelaboraciones_filtradas = cursor.fetchall()
    
    columnas = [desc[0] for desc in cursor.description]
    
    lista_subelaboraciones_filtradas = [dict(zip(columnas,subelaboracion)) for subelaboracion in subelaboraciones_filtradas]
    
    conn.close()
    
    return lista_subelaboraciones_filtradas