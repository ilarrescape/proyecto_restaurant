#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 14:30:42 2024

@author: mauricio
"""
import recetas
import ingredientes
from ingredientes import consultar_ingredientes_por_id
from componentes_subelaboraciones import visualizar_subelaboraciones


import detalle_recetas_ingredientes
import detalle_receta_subelaboracion
import componentes_kpi_busqueda
import componentes_tab_buscar_recetas
import componentes_modal_temporales

import streamlit as st
import pandas as pd


import time

from streamlit_lottie import st_lottie
import requests


def iniciar_seleccion_filtros():
    if 'seleccion_ingredientes_buscados' not in st.session_state:
        st.session_state['seleccion_ingredientes_buscados'] = pd.DataFrame(columns = ['id_detalle','id_ingrediente', 'nombre_ingrediente', 'cantidad_detalle', 'unidad_ingrediente', 'precio_unitario_ingrediente', 'subtotal_ingrediente'])
    
    if 'seleccion_subelaboraciones_buscadas' not in st.session_state:
        st.session_state['seleccion_subelaboraciones_buscadas'] = pd.DataFrame(columns = ['id_subelaboracion', 'nombre_receta', 'peso_subelaboracion','rendimiento_raciones','rendimiento_por_kg_receta','cantidad_raciones_subelaboracion','valor_subelaboracion'])

def filtros_recetas():
    lista_recetas = recetas.consultar_recetas()
    dic_recetas = {row['nombre_receta']:row['id_receta'] for row in lista_recetas}
    
    lista_seleccion_recetas = list(dic_recetas.keys())
    lista_seleccion_recetas.insert(0, 'Seleccionar una Receta...')    
    select_recetas = st.selectbox('Seleccionar Receta:', lista_seleccion_recetas, index=0)
    
    return select_recetas, dic_recetas

def mostrar_registros():
    
    
    lista_recetas = recetas.consultar_recetas()
    df_recetas = pd.DataFrame(lista_recetas)
    
    st.header('Buscar recetas')
    
    col_formulario,col_detalles = st.columns([2,3])
    
    
    with col_formulario:
        
        with st.container(border=True, height = 620):
            select_recetas, dic_recetas = filtros_recetas()
            
            if select_recetas != 'Seleccionar una Receta...':
                
                df_recetas = df_recetas[df_recetas['nombre_receta'] == select_recetas].reset_index(drop = True)
                
                iniciar_seleccion_filtros()
                
                #--------------------------------
                #----------Ingredientes----------
                #--------------------------------
                
                #Mostramos los ingredientes buscados antes de cargar los ingredientes relacionados a la receta
                
                #consultamos todos los detalles de ingredientes
                lista_detalle_ingredientes = detalle_recetas_ingredientes.consultar_detalles_receta_ingrediente()
                lista_ingredientes = ingredientes.consultar_ingredientes()
                
                
                
                #Convertimos a DataFrame                    
                df_detalle_ingrediente = pd.DataFrame(lista_detalle_ingredientes)
                df_ingredientes = pd.DataFrame(lista_ingredientes)
                
                
                #Filtramos los DataFrames que coincidan
                df_detalle_ingrediente = df_detalle_ingrediente[df_detalle_ingrediente['receta_detalle'].isin(df_recetas['id_receta'])]
                df_ingredientes = df_ingredientes[df_ingredientes['id_ingrediente'].isin(df_detalle_ingrediente['ingrediente_detalle'])]
                
                
                if not df_detalle_ingrediente.empty:
                
                    if 'id_buscado' not in st.session_state or st.session_state['id_buscado'] != int(dic_recetas[select_recetas]):
                        
                        
                        st.session_state.seleccion_ingredientes_buscados = pd.merge(df_detalle_ingrediente, df_ingredientes, left_on='ingrediente_detalle', right_on='id_ingrediente',how='inner')[['id_detalle','id_ingrediente', 'nombre_ingrediente', 'cantidad_detalle', 'unidad_ingrediente', 'precio_unitario_ingrediente']]
                        
                        st.session_state.seleccion_ingredientes_buscados['subtotal_ingrediente'] = st.session_state.seleccion_ingredientes_buscados['cantidad_detalle'] * st.session_state.seleccion_ingredientes_buscados['precio_unitario_ingrediente']
                
                else:
                    st.session_state['seleccion_ingredientes_buscados'] = pd.DataFrame(columns = ['id_detalle','id_ingrediente', 'nombre_ingrediente', 'cantidad_detalle', 'unidad_ingrediente', 'precio_unitario_ingrediente', 'subtotal_ingrediente'])
                
                #--------------------------------
                #--------Subelaboraciones--------
                #--------------------------------

                lista_subelaboraciones = detalle_receta_subelaboracion.consultar_detalles_receta_subelaboracion()
                df_detalle_subelaboracion =pd.DataFrame(lista_subelaboraciones)
                
                st.session_state.seleccion_subelaboraciones_buscadas = df_detalle_subelaboracion[df_detalle_subelaboracion['id_receta'].isin(df_recetas['id_receta'])] if len(lista_subelaboraciones)>0 else pd.DataFrame(columns = ['id_subelaboracion', 'nombre_receta', 'peso_subelaboracion','rendimiento_raciones','rendimiento_por_kg_receta','cantidad_raciones_subelaboracion','valor_subelaboracion'])
                
                lista_consulta_subelaboraciones  = recetas.consultar_subelaboracion()
                
                df_subelaboraciones = pd.DataFrame(lista_consulta_subelaboraciones)
                
                if len(lista_subelaboraciones)>0:
                    st.session_state.seleccion_subelaboraciones_buscadas = pd.merge(st.session_state.seleccion_subelaboraciones_buscadas, df_subelaboraciones, left_on='id_subelaboracion', right_on='id_receta',how='inner')[['id_subelaboracion', 'nombre_receta', 'peso_subelaboracion','rendimiento_raciones','rendimiento_por_kg_receta']]
                
                st.session_state.seleccion_subelaboraciones_buscadas['valor_subelaboracion'] = None
                
                for i in range(len(st.session_state.seleccion_subelaboraciones_buscadas)):
                    lista_subelaboraciones_filtradas = recetas.consultar_ingredientes_subelaboracion(int(st.session_state.seleccion_subelaboraciones_buscadas.loc[i,'id_subelaboracion']))
                    
                    if len(lista_subelaboraciones_filtradas)>0:
                        
                        df_subelaboraciones_filtradas = pd.DataFrame(lista_subelaboraciones_filtradas)

                        st.session_state.seleccion_subelaboraciones_buscadas.loc[i,'valor_subelaboracion'] = sum(df_subelaboraciones_filtradas['subtotal']) 
                    else:
                        st.session_state.seleccion_subelaboraciones_buscadas.loc[i,'valor_subelaboracion'] = 0
                
                #-------------------------------------

                col_nombre_receta,col_clasificacion_receta= st.columns([4,3])
                
                with col_nombre_receta:
                    txt_nombre_receta = st.text_input('Nombre Receta:', value = df_recetas.loc[0, 'nombre_receta'])
                
                with col_clasificacion_receta:
                    lista_tipo_receta = ['Entrada', 'Desayuno', 'Plato Principal', 'Postre', 'Subelaboración']
                    
                    select_clasificacion_receta = st.selectbox('Clasificacion Receta:',options=lista_tipo_receta, index=lista_tipo_receta.index(df_recetas.loc[0, 'clasificación_receta']))
                    
                col_rend_kil, col_peso_racion = st.columns(2)
                
                rendimiento_en_kg = float(df_recetas.loc[0,'rendimiento_por_kg_receta'])
                
                with col_rend_kil:
                    number_rendimiento_en_kilos = st.number_input('Rendimiento en kg:', value = rendimiento_en_kg,format='%2.f',step=0.25)
                
                with col_peso_racion:
                    
                    peso_por_racion = round(float(rendimiento_en_kg / float(df_recetas.loc[0,'rendimiento_raciones'])),2)
                    
                    number_peso_racion = st.number_input('Peso por Racion:', value = peso_por_racion,format='%2.f',step=0.25)
                
                cantidad_raciones = componentes_kpi_busqueda.fun_mostrar_kpi(float(number_rendimiento_en_kilos), float(number_peso_racion), st.session_state.seleccion_ingredientes_buscados,st.session_state.seleccion_subelaboraciones_buscadas)
                col_relleno_botones,col_editar_receta, col_eliminar_receta = st.columns([4,2,2])
                with col_editar_receta:
                    if st.button(label = 'Receta', icon=':material/save:', use_container_width = True, key = 'guardar_cambios_receta'):

                        componentes_modal_temporales.guardar_cambios_receta(int(dic_recetas[select_recetas]), nuevo_nombre=str(txt_nombre_receta),nueva_clasificacion=str(select_clasificacion_receta),nuevo_rendimiento_por_kg = float(number_rendimiento_en_kilos), nuevo_rendimiento_raciones=float(cantidad_raciones))
                with col_eliminar_receta:
                    if st.button(label= 'Receta',icon = ':material/delete:', use_container_width = True, key = 'eliminar_receta'):
                        componentes_modal_temporales.eliminar_receta(int(dic_recetas[select_recetas]))
                
    with col_detalles:
        with st.container(border= True, height = 620):
            
            if select_recetas != 'Seleccionar una Receta...':
                lista_ingredientes = ingredientes.consultar_ingredientes()

                st.session_state['receta_detalle_actual'] = dic_recetas[select_recetas]
                    
                componentes_tab_buscar_recetas.fun_tabs(str(select_recetas), lista_ingredientes, lista_subelaboraciones, int(st.session_state['receta_detalle_actual']))
            
            else: st.warning('No hay recetas seleccionadas')
def main_buscar_recetas():
    
    mostrar_registros()