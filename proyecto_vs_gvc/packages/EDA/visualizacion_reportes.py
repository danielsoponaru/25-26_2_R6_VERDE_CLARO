import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generar_reporte_eda_detallado(df):
    """
    Genera 7 archivos PDF individuales con títulos limpios (sin números) 
    y ejes con nombres de negocio formales.
    """
    ruta_carpeta = "Graficos"
    os.makedirs(ruta_carpeta, exist_ok=True)
    
    sns.set_theme(style="whitegrid")
    paleta_unificada = "mako"
    
    print(f"[SISTEMA EDA] Generando reportes individuales con etiquetas de negocio...")

    def guardar_grafico(fig, nombre):
        ruta = os.path.join(ruta_carpeta, f"{nombre}.pdf")
        fig.savefig(ruta, bbox_inches='tight')
        plt.close(fig)
        print(f" -> Guardado: {ruta}")

    # --- 1. DISTRIBUCIÓN DEL ESTADO ---
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=df, x='status', hue='status', palette=paleta_unificada, legend=False, ax=ax)
    ax.set_title('Proporción de Reservas y Cancelaciones', fontsize=14)
    ax.set_xlabel("Estado de la Reserva")
    ax.set_ylabel("Cantidad Total de Registros")
    guardar_grafico(fig, "distribucion_estado_reserva")

    # --- 2. ESTACIONALIDAD ---
    fig, ax = plt.subplots(figsize=(10, 6))
    if 'checkin_month' in df.columns:
        df_sorted = df.sort_values('checkin_month')
        sns.countplot(data=df_sorted, x='checkin_month', hue='status', palette=paleta_unificada, ax=ax)
        ax.set_title('Volumen de Reservas y Cancelaciones por Mes', fontsize=14)
        ax.set_xlabel("Mes de Entrada (Check-in)")
        ax.set_ylabel("Número de Reservas")
    guardar_grafico(fig, "estacionalidad_mensual")

    # --- 3. ANTELACIÓN ---
    fig, ax = plt.subplots(figsize=(10, 6))
    if 'days_before_checkin' in df.columns:
        sns.histplot(data=df, x='days_before_checkin', hue='status', kde=True, 
                     palette=paleta_unificada, element="step", ax=ax)
        ax.set_title('Distribución de la Antelación de la Reserva', fontsize=14)
        ax.set_xlabel("Días de Antelación (Lead Time)")
        ax.set_ylabel("Frecuencia de Reservas")
    guardar_grafico(fig, "distribucion_antelacion")

    # --- 4. SEGMENTO DE NEGOCIO ---
    fig, ax = plt.subplots(figsize=(10, 6))
    if 'business_segment' in df.columns:
        sns.countplot(data=df, x='business_segment', hue='status', palette=paleta_unificada, ax=ax)
        ax.set_title('Comportamiento de Cancelación por Segmento de Mercado', fontsize=14)
        ax.set_xlabel("Segmento de Negocio")
        ax.set_ylabel("Cantidad de Reservas")
        plt.xticks(rotation=30, ha='right')
    guardar_grafico(fig, "segmento_mercado")

    # --- 5. TARIFAS (ADR) ---
    fig, ax = plt.subplots(figsize=(10, 6))
    if 'total_adr' in df.columns:
        sns.boxplot(data=df, x='status', y='total_adr', hue='status', palette=paleta_unificada, legend=False, ax=ax)
        ax.set_title('Impacto del Precio en el Estado de la Reserva', fontsize=14)
        ax.set_xlabel("Estado de la Reserva")
        ax.set_ylabel("Tarifa Diaria Promedio (ADR)")
    guardar_grafico(fig, "analisis_tarifas_adr")

    # --- 6. DURACIÓN ESTANCIA ---
    fig, ax = plt.subplots(figsize=(10, 6))
    col_stay = 'stay_length' if 'stay_length' in df.columns else 'length_of_stay'
    if col_stay in df.columns:
        sns.violinplot(data=df, x='status', y=col_stay, hue='status', palette=paleta_unificada, legend=False, ax=ax)
        ax.set_title('Densidad de la Duración de las Estancias', fontsize=14)
        ax.set_xlabel("Estado de la Reserva")
        ax.set_ylabel("Duración de la Estancia (Noches)")
    guardar_grafico(fig, "duracion_estancia")

    # --- 7. MATRIZ DE CORRELACIÓN ---
    fig, ax = plt.subplots(figsize=(12, 10))
    numeric_df = df.select_dtypes(include=['number'])
    # Renombrar columnas solo para el gráfico de correlación para que se vean bien
    corr_matrix = numeric_df.corr()
    sns.heatmap(corr_matrix, annot=True, cmap='mako', fmt=".2f", center=0, ax=ax)
    ax.set_title('Relación entre Variables Numéricas', fontsize=14)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_xlabel("Variables de Negocio")
    ax.set_ylabel("Variables de Negocio")
    guardar_grafico(fig, "matriz_correlacion")
    
    print(f"\n[FINALIZADO] Los 7 reportes han sido generados en la carpeta '{ruta_carpeta}'.")