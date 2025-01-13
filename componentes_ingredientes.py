#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 04:52:36 2024

@author: mauricio
"""

import streamlit as st
import pandas as pd
from ingredientes import insertar_ingrediente, consultar_ingredientes, modificar_ingrediente, eliminar_ingrediente
import time

@st.dialog('Eliminar Ingrediente')
def remover_ingredientes(indice, df_ingredientes):
    
    nuevo_df = df_ingredientes.iloc[indice] 

    with st.form("formulario_eliminar_ingrediente"):
        
        
        st.warning(f'¿Esta seguro que quiere eliminar el ingrediente_{nuevo_df.iloc[0]["nombre_ingrediente"]}_?')
        
        _col_relleno, _col_submit = st.columns([5,3])
        with _col_submit:
            submit = st.form_submit_button('Eliminar', use_container_width=True)
        if submit:
            eliminar_ingrediente(int(nuevo_df.iloc[0]['id_ingrediente']))
            st.error(f'Ingrediente __{nuevo_df.iloc[0]['nombre_ingrediente']}__ fue eliminado exitosamente.')
            time.sleep(2)
            st.rerun()

@st.dialog('Editar Ingrediente')
def editar_ingrediente(indice, df_ingredientes):
    
    
    nuevo_df = df_ingredientes.iloc[indice]
    
    # Formulario para editar el ingrediente seleccionado
    with st.form("formulario_editar_ingrediente"):
        nuevo_nombre = st.text_input("Nombre del ingrediente", value= nuevo_df.iloc[0]['nombre_ingrediente'])
        
        lista_unidad = ["kg", "unidad", "litro"]
        
        nueva_unidad = st.selectbox("Unidad del ingrediente", options = lista_unidad, 
                                    index=lista_unidad.index(nuevo_df.iloc[0]['unidad_ingrediente']))
        nuevo_precio_unitario = st.number_input("Precio unitario del ingrediente", min_value=0.0, 
                                                value=nuevo_df.iloc[0]['precio_unitario_ingrediente'], format="%.2f")
        

    
        _col_relleno, _col_submit = st.columns([5,3])
        
        with _col_submit:
            # Botón de envío
            submit = st.form_submit_button("Guardar cambios", use_container_width=True)
            # Procesar la edición al enviar el formulario
        if submit:
            modificar_ingrediente(int(nuevo_df.iloc[0]['id_ingrediente']), nuevo_nombre, nueva_unidad, nuevo_precio_unitario)
            st.success(f"Ingrediente _{nuevo_nombre}_ actualizado exitosamente.")
            time.sleep(2)
            st.rerun()

def agregar_ingrediente():

    # Crear el formulario
    with st.form("formulario_ingrediente"):
        st.write("### Agregar un Nuevo Ingrediente")
        # Campo de entrada para el nombre del ingrediente
        nombre = st.text_input("Nombre del ingrediente")

        # Selector para la unidad del ingrediente
        unidad = st.selectbox("Unidad del ingrediente", options=["kg", "unidad", "litro"])

        # Campo de entrada para el precio unitario
        precio_unitario = st.number_input("Precio unitario del ingrediente", min_value=0.0, format="%.2f")

        # Botón de envío
        submit = st.form_submit_button("Agregar ingrediente")

    # Al hacer clic en el botón de envío
    if submit:
        if nombre and unidad and precio_unitario > 0:
            # Llamar a la función insertar_ingrediente
            insertar_ingrediente(nombre, unidad, precio_unitario)
            st.success(f"Ingrediente '{nombre}' agregado exitosamente.")
            st.rerun()
        else:
            st.error("Por favor, complet todos los campos correctamente.")


def mostrar_ingredientes():
    st.write("### Lista de Ingredientes")

    # Obtener la lista de ingredientes
    df_ingredientes = pd.DataFrame(consultar_ingredientes())

    # Verificar si hay ingredientes en la lista
    if not(df_ingredientes.empty):
        # Mostrar los ingredientes en un dataframe interactivo
        filtro_ingrediente = st.dataframe(data = df_ingredientes,
                                          use_container_width = True,
                                          selection_mode='single-row',
                                          on_select='rerun',
                                          hide_index=True,
                                          height=230)
        desactivado = True
        if filtro_ingrediente['selection']['rows']:
                desactivado = False
        
        
        _relleno, _col_agregar, _col_eliminar = st.columns([11,1,1])
        with _col_agregar:
            if st.button(label = '', icon = ':material/edit:', disabled = desactivado, use_container_width=True):
                editar_ingrediente(filtro_ingrediente['selection']['rows'], df_ingredientes)
        
        with _col_eliminar:
            if st.button(label = '', icon = ':material/delete:', disabled = desactivado, use_container_width= True):
                remover_ingredientes(filtro_ingrediente['selection']['rows'], df_ingredientes)
        
            
    else:
        st.info("No hay ingredientes registrados en la base de datos.")


def main_ingredientes():
    _col_mostrar_ingredientes, _col_agregar_ingredientes = st.columns([5,3])
    with _col_mostrar_ingredientes:
        _container_mostrar_ingredientes = st.container(border=True)
        with _container_mostrar_ingredientes:
            mostrar_ingredientes()
    with _col_agregar_ingredientes:
        agregar_ingrediente()
    
