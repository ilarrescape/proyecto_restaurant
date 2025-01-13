#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 10:51:05 2024

@author: mauricio
"""

import sqlite3

def insertar_detalle_receta_subelaboracion(receta_id, subelaboracion_id, subelaboracion_peso):
    # Conectar a la base de datos
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    
    # Insertar el detalle de receta-ingrediente
    cursor.execute('''
        INSERT INTO detalle_subelaboracion_receta (id_receta, id_subelaboracion, peso_subelaboracion)
        VALUES (?,?,?)
    ''', (receta_id, subelaboracion_id, subelaboracion_peso))
    
    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()


def consultar_detalles_receta_subelaboracion():
    # Conectar a la base de datos
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    
    # Consultar todos los detalles de receta-ingrediente
    cursor.execute('SELECT * FROM detalle_subelaboracion_receta')
    detalles = cursor.fetchall()
    
    
    # Obtener los nombres de las columnas
    columnas = [desc[0] for desc in cursor.description]
    
    # Convertir las filas a una lista de diccionarios
    lista_detalles = [dict(zip(columnas, detalle)) for detalle in detalles]
    
    # Cerrar la conexión
    conn.close()
    return lista_detalles

#   modificar_detalle_receta_subelaboracion(int(id_receta), int(diccionario_subelaboracion['id_receta']), int(serie_df_subelaboracion.loc['id_subelaboracion']), round(cantidad_detalle,3))

def modificar_detalle_receta_subelaboracion(receta_id, subelaboracion_id, subelaboracion_id_modificar, subelaboracion_peso):
    # Conectar a la base de datos
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    
    # Actualizar el detalle de receta-ingrediente
    cursor.execute('''
        UPDATE detalle_subelaboracion_receta
        SET id_receta = ?, id_subelaboracion = ?, peso_subelaboracion = ?
        WHERE id_receta = ? AND id_subelaboracion = ?
    ''', (receta_id, subelaboracion_id_modificar, subelaboracion_peso, receta_id, subelaboracion_id))
    
    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()
    

def eliminar_detalle_receta_ingrediente(receta_id, subelaboracion_id):
    # Conectar a la base de datos
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    
    # Eliminar el detalle de receta-ingrediente
    cursor.execute('DELETE FROM detalle_subelaboracion_receta WHERE id_receta = ? and id_subelaboracion', (receta_id,subelaboracion_id))
    
    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()


def eliminar_detalle_receta_subelaboracion(receta_id,subelaboracion_id):
    # Conectar a la base de datos
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    
    # Eliminar el detalle de receta-ingrediente
    cursor.execute('DELETE FROM detalle_subelaboracion_receta WHERE id_receta = ? and id_subelaboracion = ?', (receta_id,subelaboracion_id))
    
    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()    

def eliminar_detalle_receta_subelaboracion_por_receta(receta_id):
    # Conectar a la base de datos
    conn = sqlite3.connect('recetas.db')
    cursor = conn.cursor()
    
    # Eliminar el detalle de receta-ingrediente
    cursor.execute('DELETE FROM detalle_subelaboracion_receta WHERE id_receta = ?', (receta_id,))
    
    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()    


