#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicación principal de Streamlit para la gestión de recetas.
"""

import time

import streamlit as st

import auth
import componentes_buscar_recetas
import componentes_ingredientes
import componentes_recetas
import graficos

st.set_page_config(layout='wide', page_icon=":male_cook:")

AUTH_SESSION_KEY = 'auth_user'


def _mostrar_logout(usuario: str) -> None:
    """Renderiza los controles de cierre de sesión en la barra lateral."""
    with st.sidebar:
        st.write(f"👤 Sesión iniciada como: **{usuario}**")
        if st.button('Cerrar sesión'):
            st.session_state.pop(AUTH_SESSION_KEY, None)
            st.rerun()


def login() -> None:
    """Controla el flujo de autenticación del usuario."""
    auth.initialize_user_table()

    if AUTH_SESSION_KEY in st.session_state:
        usuario = st.session_state[AUTH_SESSION_KEY]
        _mostrar_logout(usuario)
        visualizar_elementos(usuario)
        return

    if 'show_register' not in st.session_state:
        st.session_state['show_register'] = False

    _col_relleno1, _col_container, _col_relleno2 = st.columns(3)
    with _col_container:
        with st.container(border=True):
            st.image('chef.jpg')

            if not st.session_state['show_register']:
                with st.form('login_form'):
                    usuario = st.text_input('Ingresar Nombre de Usuario: ')
                    contraseña = st.text_input('Ingresar Contraseña: ', type='password')
                    iniciar = st.form_submit_button('Iniciar Sesión')

                if iniciar:
                    if auth.verify_user(usuario, contraseña):
                        st.session_state[AUTH_SESSION_KEY] = usuario
                        st.success('Autenticación exitosa. Redirigiendo...')
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error('Credenciales inválidas. Por favor, inténtalo de nuevo.')

                if st.button('Registrar nuevo usuario'):
                    st.session_state['show_register'] = True
                    st.rerun()
            else:
                st.subheader('Registrar nuevo usuario')
                with st.form('register_form'):
                    nuevo_usuario = st.text_input('Nuevo nombre de usuario: ')
                    nueva_contraseña = st.text_input('Nueva contraseña: ', type='password')
                    confirmar_contraseña = st.text_input('Confirmar contraseña: ', type='password')
                    registrar = st.form_submit_button('Crear usuario')

                if registrar:
                    if not nuevo_usuario or not nueva_contraseña:
                        st.error('Debes completar todos los campos para registrar un usuario.')
                    elif nueva_contraseña != confirmar_contraseña:
                        st.error('Las contraseñas no coinciden. Intenta nuevamente.')
                    else:
                        try:
                            auth.create_user(nuevo_usuario, nueva_contraseña)
                        except ValueError as exc:
                            st.error(str(exc))
                        except Exception:
                            st.error('Ocurrió un error inesperado al crear el usuario.')
                        else:
                            st.success('Usuario creado correctamente. Ahora puedes iniciar sesión.')
                            st.session_state['show_register'] = False
                            st.rerun()

                if st.button('Cancelar registro'):
                    st.session_state['show_register'] = False
                    st.rerun()


def visualizar_elementos(usuario: str) -> None:
    """Renderiza el contenido principal de la aplicación cuando el usuario está autenticado."""

    st.write('## Bienvenido a la Aplicacion de Recetas')
    st.info(f'Usuario autenticado: **{usuario}**')

    tab_nuevos_ingredientes, tab_nueva_receta, tab_buscar_receta, tab_graficos = st.tabs([
        'Agregar Ingredientes',
        'Nueva Receta',
        'Buscar Receta',
        'Ver Reporte',
    ])

    with tab_nuevos_ingredientes:
        componentes_ingredientes.main_ingredientes()

    with tab_nueva_receta:
        componentes_recetas.main_recetas()

    with tab_buscar_receta:
        componentes_buscar_recetas.main_buscar_recetas()

    with tab_graficos:
        graficos.main_graficos()


login()
