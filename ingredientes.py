#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 04:24:49 2024

@author: mauricio
"""

import sqlite3


def insertar_ingrediente(nombre, unidad, precio_unitario):
    # Conectar a la base de datos
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    
    # Ejecutar la inserción
    cursor.execute('''
        INSERT INTO ingrediente (nombre_ingrediente, unidad_ingrediente, precio_unitario_ingrediente)
        VALUES (?, ?, ?)
    ''', (nombre, unidad, precio_unitario))
    
    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()
    print(f"Ingrediente '{nombre}' agregado exitosamente.")

def consultar_ingredientes():
    # Conectar a la base de datos
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    
    # Ejecutar la consulta
    cursor.execute('SELECT * FROM ingrediente')
    ingredientes = cursor.fetchall()
    
    # Obtener los nombres de las columnas
    columnas = [desc[0] for desc in cursor.description]
    
    # Convertir cada fila en un diccionario
    lista_ingredientes = [dict(zip(columnas, ingrediente)) for ingrediente in ingredientes]
    
    # Cerrar la conexión
    conn.close()
    
    return lista_ingredientes



def modificar_ingrediente(id_ingrediente, nuevo_nombre, nueva_unidad, nuevo_precio_unitario):
    # Conectar a la base de datos
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    
    # Ejecutar la actualización
    cursor.execute('''
        UPDATE ingrediente
        SET nombre_ingrediente = ?, unidad_ingrediente = ?, precio_unitario_ingrediente = ?
        WHERE id_ingrediente = ?
    ''', (nuevo_nombre, nueva_unidad, nuevo_precio_unitario, id_ingrediente))
    
        # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()
    print(f"Ingrediente con ID {id_ingrediente} modificado exitosamente.")

def eliminar_ingrediente(id_ingrediente):
    # Conectar a la base de datos
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    
    # Ejecutar la eliminación
    cursor.execute('''
        DELETE FROM ingrediente WHERE id_ingrediente = ?
    ''', (id_ingrediente,))
    
    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()
    print(f"Ingrediente con ID {id_ingrediente} eliminado exitosamente.")

def consultar_ingredientes_por_id(id_ingrediente):
    # Conectar a la base de datos
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    
    # Ejecutar la consulta con un filtro por ID
    query = 'SELECT * FROM ingrediente WHERE id_ingrediente = ?'
    cursor.execute(query, (id_ingrediente,))
    ingredientes = cursor.fetchall()
    
    # Obtener los nombres de las columnas
    columnas = [desc[0] for desc in cursor.description]
    
    # Convertir cada fila en un diccionario
    lista_ingredientes = [dict(zip(columnas, ingrediente)) for ingrediente in ingredientes]
    
    # Cerrar la conexión
    conn.close()
    
    return lista_ingredientes


