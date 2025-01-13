#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 23:44:14 2024

@author: mauricio
"""

import recetas
import ingredientes
from ingredientes import consultar_ingredientes_por_id
from componentes_subelaboraciones import visualizar_subelaboraciones, reiniciar_subelaboracion

import detalle_recetas_ingredientes
import detalle_receta_subelaboracion
import streamlit as st
import pandas as pd


import time

from streamlit_lottie import st_lottie
import requests



def iniciar_seleccion():
    if 'seleccion_ingredientes' not in st.session_state:
        columnas = ['id_ingrediente', 'nombre_ingrediente', 'unidad_ingrediente', 'cantidad_ingrediente', 'subtotal_ingrediente']
        df = pd.DataFrame(columns=columnas)
        st.session_state['seleccion_ingredientes'] = df

def reininiciar_seleccion():
    columnas = ['id_ingrediente', 'nombre_ingrediente', 'unidad_ingrediente', 'cantidad_ingrediente', 'subtotal_ingrediente']
    df = pd.DataFrame(columns=columnas)
    st.session_state['seleccion_ingredientes'] = df
    
    st.session_state.nombre_receta = ''
    st.session_state.rendimiento_peso = 0
    st.session_state.peso_porcion = 0


def eliminar_ingrediente_temporal(seleccion):
    indice_auxiliar = seleccion['selection']['rows']
    st.session_state.seleccion_ingredientes.drop(indice_auxiliar, axis=0, inplace = True)
    st.session_state.seleccion_ingredientes.reset_index(drop = True, inplace = True)
    st.rerun()


@st.dialog("Editar Ingrediente")
def editar_ingrediente_temporal(seleccion,lista_ingredientes):  
    
    # Generamos la serie
    indice_auxiliar = seleccion['selection']['rows']
    serie_df = st.session_state.seleccion_ingredientes.iloc[indice_auxiliar[0]]
    
    # Generamos el diccionario de ingredientes y extraemos los nombres para guardarlos en una lista
    dic_ingredientes = {row['nombre_ingrediente']: row['id_ingrediente'] for row in lista_ingredientes}
    lista_nombre_ingredientes = list(dic_ingredientes.keys())
    
    # Mostramos en el selectbox el nombre del ingrediente que se filtro
    cmb_ingredientes = st.selectbox('Seleccionar Ingredientes', lista_nombre_ingredientes, index= lista_nombre_ingredientes.index(serie_df['nombre_ingrediente']))
    lista_ingredientes = consultar_ingredientes_por_id(dic_ingredientes[cmb_ingredientes])
    txt_unidad = st.text_input('Unidad: ',value=lista_ingredientes[0]['unidad_ingrediente'], disabled=True)
    label_precio = f"Precio por {lista_ingredientes[0]['unidad_ingrediente']}:"
    valor = f"${lista_ingredientes[0]['precio_unitario_ingrediente']:,.2f}"
    txt_precio = st.text_input(label_precio,value=valor, disabled=True)
    nmb_cantidad = st.number_input(f"Ingresar cantidad en {lista_ingredientes[0]['unidad_ingrediente']}:",format='%2.f',step=0.25, value= serie_df['cantidad_ingrediente'])
    subtotal = lista_ingredientes[0]['precio_unitario_ingrediente'] * nmb_cantidad
    st.info(f'El subtotal es __${subtotal:,.2f}__')
    
    #Agregamos los nuevos datos al diccionario
    diccionario_editar = {
            'id_ingrediente': int(dic_ingredientes[cmb_ingredientes]),
            'nombre_ingrediente': str(cmb_ingredientes),
            'unidad_ingrediente': str(txt_unidad),
            'cantidad_ingrediente': float(nmb_cantidad),
            'subtotal_ingrediente': float(subtotal)
        }   
    if st.button('Guardar Datos'):
        # Actualizar toda la fila con update()
        st.session_state.seleccion_ingredientes.loc[indice_auxiliar[0], diccionario_editar.keys()] = diccionario_editar.values()
        st.rerun()
        
        
@st.dialog("Buscar Ingredientes")
def seleccionar_ingredientes(lista_ingredientes):
    dic_ingredientes = {row['nombre_ingrediente']: row['id_ingrediente'] for row in lista_ingredientes}
    cmb_ingredientes = st.selectbox('Seleccionar Ingredientes', dic_ingredientes.keys())
    lista_ingredientes = consultar_ingredientes_por_id(dic_ingredientes[cmb_ingredientes])
    txt_unidad = st.text_input('Unidad: ',value=lista_ingredientes[0]['unidad_ingrediente'], disabled=True)
    label_precio = f"Precio por {lista_ingredientes[0]['unidad_ingrediente']}:"
    valor = f"${lista_ingredientes[0]['precio_unitario_ingrediente']:,.2f}"
    txt_precio = st.text_input(label_precio,value=valor, disabled=True)
    nmb_cantidad = st.number_input(f"Ingresar cantidad en {lista_ingredientes[0]['unidad_ingrediente']}:",format='%2.f',step=0.25)
    subtotal = lista_ingredientes[0]['precio_unitario_ingrediente'] * nmb_cantidad
    st.info(f'El subtotal es __${subtotal:,.2f}__')
    
    diccionario_agregar = {
            'id_ingrediente': int(dic_ingredientes[cmb_ingredientes]),
            'nombre_ingrediente': str(cmb_ingredientes),
            'unidad_ingrediente': str(txt_unidad),
            'cantidad_ingrediente': float(nmb_cantidad),
            'subtotal_ingrediente': float(subtotal)
        }
    
    st.write(len(st.session_state.seleccion_ingredientes))
    if st.button('Guardar Ingrediente'):
        st.session_state['seleccion_ingredientes'].loc[len(st.session_state['seleccion_ingredientes'])] = diccionario_agregar
        st.rerun()

def load_lottieurl(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

@st.dialog('Confirmar Cambios')
def guardar_cambios(txt_nombre_receta,box_seleccionar_clasificacion,nmb_rendimiento,raciones):
    
    
    lista_confirmar = [txt_nombre_receta, box_seleccionar_clasificacion,nmb_rendimiento, raciones]
    
    hay_cadena_vacia = any(isinstance(x, str) and not x for x in lista_confirmar)
    
    hay_numero_cero = any(isinstance(x, (int, float)) and x == 0 for x in lista_confirmar)
    
    if hay_cadena_vacia or hay_numero_cero:
        
        lottie_url = "https://lottie.host/064898bb-9b0f-45bb-983c-5aa7bd8ff9ae/iBIdLAqoFK.json"
        
        st.markdown(f'<p style="color:white; background-color:#FF4B4B;padding-top: 0.5em; border-radius:10px; font-size:20px;text-align:center;border-bottom: 2px solid #262730;padding-bottom:0.5em;"> Falta Completar Datos</p>', unsafe_allow_html=True)
        
        
        lottie_animation = load_lottieurl(lottie_url)
        st_lottie(lottie_animation, speed=1, loop=True, height=250, key="No")
        
    else:
        # URL de una animación Lottie
        lottie_url = "https://lottie.host/e09a77ad-94fd-49ab-9f01-d5ce090c84ae/WX8RFeS54T.json"
        lottie_animation = load_lottieurl(lottie_url)
        
        st.write(f'## ¿Seguro que quiere guardar la receta __{txt_nombre_receta}__?')
        # Mostrar la animación Lottie
        st_lottie(lottie_animation, speed=1, loop=True, height=250, key="example")
        
        if st.button('Confirmar Cambios'):
            recetas.insertar_receta(txt_nombre_receta,box_seleccionar_clasificacion,nmb_rendimiento,raciones)
            
            #Obtenemos el ultimo ID guardado
            ultimo_id_receta = recetas.consultar_ultima_receta()[0][0]
            for row in st.session_state.seleccion_ingredientes.itertuples():
                detalle_recetas_ingredientes.insertar_detalle_receta_ingrediente(
                    (row.id_ingrediente), int(ultimo_id_receta), float(row.cantidad_ingrediente))
            
            if 'seleccion_subelaboraciones' in st.session_state:
                for row in st.session_state.seleccion_subelaboraciones.itertuples():
                    detalle_receta_subelaboracion.insertar_detalle_receta_subelaboracion(int(ultimo_id_receta),int(row.id_subelaboracion), float(row.peso_subelaboracion))
                
            st.success('Datos Ingresados Correctamente 😎')
            
            reininiciar_seleccion()
            reiniciar_subelaboracion()
            
            time.sleep(1)
            st.rerun()
            

def agregar_receta():
    st.subheader('Agregar Receta')
    _col_componentes, _col_tabla_ingredientes = st.columns([3,4])
    
    with _col_componentes:
        _container_componentes = st.container(border=True, height = 550)
        with _container_componentes:
            txt_nombre_receta = st.text_input('Nombre de la receta: ', key='nombre_receta')
            lista_clasificacion_receta = ['Entrada', 'Desayuno', 'Plato Principal', 'Postre', 'Subelaboración']
            box_seleccionar_clasificacion = st.selectbox('Clasificacion', options=lista_clasificacion_receta)
            
            _col_peso, _col_peso_racion = st.columns([3,2])
            with _col_peso:
                nmb_rendimiento = st.number_input(f"Rendimiento en Kg:",format='%2.f',step=0.25, key='rendimiento_peso')
            
            with _col_peso_racion:
                peso_por_racion = st.number_input(f"Peso por racion:",format='%2.f',step=0.25, key='peso_porcion')
            
            
            raciones = round(float(nmb_rendimiento)/peso_por_racion,3) if peso_por_racion > 0 else 0
            _col_raciones, _col_total = st.columns(2)
            with _col_raciones:
                with st.container(border=True):
                    st.markdown(f'<p style="color:white; font-size:15px;text-align:center;border-bottom: 2px solid #262730;padding-bottom:0.5em;">Porciones</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style="color:yellow; font-size:20px;text-align:center;">{raciones}</p>', unsafe_allow_html=True)
            with _col_total:
                
                if 'seleccion_subelaboraciones' in st.session_state:
                    total = sum(st.session_state.seleccion_ingredientes['subtotal_ingrediente']) + sum(st.session_state.seleccion_subelaboraciones['valor_subelaboracion'])
                else:
                    total = round(sum(st.session_state.seleccion_ingredientes['subtotal_ingrediente']),2)
                
                with st.container(border=True):
                    st.markdown(f'<p style="color:white; font-size:15px;text-align:center;border-bottom: 2px solid #262730;padding-bottom:0.5em;"> Valor Total</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style="color:green; font-size:20px;text-align:center;">$ {total}</p>', unsafe_allow_html=True)
            
            _col_costo_kg, _col_costo_racion = st.columns(2)
            with _col_costo_kg:
                
                if total > 0 and nmb_rendimiento > 0:
                    costo_por_kg = round(total/nmb_rendimiento,1)
                else:
                    costo_por_kg = 0
                    
                with st.container(border=True):
                    st.markdown(f'<p style="color:white; font-size:15px;text-align:center;border-bottom: 2px solid #262730;padding-bottom:0.5em;">Valor por Kg</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style="color:#26C6DA; font-size:20px;text-align:center;">$ {costo_por_kg}</p>', unsafe_allow_html=True)
            with _col_costo_racion:
                
                if total>0 and raciones > 0:
                    costo_por_racion = round(total/raciones,1)
                else: costo_por_racion = 0
                
                with st.container(border=True):
                    st.markdown(f'<p style="color:white; font-size:15px;text-align:center;border-bottom: 2px solid #262730;padding-bottom:0.5em;">Valor por Racion</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style="color:#FF9999; font-size:20px;text-align:center;">$ {costo_por_racion}</p>', unsafe_allow_html=True)
                
            
    with _col_tabla_ingredientes:
        _container_ingredientes = st.container(border=True, height=550)
        
        with _container_ingredientes:
            tab_ingredientes, tab_subelaboracion = st.tabs(['Agregar Ingredientes', 'Agregar Subelaboraciones'])
            
            with tab_ingredientes:
                seleccion = st.dataframe(st.session_state.seleccion_ingredientes,
                                         hide_index=True,
                                         selection_mode='single-row',
                                         on_select='rerun',
                                         use_container_width=True,
                                         height=390,
                                         column_order=['nombre_ingrediente', 'unidad_ingrediente','cantidad_ingrediente', 'subtotal_ingrediente'])
                
                lista_ingredientes = ingredientes.consultar_ingredientes()
        
                if seleccion['selection']['rows']:
                    _col_relleno, _col_eliminar, _col_editar = st.columns([6,2,2])
                    with _col_eliminar:
                        if st.button(label='Ingrediente', icon = ':material/delete:', use_container_width=True):
                            eliminar_ingrediente_temporal(seleccion)
                    with _col_editar:
                        if st.button(label='Ingrediente', icon = ':material/edit:', use_container_width=True):
                            editar_ingrediente_temporal(seleccion, lista_ingredientes)
                else:
                    _col_relleno, _col_guardar_receta,_col_agregar_ingrediente = st.columns([5,1.5,1.5])
    
                    with _col_guardar_receta:
                        if st.button('Guardar Receta', use_container_width=True, type='primary'):
                            guardar_cambios(str(txt_nombre_receta), str(box_seleccionar_clasificacion), float(nmb_rendimiento), int(raciones))
                            
                    
                    with _col_agregar_ingrediente:
                        if st.button('__+__ Ingredientes', use_container_width=True):
                            seleccionar_ingredientes(lista_ingredientes)
            with tab_subelaboracion:
                visualizar_subelaboraciones()
                        

def mostrar_recetas():
    df_recetas = pd.DataFrame(recetas.consultar_recetas())
    filtro_recetas = st.dataframe(df_recetas,
                                  use_container_width=True,
                                  selection_mode='single-row',
                                  on_select='rerun',)
                                      

def main_recetas():
    iniciar_seleccion()
    _container_formulario_receta = st.container(border=True)
    with _container_formulario_receta:
        agregar_receta()
    
    _container_tabla_receta = st.container(border=True)
    with _container_tabla_receta:
        mostrar_recetas()