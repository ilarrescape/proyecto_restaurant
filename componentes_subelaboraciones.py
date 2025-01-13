#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 20:06:52 2024

@author: mauricio
"""
import recetas
import ingredientes
from ingredientes import consultar_ingredientes_por_id
import detalle_recetas_ingredientes
import streamlit as st
import pandas as pd
import time

def eliminar_subelaboracion_temporal(seleccion):
    indice_auxiliar = seleccion['selection']['rows']
    st.session_state.seleccion_subelaboraciones.drop(indice_auxiliar, axis=0, inplace = True)
    st.session_state.seleccion_subelaboraciones.reset_index(drop = True, inplace = True)
    st.rerun()

@st.dialog('Editar Subelaboracion')
def editar_subelaboracion_temporal(seleccion,lista_subelaboracion):
    
    indice_auxiliar = seleccion['selection']['rows']
    serie_df_subelaboracion = st.session_state.seleccion_subelaboraciones.iloc[indice_auxiliar[0]]
    
    st.write(serie_df_subelaboracion)
    
    dic_subelaboracion = {row['nombre_receta']:row['id_receta'] for row in lista_subelaboracion}

    lista_nombre_subelaboracion = list(dic_subelaboracion.keys())

    select_subelaboracion = st.selectbox('Ingresar Subelaboracion', dic_subelaboracion,index= lista_nombre_subelaboracion.index(serie_df_subelaboracion['nombre_subelaboracion']))
    
    
    #Buscamos todos los detalles de la saubelaboracion,ingresando el id de la subelaboracion asociada
    lista_detalle = detalle_recetas_ingredientes.consultar_detalles_receta_ingrediente_por_id_receta(int(dic_subelaboracion[str(select_subelaboracion)]))
    
    
    dic_nombre_precio_ingrediente = ingredientes_precio = {
                                    row['nombre_ingrediente']: [row['id_ingrediente'], row['precio_unitario_ingrediente'],row['unidad_ingrediente']]
                                    for valor in lista_detalle
                                    for row in ingredientes.consultar_ingredientes_por_id(int(valor['ingrediente_detalle']))}
    
    for fila in lista_detalle:
        for valor in dic_nombre_precio_ingrediente.values():
            if valor[0] == fila['ingrediente_detalle']:
                valor.append(fila['cantidad_detalle'])
                valor.append(fila['cantidad_detalle']*valor[1])
    
    
    diccionario_subelaboracion = [fila for fila in lista_subelaboracion  if fila['nombre_receta'] == select_subelaboracion][0]
    
    precio_total = sum(valor[4] for valor in dic_nombre_precio_ingrediente.values())
    
    diccionario_subelaboracion.update({'precio_total':precio_total})
    
    diccionario_subelaboracion['precio_por_kg'] = round(diccionario_subelaboracion['precio_total']/diccionario_subelaboracion['rendimiento_por_kg_receta'],2)
    
    cantidad_detalle = st.number_input('Ingresar Cantidad: ', format='%3.f', step=0.25, value= round(serie_df_subelaboracion['peso_subelaboracion'],3))
    rendimiento_detalle = round(cantidad_detalle * diccionario_subelaboracion['rendimiento_raciones']/diccionario_subelaboracion["rendimiento_por_kg_receta"],2)
    
    peso_racion = diccionario_subelaboracion["rendimiento_por_kg_receta"]/diccionario_subelaboracion["rendimiento_raciones"]
    
    _col_a, _col_b = st.columns(2)
    with _col_a:
        with st.container(border=True):
            st.markdown(f'<p style="color:white; font-size:15px;text-align:center;border-bottom: 2px solid #262730;padding-bottom:0.5em;">Raciones</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:yellow; font-size:20px;text-align:center;">{rendimiento_detalle}</p>', unsafe_allow_html=True)    
        with st.container(border = True):
            st.markdown(f'<p style="color:white; font-size:15px;text-align:center;border-bottom: 2px solid #262730;padding-bottom:0.5em;">Valor Por Racion ({round(peso_racion,3)})</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:green; font-size:20px;text-align:center;">$ {round(peso_racion*diccionario_subelaboracion["precio_por_kg"])}</p>', unsafe_allow_html=True)
        
    with _col_b:
        with st.container(border = True):
            st.markdown(f'<p style="color:white; font-size:15px;text-align:center;border-bottom: 2px solid #262730;padding-bottom:0.5em;">Valor por Kg</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:#26C6DA; font-size:20px;text-align:center;">$ {diccionario_subelaboracion["precio_por_kg"]}</p>', unsafe_allow_html=True) 
        
        valor_por_seleccion = float(diccionario_subelaboracion["precio_por_kg"]*cantidad_detalle) if cantidad_detalle > 0 else 0.0
        with st.container(border = True):
            st.markdown(f'<p style="color:white; font-size:15px;text-align:center;border-bottom: 2px solid #262730;padding-bottom:0.5em;">Valor por Cantidad</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:#FF9999; font-size:20px;text-align:center;">$ {round(valor_por_seleccion)}</p>', unsafe_allow_html=True)
    
    diccionario_guardar_subelaboracion = {
            'id_subelaboracion' : diccionario_subelaboracion['id_receta'],
            'nombre_subelaboracion' : diccionario_subelaboracion['nombre_receta'],
            'peso_subelaboracion' : round(cantidad_detalle,3),
            'cantidad_raciones_subelaboracion': rendimiento_detalle,
            'valor_subelaboracion': round(valor_por_seleccion,2)
        }
    
    if st.button('Guardar Subelaboracion'):
        st.session_state.seleccion_subelaboraciones.loc[indice_auxiliar[0], diccionario_guardar_subelaboracion.keys()] = diccionario_guardar_subelaboracion.values()
        st.rerun()



@st.dialog('Agregar Subelaboracion')
def agregar_subelaboracion():
    lista_subelaboracion = recetas.consultar_subelaboracion()
    
    dic_subelaboracion = {row['nombre_receta']:row['id_receta'] for row in lista_subelaboracion}

    select_subelaboracion = st.selectbox('Ingresar Subelaboracion', dic_subelaboracion)
    
    
    #Buscamos todos los detalles de la saubelaboracion,ingresando el id de la subelaboracion asociada
    lista_detalle = detalle_recetas_ingredientes.consultar_detalles_receta_ingrediente_por_id_receta(int(dic_subelaboracion[str(select_subelaboracion)]))
    
    
    dic_nombre_precio_ingrediente = ingredientes_precio = {
                                    row['nombre_ingrediente']: [row['id_ingrediente'], row['precio_unitario_ingrediente'],row['unidad_ingrediente']]
                                    for valor in lista_detalle
                                    for row in ingredientes.consultar_ingredientes_por_id(int(valor['ingrediente_detalle']))}
    
    for fila in lista_detalle:
        for valor in dic_nombre_precio_ingrediente.values():
            if valor[0] == fila['ingrediente_detalle']:
                valor.append(fila['cantidad_detalle'])
                valor.append(fila['cantidad_detalle']*valor[1])
    
    
    diccionario_subelaboracion = [fila for fila in lista_subelaboracion  if fila['nombre_receta'] == select_subelaboracion][0]
    
    precio_total = sum(valor[4] for valor in dic_nombre_precio_ingrediente.values())
    
    diccionario_subelaboracion.update({'precio_total':precio_total})
    
    diccionario_subelaboracion['precio_por_kg'] = round(diccionario_subelaboracion['precio_total']/diccionario_subelaboracion['rendimiento_por_kg_receta'],2)
    
    cantidad_detalle = st.number_input('Ingresar Cantidad: ', format='%3.f', step=0.25, value= round(diccionario_subelaboracion["rendimiento_por_kg_receta"]/diccionario_subelaboracion["rendimiento_raciones"],3))
    rendimiento_detalle = round(cantidad_detalle * diccionario_subelaboracion['rendimiento_raciones']/diccionario_subelaboracion["rendimiento_por_kg_receta"],2)
    
    peso_racion = diccionario_subelaboracion["rendimiento_por_kg_receta"]/diccionario_subelaboracion["rendimiento_raciones"]
    
    _col_a, _col_b = st.columns(2)
    with _col_a:
        with st.container(border=True):
            st.markdown(f'<p style="color:white; font-size:15px;text-align:center;border-bottom: 2px solid #262730;padding-bottom:0.5em;">Raciones</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:yellow; font-size:20px;text-align:center;">{rendimiento_detalle}</p>', unsafe_allow_html=True)    
        with st.container(border = True):
            st.markdown(f'<p style="color:white; font-size:15px;text-align:center;border-bottom: 2px solid #262730;padding-bottom:0.5em;">Valor Por Racion ({round(peso_racion,3)})</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:green; font-size:20px;text-align:center;">$ {round(peso_racion*diccionario_subelaboracion["precio_por_kg"])}</p>', unsafe_allow_html=True)
        
    with _col_b:
        with st.container(border = True):
            st.markdown(f'<p style="color:white; font-size:15px;text-align:center;border-bottom: 2px solid #262730;padding-bottom:0.5em;">Valor por Kg</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:#26C6DA; font-size:20px;text-align:center;">$ {diccionario_subelaboracion["precio_por_kg"]}</p>', unsafe_allow_html=True) 
        
        valor_por_seleccion = float(diccionario_subelaboracion["precio_por_kg"]*cantidad_detalle) if cantidad_detalle > 0 else 0.0
        with st.container(border = True):
            st.markdown(f'<p style="color:white; font-size:15px;text-align:center;border-bottom: 2px solid #262730;padding-bottom:0.5em;">Valor por Cantidad</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:#FF9999; font-size:20px;text-align:center;">$ {round(valor_por_seleccion)}</p>', unsafe_allow_html=True)
    
    diccionario_guardar_subelaboracion = {
            'id_subelaboracion' : diccionario_subelaboracion['id_receta'],
            'nombre_subelaboracion' : diccionario_subelaboracion['nombre_receta'],
            'peso_subelaboracion' : round(cantidad_detalle,3),
            'cantidad_raciones_subelaboracion': rendimiento_detalle,
            'valor_subelaboracion': round(valor_por_seleccion,2)
        }
    
    if st.button('Guardar Subelaboracion'):
        st.session_state.seleccion_subelaboraciones.loc[len(st.session_state['seleccion_subelaboraciones'])] = diccionario_guardar_subelaboracion
        st.rerun()


def iniciar_seleccion():
    if 'seleccion_subelaboraciones' not in st.session_state:
        columnas = ['id_subelaboracion', 'nombre_subelaboracion', 'peso_subelaboracion', 'cantidad_raciones_subelaboracion', 'valor_subelaboracion']
        df = pd.DataFrame(columns=columnas)
        st.session_state['seleccion_subelaboraciones'] = df

def reiniciar_subelaboracion():
    columnas = ['id_subelaboracion', 'nombre_subelaboracion', 'peso_subelaboracion', 'cantidad_raciones_subelaboracion', 'valor_subelaboracion']
    df = pd.DataFrame(columns=columnas)
    st.session_state['seleccion_subelaboraciones'] = df
    
    # st.session_state.nombre_receta = ''
    # st.session_state.rendimiento_peso = 0
    # st.session_state.peso_porcion = 0


def visualizar_subelaboraciones():
    iniciar_seleccion()
    seleccion_subelaboracion = st.dataframe(st.session_state.seleccion_subelaboraciones,
                                            hide_index=True,
                                            use_container_width=True,
                                            selection_mode='single-row',
                                            on_select='rerun',
                                            height=390,
                                            column_order=['nombre_subelaboracion','peso_subelaboracion','cantidad_raciones_subelaboracion', 'valor_subelaboracion'])
    
    if seleccion_subelaboracion['selection']['rows']:
        _col_relleno, _col_eliminar, _col_editar = st.columns([6,2,2])
        with _col_eliminar:
            if st.button('Subelaboracion', icon=':material/delete:', use_container_width=True):
                eliminar_subelaboracion_temporal(seleccion_subelaboracion)
        
        with _col_editar:
            
            lista_subelaboracion = recetas.consultar_subelaboracion()
            
            if st.button('Subelaboracion',icon=':material/edit:', use_container_width=True):
                editar_subelaboracion_temporal(seleccion_subelaboracion, lista_subelaboracion)
    else:
        _col_relleno, _col_agregar = st.columns([8,2])
        with _col_agregar:
            if st.button('__+__ Subelaboracion', use_container_width=True):
                agregar_subelaboracion()