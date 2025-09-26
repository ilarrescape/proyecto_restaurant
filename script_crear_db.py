#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 04:11:40 2024

@author: mauricio
"""

import sqlite3

import auth

# Conectar y crear el archivo de base de datos
conn = sqlite3.connect('recetas.db')
cursor = conn.cursor()

# Crear la tabla receta
cursor.execute('''
    CREATE TABLE IF NOT EXISTS receta (
        id_receta INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_receta TEXT NOT NULL,
        clasificación_receta TEXT CHECK(clasificación_receta IN ('Entrada', 'Desayuno', 'Plato Principal', 'postre', 'Subelaboración')) NOT NULL,
        rendimiento_por_kg_receta REAL,
        rendimiento_raciones INTEGER
    )
''')

# Crear la tabla ingrediente
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ingrediente (
        id_ingrediente INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_ingrediente TEXT NOT NULL,
        unidad_ingrediente TEXT CHECK(unidad_ingrediente IN ('kg', 'unidad', 'litro')) NOT NULL,
        precio_unitario_ingrediente REAL
    )
''')

# Crear la tabla detalle_receta_ingrediente
cursor.execute('''
    CREATE TABLE IF NOT EXISTS detalle_receta_ingrediente (
        id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
        ingrediente_detalle INTEGER,
        receta_detalle INTEGER,
        cantidad_detalle REAL,
        FOREIGN KEY (ingrediente_detalle) REFERENCES ingrediente(id_ingrediente),
        FOREIGN KEY (receta_detalle) REFERENCES receta(id_receta)
    )
''')

# Crear la tabla detalle_subelaboracion_receta
cursor.execute('''
    CREATE TABLE IF NOT EXISTS detalle_subelaboracion_receta (
        id_receta INTEGER,
        id_subelaboracion INTEGER,
        PRIMARY KEY (id_receta, id_subelaboracion),
        FOREIGN KEY (id_receta) REFERENCES receta(id_receta),
        FOREIGN KEY (id_subelaboracion) REFERENCES receta(id_receta)
    )
''')

# Crear la tabla de usuarios segura
auth.initialize_user_table()

# Guardar los cambios
conn.commit()

# Cerrar la conexión
conn.close()
