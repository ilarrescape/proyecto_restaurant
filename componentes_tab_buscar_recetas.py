#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 19:37:57 2024

@author: mauricio
"""

import streamlit as st
import componentes_modal_temporales

def fun_tabs(nombre_buscado, lista_ingredientes, lista_subelaboraciones, id_receta):
    
    tab_ingredientes, tab_subelaboraciones = st.tabs(['Modificar Ingredientes', 'Modificar Subelaboraciones'])
    
    with tab_ingredientes:
        df_seleccion_ingredientes = st.dataframe(st.session_state.seleccion_ingredientes_buscados,
                                                 height=450,
                                                 hide_index=True,
                                                 selection_mode='single-row',
                                                 on_select='rerun',
                                                 use_container_width=True,
                                                 column_order=['nombre_ingrediente', 'cantidad_detalle', 'unidad_ingrediente', 'precio_unitario_ingrediente', 'subtotal_ingrediente'])
        
        if df_seleccion_ingredientes['selection']['rows']:
            _col_relleno_ingredientes, _col_eliminar_ingredientes, _col_editar_ingredientes = st.columns([6,2,2])
            with _col_eliminar_ingredientes:
                if st.button(label='Ingrediente', icon = ':material/delete:', use_container_width=True, key='eliminar_ingrediente_buscado'):
                    componentes_modal_temporales.eliminar_ingrediente_temporal(df_seleccion_ingredientes, nombre_buscado, id_receta)
            
            with _col_editar_ingredientes:
                if st.button(label='Ingrediente', icon = ':material/edit:', use_container_width=True, key='editar_ingrediente_buscado'):
                    componentes_modal_temporales.editar_ingrediente_temporal(df_seleccion_ingredientes, lista_ingredientes, nombre_buscado, id_receta)
        else:
            _col_relleno_ingredientes, _col_guardar_receta, _col_agregar_ingredientes = st.columns([6,2,2])
            with _col_agregar_ingredientes:
                if st.button(label='Ingrediente', icon=':material/add:', use_container_width=True, key='agregar_ingrediente_buscado'):
                    componentes_modal_temporales.agregar_ingrediente_temporal(lista_ingredientes, nombre_buscado, id_receta)
        
    
    with tab_subelaboraciones:
        st.session_state.seleccion_subelaboraciones_buscadas.rename(columns={'nombre_receta':'nombre_subelaboracion'},inplace = True)
        st.session_state.seleccion_subelaboraciones_buscadas['cantidad_raciones_subelaboracion'] = st.session_state.seleccion_subelaboraciones_buscadas['peso_subelaboracion'] / round(st.session_state.seleccion_subelaboraciones_buscadas['rendimiento_por_kg_receta']/st.session_state.seleccion_subelaboraciones_buscadas['rendimiento_raciones'],3)
        
        columnas = ['id_subelaboracion', 
                    'nombre_subelaboracion', 
                    'peso_subelaboracion',
                    'rendimiento_raciones',
                    'rendimiento_por_kg_receta',
                    'cantidad_raciones_subelaboracion',
                    'valor_subelaboracion']
        
        
        st.session_state.seleccion_subelaboraciones_buscadas = st.session_state.seleccion_subelaboraciones_buscadas[columnas]
        df_seleccion_subelaboraciones = st.dataframe(st.session_state.seleccion_subelaboraciones_buscadas,
                                                         height=450,
                                                         hide_index=True,
                                                         selection_mode='single-row',
                                                         on_select='rerun',
                                                         use_container_width=True,
                                                         column_order=['nombre_subelaboracion','peso_subelaboracion', 'cantidad_raciones_subelaboracion','valor_subelaboracion'])
        if df_seleccion_subelaboraciones['selection']['rows']:
            _col_relleno_subelaboraciones, _col_eliminar_subelaboraciones, _col_editar_subelaboraciones = st.columns([6,2,2])
            
            with _col_eliminar_subelaboraciones:
                if st.button(label='Subelaboracion', icon = ':material/delete:', use_container_width=True, key='eliminar_subelaboracion_buscada'):
                    componentes_modal_temporales.eliminar_subelaboracion_temporal(df_seleccion_subelaboraciones, nombre_buscado, id_receta)
            
            with _col_editar_subelaboraciones:
                if st.button(label='Subelaboracion', icon = ':material/edit:', use_container_width=True, key='editar_subelaboracion_buscada'):
                    componentes_modal_temporales.editar_subelaboracion(df_seleccion_subelaboraciones, lista_subelaboraciones, id_receta)
        else:
            _col_relleno_subelaboraciones, _col_guardar_subelaboraciones, _col_agregar_subelaboraciones = st.columns([6,2,2])
            with _col_agregar_subelaboraciones:
                if st.button(label='Subelaboracion', icon=':material/add:', use_container_width=True, key='agregar_subelaboracion_buscada'):
                    componentes_modal_temporales.agregar_subelaboracion(id_receta)
        
                    

        