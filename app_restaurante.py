#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 05:07:35 2024

@author: mauricio
"""

import streamlit as st
import componentes_ingredientes
import componentes_recetas
import componentes_buscar_recetas
import graficos

import time

st.set_page_config(layout='wide', page_icon=":male_cook:")

def crear_session_state(usuario, Contraseña):
    if 'user_session' not in st.session_state:
        st.session_state['user_session'] = usuario
    if 'pass_session' not in st.session_state:
        st.session_state['pass_session'] = Contraseña

def verificar_login(usuario, contraseña):
    if usuario == 'chef_loquillo' and contraseña == 'tiramisu980':
        return True
    else:
        st.error('Datos Mal Ingresados')
        del st.session_state['user_session']
        del st.session_state['pass_session']
        time.sleep(2)
        return False
def login():
    if 'user_session' in st.session_state and 'pass_session' in st.session_state:
        if verificar_login(st.session_state['user_session'],st.session_state['pass_session']):
            visualizar_elementos()
        else:
            st.rerun()
    else:
        _col_relleno1, _col_container, _col_relleno2 = st.columns(3)
        with _col_container:
            with st.container(border=True):
                st.image('chef.jpg')
                usuario = st.text_input('Ingresar Nombre de Usuario: ')
                contraseña = st.text_input('Ingresar Contraseña: ', type='password')
                if st.button('Iniciar Sesion'):
                    crear_session_state(usuario, contraseña)
                    st.rerun()
                    
def visualizar_elementos():

    st.write('## Bienvenido a la Aplicacion de Recetas')
    
    tab_nuevos_ingredientes, tab_nueva_receta, tab_buscar_receta, tab_graficos = st.tabs(['Agregar Ingredientes', 'Nueva Receta', 'Buscar Receta', 'Ver Reporte'])
    
    with tab_nuevos_ingredientes:
        componentes_ingredientes.main_ingredientes()
    
    with tab_nueva_receta:
        componentes_recetas.main_recetas()
    
    with tab_buscar_receta:
        componentes_buscar_recetas.main_buscar_recetas()
    
    with tab_graficos:
       graficos.main_graficos()

login()