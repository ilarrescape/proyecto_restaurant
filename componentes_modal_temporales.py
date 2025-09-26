#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 20:41:26 2024

@author: mauricio
"""
import streamlit as st

import time

import ingredientes
import recetas

import detalle_recetas_ingredientes
import detalle_receta_subelaboracion

# from streamlit_lottie import st_lottie
import requests

def load_lottieurl(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()


def iniciar_copia_buscados(nombre_buscado):
    if 'nombre_buscado' not in st.session_state:
        st.session_state['nombre_buscado'] = nombre_buscado

@st.dialog("Eliminar Ingrediente")
def eliminar_ingrediente_temporal(seleccion, nombre_buscado, id_receta):
    
    indice_auxiliar = seleccion['selection']['rows']
    
    
    df_a_eliminar = st.session_state.seleccion_ingredientes_buscados.loc[indice_auxiliar]

    id_ingrediente = int(df_a_eliminar.iloc[0]['id_ingrediente'])
    
    nombre_ingrediente = df_a_eliminar.iloc[0]["nombre_ingrediente"]
    
    st.warning(f'¿Seguro que quiere eliminar el ingrediente __{nombre_ingrediente}__?')
    
    if st.button('Eliminar'):
        st.session_state.seleccion_ingredientes_buscados.drop(indice_auxiliar, axis=0, inplace = True)
        st.session_state.seleccion_ingredientes_buscados.reset_index(drop = True, inplace = True)
        detalle_recetas_ingredientes.eliminar_detalle_receta_ingrediente(id_ingrediente, id_receta)
        iniciar_copia_buscados(nombre_buscado)
        st.rerun()
    

def guardar_id_receta(id_receta):
    if 'id_receta_buscada' not in st.session_state:
        st.session_state['id_buscado'] = id_receta
    else:
        st.session_state.id_buscado = id_receta


@st.dialog("Aregar nuevo Ingrediente")
def agregar_ingrediente_temporal(lista_ingredientes, nombre_buscado, id_receta):
    dic_ingredientes = {row['nombre_ingrediente']: row['id_ingrediente'] for row in lista_ingredientes}
    cmb_ingredientes = st.selectbox('Seleccionar Ingredientes', dic_ingredientes.keys())
    lista_ingredientes = ingredientes.consultar_ingredientes_por_id(dic_ingredientes[cmb_ingredientes])
    txt_unidad = st.text_input('Unidad: ',value=lista_ingredientes[0]['unidad_ingrediente'], disabled=True)
    label_precio = f"Precio por {lista_ingredientes[0]['unidad_ingrediente']}:"
    valor = f"${lista_ingredientes[0]['precio_unitario_ingrediente']:,.2f}"
    txt_precio = st.text_input(label_precio,value=valor, disabled=True)
    nmb_cantidad = st.number_input(f"Ingresar cantidad en {lista_ingredientes[0]['unidad_ingrediente']}:",format='%2.f',step=0.25)
    subtotal = lista_ingredientes[0]['precio_unitario_ingrediente'] * nmb_cantidad
    st.info(f'El subtotal es __${subtotal:,.2f}__')
    


    if st.button('Guardar Ingrediente'):
        
        detalle_recetas_ingredientes.insertar_detalle_receta_ingrediente(int(dic_ingredientes[cmb_ingredientes]), id_receta, float(nmb_cantidad))
        
        id_nuevo_detalle = detalle_recetas_ingredientes.recuperar_ultimo_detalle()
        
        diccionario_agregar = {
                'id_detalle': id_nuevo_detalle,
                'id_ingrediente': int(dic_ingredientes[cmb_ingredientes]),
                'nombre_ingrediente': str(cmb_ingredientes),
                'unidad_ingrediente': str(txt_unidad),
                'precio_unitario_ingrediente': float(lista_ingredientes[0]['precio_unitario_ingrediente']),
                'cantidad_detalle': float(nmb_cantidad),
                'subtotal_ingrediente': float(subtotal)
            }
        
        st.session_state['seleccion_ingredientes_buscados'].loc[len(st.session_state['seleccion_ingredientes_buscados'])] = diccionario_agregar
        iniciar_copia_buscados(nombre_buscado)
        guardar_id_receta(id_receta)
        st.rerun()



@st.dialog("Editar Ingrediente")
def editar_ingrediente_temporal(seleccion,lista_ingredientes, nombre_buscado, id_receta):  
    
    # Generamos la serie
    indice_auxiliar = seleccion['selection']['rows']
    serie_df = st.session_state.seleccion_ingredientes_buscados.iloc[indice_auxiliar[0]]
    
    # Generamos el diccionario de ingredientes y extraemos los nombres para guardarlos en una lista
    dic_ingredientes = {row['nombre_ingrediente']: row['id_ingrediente'] for row in lista_ingredientes}
    lista_nombre_ingredientes = list(dic_ingredientes.keys())
    
    # Mostramos en el selectbox el nombre del ingrediente que se filtro
    cmb_ingredientes = st.selectbox('Seleccionar Ingredientes', lista_nombre_ingredientes, index= lista_nombre_ingredientes.index(serie_df['nombre_ingrediente']))
    lista_ingredientes = ingredientes.consultar_ingredientes_por_id(dic_ingredientes[cmb_ingredientes])
    txt_unidad = st.text_input('Unidad: ',value=lista_ingredientes[0]['unidad_ingrediente'], disabled=True)
    label_precio = f"Precio por {lista_ingredientes[0]['unidad_ingrediente']}:"
    valor = f"${lista_ingredientes[0]['precio_unitario_ingrediente']:,.2f}"
    txt_precio = st.text_input(label_precio,value=valor, disabled=True)
    nmb_cantidad = st.number_input(f"Ingresar cantidad en {lista_ingredientes[0]['unidad_ingrediente']}:",format='%2.f',step=0.25, value= serie_df['cantidad_detalle'])
    subtotal = lista_ingredientes[0]['precio_unitario_ingrediente'] * nmb_cantidad
    st.info(f'El subtotal es __${subtotal:,.2f}__')
    
    indice_auxiliar = seleccion['selection']['rows']
    df_a_modificar = st.session_state.seleccion_ingredientes_buscados.loc[indice_auxiliar]
    id_detalle = int(df_a_modificar.iloc[0]['id_detalle'])
    
    #Agregamos los nuevos datos al diccionario
    diccionario_editar = {
            'id_detalle': id_detalle,
            'id_ingrediente': int(dic_ingredientes[cmb_ingredientes]),
            'nombre_ingrediente': str(cmb_ingredientes),
            'unidad_ingrediente': str(txt_unidad),
            'precio_unitario_ingrediente': float(lista_ingredientes[0]['precio_unitario_ingrediente']),
            'cantidad_detalle': float(nmb_cantidad),
            'subtotal_ingrediente': float(subtotal)
        }   
    if st.button('Guardar Datos'):
        # Actualizar toda la fila con update()
        st.session_state.seleccion_ingredientes_buscados.loc[indice_auxiliar[0], diccionario_editar.keys()] = diccionario_editar.values()
        iniciar_copia_buscados(nombre_buscado)
        guardar_id_receta(id_receta)
        detalle_recetas_ingredientes.modificar_detalle_receta_ingrediente(id_detalle, int(dic_ingredientes[cmb_ingredientes]), int(id_receta), float(nmb_cantidad))
        st.rerun()


@st.dialog("Eliminar Subelaboracion")
def eliminar_subelaboracion_temporal(seleccion, nombre_buscado, id_receta):
    
    indice_auxiliar = seleccion['selection']['rows']
    
    df_a_eliminar = st.session_state.seleccion_subelaboraciones_buscadas.loc[indice_auxiliar]

    id_subelaboracion_buscada = int(df_a_eliminar.iloc[0]['id_subelaboracion'])
    
    nombre_subelaboracion_buscada = df_a_eliminar.iloc[0]["nombre_subelaboracion"]
    
    st.warning(f'¿Seguro que quiere eliminar la subelaboracion __{nombre_subelaboracion_buscada}__?')
    
    if st.button('Eliminar'):
        st.session_state.seleccion_subelaboraciones_buscadas.drop(indice_auxiliar, axis=0, inplace = True)
        st.session_state.seleccion_subelaboraciones_buscadas.reset_index(drop = True, inplace = True)
        detalle_receta_subelaboracion.eliminar_detalle_receta_subelaboracion(id_receta, id_subelaboracion_buscada)
        iniciar_copia_buscados(nombre_buscado)
        st.rerun()
    
@st.dialog('Agregar Subelaboracion')
def agregar_subelaboracion(id_receta):
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
    
    if st.button('Guardar Subelaboracion'):
        detalle_receta_subelaboracion.insertar_detalle_receta_subelaboracion(id_receta, dic_subelaboracion[select_subelaboracion], round(cantidad_detalle,3))
        
        diccionario_guardar_subelaboracion = {
                'id_subelaboracion' : diccionario_subelaboracion['id_receta'],
                'nombre_subelaboracion' : diccionario_subelaboracion['nombre_receta'],
                'peso_subelaboracion' : round(cantidad_detalle,3),
                'cantidad_raciones_subelaboracion': rendimiento_detalle,
                'valor_subelaboracion': round(valor_por_seleccion,2)
            }
        
        st.session_state.seleccion_subelaboraciones.loc[len(st.session_state['seleccion_subelaboraciones'])] = diccionario_guardar_subelaboracion
        
        st.rerun()


@st.dialog('Editar Subelaboracion')
def editar_subelaboracion(seleccion,lista_subelaboracion, id_receta):
    
    indice_auxiliar = seleccion['selection']['rows']
    
    serie_df_subelaboracion = st.session_state.seleccion_subelaboraciones_buscadas.iloc[indice_auxiliar[0]]
    
    
    
    lista_todas_subelaboraciones = recetas.consultar_subelaboracion()
    
    dic_subelaboracion = {row['nombre_receta']:row['id_receta'] for row in lista_todas_subelaboraciones}

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
    
    
    diccionario_subelaboracion = [fila for fila in lista_todas_subelaboraciones  if fila['nombre_receta'] == select_subelaboracion][0]
    
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
        st.session_state.seleccion_subelaboraciones_buscadas.loc[indice_auxiliar[0], diccionario_guardar_subelaboracion.keys()] = diccionario_guardar_subelaboracion.values()
        detalle_receta_subelaboracion.modificar_detalle_receta_subelaboracion(int(id_receta), int(serie_df_subelaboracion.loc['id_subelaboracion']), int(diccionario_subelaboracion['id_receta']), round(cantidad_detalle,3))
        st.rerun()
    
@st.dialog('Guardar Cambios')
def guardar_cambios_receta(id_receta, nuevo_nombre, nueva_clasificacion, nuevo_rendimiento_por_kg, nuevo_rendimiento_raciones):
    
    st.write('## ¿Seguro que quiere guardar los cambios?')
    lottie_url = "https://lottie.host/e450e7e3-e884-41d3-bd23-7d1ca8b7c121/NXA5EbUILJ.json"
                  
    lottie_animation = load_lottieurl(lottie_url)
    st_lottie(lottie_animation, speed=1, loop=True, height=250, key="No")
    if st.button('Confirmar'):
        recetas.modificar_receta(id_receta, nuevo_nombre, nueva_clasificacion, nuevo_rendimiento_por_kg, nuevo_rendimiento_raciones)
        st.success('Cambios guardados exitosamente.')
        time.sleep(1)
        st.rerun()


@st.dialog('Eliminar Receta')
def eliminar_receta(id_receta):
    st.write('## ¿Seguro que quiere eliminar la receta?')

    lottie_url = "https://lottie.host/e450e7e3-e884-41d3-bd23-7d1ca8b7c121/NXA5EbUILJ.json"
                  
    lottie_animation = load_lottieurl(lottie_url)
    st_lottie(lottie_animation, speed=1, loop=True, height=250, key="No")
    if st.button('Confirmar'):
        detalle_recetas_ingredientes.eliminar_detalle_receta_ingrediente_por_receta(id_receta)
        detalle_receta_subelaboracion.eliminar_detalle_receta_subelaboracion_por_receta(id_receta)
        recetas.eliminar_receta(id_receta)
        st.success('Cambios guardados exitosamente.')
        time.sleep(1)
        st.rerun()