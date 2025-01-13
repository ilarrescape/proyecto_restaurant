#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 19:46:51 2025

@author: mauricio
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import ingredientes
import recetas
import detalle_recetas_ingredientes


def main_graficos():
    
    lista_ingredientes = ingredientes.consultar_ingredientes()
    df_ingredientes = pd.DataFrame(lista_ingredientes)

    lista_recetas = recetas.consultar_recetas()
    df_recetas = pd.DataFrame(lista_recetas)
    
    lista_detalle_receta_ingrediente = detalle_recetas_ingredientes.consultar_detalles_receta_ingrediente()
    df_detalle_receta_ingrediente = pd.DataFrame(lista_detalle_receta_ingrediente)
    
    # Relacionar detalle de recetas con ingredientes
    detalle_receta = df_detalle_receta_ingrediente.merge(
        df_ingredientes,
        left_on="ingrediente_detalle",
        right_on="id_ingrediente"
    )
    
    # Calcular costo total por ingrediente en cada receta
    detalle_receta["costo_ingrediente"] = (
        detalle_receta["cantidad_detalle"] * detalle_receta["precio_unitario_ingrediente"]
    )
    
    costo_por_receta = detalle_receta.groupby("receta_detalle")["costo_ingrediente"].sum().reset_index()
    costo_por_receta.columns = ["id_receta", "costo_total"]
    
    # Relacionar costos con recetas
    df_recetas = df_recetas.merge(costo_por_receta, on="id_receta")
    df_recetas["costo_por_ración"] = df_recetas["costo_total"] / df_recetas["rendimiento_raciones"]
    
    # Dashboard en Streamlit
    st.title("Reporte de Costos de Recetas")
    
    st.subheader("Filtros")
    col1, col2 = st.columns(2)
    
    with col1:
        selected_recetas = st.multiselect(
            "Seleccionar Recetas:",
            options= df_recetas["nombre_receta"].unique(),
            default= df_recetas["nombre_receta"].unique()
        )
    
    with col2:
        selected_categorias = st.multiselect(
            "Seleccionar Categorías:",
            options= df_recetas["clasificación_receta"].unique(),
            default= df_recetas["clasificación_receta"].unique()
        )
    
    # Aplicar filtros
    df_recetas = df_recetas[
        (df_recetas["nombre_receta"].isin(selected_recetas)) |
        (df_recetas["clasificación_receta"].isin(selected_categorias))
    ]

    
    _col_costo_racion, _col_mas_costosa, _col_ingrediente_mas_usado = st.columns([2,3,3])
    
    with _col_costo_racion:
        with st.container(border=True):
            # KPI: Costo promedio por racion
            costo_promedio = df_recetas["costo_por_ración"].mean()
            st.markdown(f'<p style="color:white; font-size:15px;text-align:center;border-bottom: 2px solid #262730;padding-bottom:0.5em;">Costo Promedio por Ración</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:yellow; font-size:35px;text-align:center;">$ {round(costo_promedio,2)}</p>', unsafe_allow_html=True)    

    with _col_mas_costosa:
            with st.container(border=True):        
                # KPI: Receta más costosa
                
                receta_max_costo = df_recetas.loc[df_recetas["costo_total"].idxmax()]
                costo_receta = receta_max_costo["costo_por_ración"]
                
                nombre_receta = receta_max_costo["nombre_receta"]
                
                # st.markdown(f'<p style="color:white; font-size:15px;text-align:center;border-bottom: 2px solid #262730;padding-bottom:0.5em;">Receta mas costosa ($ {costo_receta})</p>', unsafe_allow_html=True)
                st.markdown(f'''
                            <p style="color:white; font-size:15px; text-align:center; border-bottom: 2px solid #262730; padding-bottom:0.5em;">
                            Receta más Costosa por Porción <span style="color:green;">$ {costo_receta}</span>
                            </p>
                            ''', unsafe_allow_html=True)
                
                st.markdown(f'<p style="color:green; font-size:35px;text-align:center;"> {nombre_receta}</p>', unsafe_allow_html=True)

    
    with _col_ingrediente_mas_usado:
        with st.container(border=True):
            ingrediente_mas_utilizado = df_detalle_receta_ingrediente["ingrediente_detalle"].value_counts().idxmax()
            nombre_ingrediente_mas_utilizado = df_ingredientes.loc[df_ingredientes["id_ingrediente"] == ingrediente_mas_utilizado, "nombre_ingrediente"].values[0]
            st.markdown(f'<p style="color:white; font-size:15px;text-align:center;border-bottom: 2px solid #262730;padding-bottom:0.5em;">Ingrediente más Utilizado</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:#FF9999; font-size:35px;text-align:center;"> {nombre_ingrediente_mas_utilizado}</p>', unsafe_allow_html=True)
    
    _col_bar, _col_pie = st.columns(2)
    
    with _col_bar:
        with st.container(border=True):         
            # Gráfico de barras: Costos por receta
            bar_chart = px.bar(
                df_recetas,
                x="nombre_receta",
                y="costo_por_ración",
                title="Costos por Receta",
                labels={"costo_por_ración": "Costo", "nombre_receta": "Receta"},
                hover_data=["rendimiento_raciones", "costo_por_ración"],
                color = "costo_por_ración",
                color_continuous_scale="Viridis"
            )
            st.plotly_chart(bar_chart, use_container_width=True)
            
    with _col_pie:
        with st.container(border=True):
            # Gráfico de torta: Proporción por clasificación
            pie_chart = px.pie(
                df_recetas,
                names="clasificación_receta",
                values="costo_por_ración",
                title="Proporción de Costos por Clasificación",
                hover_data=["costo_por_ración"],
                color_discrete_sequence=["#FF5733", "#33FF57", "#3357FF"],
                labels={"clasificación_receta": "Clasificación"}
            )
            st.plotly_chart(pie_chart, use_container_width=True)
            
    # Tabla: Resumen de costos por receta
    st.subheader("Resumen de Costos por Receta")
    
    st.dataframe(df_recetas, hide_index= True, column_order=['nombre_receta', 'clasificación_receta','rendimiento_por_kg_receta', 'rendimiento_raciones', 'costo_total','costo_por_ración'], use_container_width=True)
