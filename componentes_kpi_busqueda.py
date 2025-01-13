#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import streamlit as st

"""
Created on Sat Dec 28 20:37:35 2024

@author: mauricio
"""
def fun_mostrar_kpi(peso_total, peso_racion,df_ingredientes_buscados, df_subelaboraciones_buscadas):
    _col_raciones, _col_total  = st.columns(2)
    
    with _col_raciones:
        raciones = round(peso_total/peso_racion,3)  
        with st.container(border=True):
            st.markdown(f'<p style="color:white; font-size:15px;text-align:center;border-bottom: 2px solid #262730;padding-bottom:0.5em;">Porciones</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:yellow; font-size:20px;text-align:center;">{raciones}</p>', unsafe_allow_html=True)
    with _col_total:
        
        if 'seleccion_subelaboraciones_buscadas' in st.session_state:
            total = sum(df_ingredientes_buscados['subtotal_ingrediente']) + sum(df_subelaboraciones_buscadas['valor_subelaboracion'])
        else:
            total = round(sum(df_ingredientes_buscados['subtotal_ingrediente']),2)
        
        with st.container(border=True):
            st.markdown(f'<p style="color:white; font-size:15px;text-align:center;border-bottom: 2px solid #262730;padding-bottom:0.5em;"> Valor Total</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:green; font-size:20px;text-align:center;">$ {total}</p>', unsafe_allow_html=True)
    
    
    _col_costo_kg, _col_costo_racion = st.columns(2)
    
    with _col_costo_kg:
        
        if total > 0 and peso_total > 0:
            costo_por_kg = round(total/peso_total,1)
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
    return raciones