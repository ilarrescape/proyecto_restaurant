#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 23:42:17 2024

@author: mauricio
"""
import sqlite3

def insertar_detalle_receta_ingrediente(ingrediente_id, receta_id, cantidad):
    # Conectar a la base de datos
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    
    # Insertar el detalle de receta-ingrediente
    cursor.execute('''
        INSERT INTO detalle_receta_ingrediente (ingrediente_detalle, receta_detalle, cantidad_detalle)
        VALUES (?, ?, ?)
    ''', (ingrediente_id, receta_id, cantidad))
    
    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()
    print(f"Detalle para el ingrediente ID {ingrediente_id} y receta ID {receta_id} agregado exitosamente.")


def consultar_detalles_receta_ingrediente():
    # Conectar a la base de datos
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    
    # Consultar todos los detalles de receta-ingrediente
    cursor.execute('SELECT * FROM detalle_receta_ingrediente')
    detalles = cursor.fetchall()
    
    # Obtener los nombres de las columnas
    columnas = [desc[0] for desc in cursor.description]
    
    # Convertir las filas a una lista de diccionarios
    lista_detalles = [dict(zip(columnas, detalle)) for detalle in detalles]
    
    # Cerrar la conexión
    conn.close()
    return lista_detalles


def modificar_detalle_receta_ingrediente(id_detalle, nuevo_ingrediente_id, nueva_receta_id, nueva_cantidad):
    # Conectar a la base de datos
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    
    # Actualizar el detalle de receta-ingrediente
    cursor.execute('''
        UPDATE detalle_receta_ingrediente
        SET ingrediente_detalle = ?, receta_detalle = ?, cantidad_detalle = ?
        WHERE id_detalle = ?
    ''', (nuevo_ingrediente_id, nueva_receta_id, nueva_cantidad, id_detalle))
    
    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()
    print(f"Detalle con ID {id_detalle} modificado exitosamente.")


def eliminar_detalle_receta_ingrediente(id_ingrediente, id_receta):
    # Conectar a la base de datos
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    
    # Eliminar el detalle de receta-ingrediente
    cursor.execute('DELETE FROM detalle_receta_ingrediente WHERE ingrediente_detalle = ? and receta_detalle = ?', (id_ingrediente,id_receta))
    
    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()


def consultar_detalles_receta_ingrediente_por_id_receta(id_receta):
    # Conectar a la base de datos
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    
    # Consultar todos los detalles de receta-ingrediente
    cursor.execute('SELECT * FROM detalle_receta_ingrediente WHERE receta_detalle = ?',(id_receta,))
    detalles = cursor.fetchall()
    
    # Obtener los nombres de las columnas
    columnas = [desc[0] for desc in cursor.description]
    
    # Convertir las filas a una lista de diccionarios
    lista_detalles = [dict(zip(columnas, detalle)) for detalle in detalles]
    
    # Cerrar la conexión
    conn.close()
    return lista_detalles

def recuperar_ultimo_detalle():
    
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM detalle_receta_ingrediente ORDER BY id_detalle DESC LIMIT 1')
    
    detalles = cursor.fetchall()
    
    columnas = [desc[0] for desc in cursor.description]
    
    lista_detalles = [dict(zip(columnas, detalles)) for detalle in detalles]
    
    id_detalle = lista_detalles[0]['id_detalle'][0]
    conn.close()
    return id_detalle

def eliminar_detalle_receta_ingrediente_por_receta(id_receta):
    # Conectar a la base de datos
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    
    # Eliminar el detalle de receta-ingrediente
    cursor.execute('DELETE FROM detalle_receta_ingrediente WHERE receta_detalle = ?', (id_receta,))
    
    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()
