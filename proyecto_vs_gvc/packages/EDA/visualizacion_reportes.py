import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generar_reporte_eda_detallado(df):
    """
    Genera 7 análisis individuales exportados en formato PDF y JPG.
    Organiza los archivos en subcarpetas para mayor orden.
    """
    # Configuración de carpetas
    base_dir = "Graficos"
    folders = ["pdf", "jpg"]
    for folder in folders:
        os.makedirs(os.path.join(base_dir, folder), exist_ok=True)
    
    sns.set_theme(style="whitegrid")
    paleta_unificada = "mako"
    
    print(f"[SISTEMA EDA] Generando archivos en formatos PDF y JPG...")

    def guardar_formatos(fig, nombre_base):
        """Guarda la figura en las subcarpetas correspondientes."""
        ruta_pdf = os.path.join(base_dir, "pdf", f"{nombre_base}.pdf")
        ruta_jpg = os.path.join(base_dir, "jpg", f"{nombre_base}.jpg")
        
        fig.savefig(ruta_pdf, bbox_inches='tight')
        fig.savefig(ruta_jpg, bbox_inches='tight', dpi=300)
        plt.close(fig)
        print(f" -> Exportado: {nombre_base} (PDF/JPG)")

    # --- 1. DISTRIBUCIÓN DEL ESTADO ---
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=df, x='status', hue='status', palette=paleta_unificada, legend=False, ax=ax)
    ax.set_title('Proporción de Reservas y Cancelaciones', fontsize=14)
    ax.set_xlabel("Estado de la Reserva")
    ax.set_ylabel("Cantidad Total de Registros")
    guardar_formatos(fig, "distribucion_estado_reserva")

    # --- 2. ESTACIONALIDAD ---
    fig, ax = plt.subplots(figsize=(10, 6))
    if 'checkin_month' in df.columns:
        df_sorted = df.sort_values('checkin_month')
        sns.countplot(data=df_sorted, x='checkin_month', hue='status', palette=paleta_unificada, ax=ax)
        ax.set_title('Volumen de Reservas y Cancelaciones por Mes', fontsize=14)
        ax.set_xlabel("Mes de Entrada (Check-in)")
        ax.set_ylabel("Número de Reservas")
    guardar_formatos(fig, "estacionalidad_mensual")

    # --- 3. ANTELACIÓN ---
    fig, ax = plt.subplots(figsize=(10, 6))
    if 'days_before_checkin' in df.columns:
        sns.histplot(data=df, x='days_before_checkin', hue='status', kde=True, 
                     palette=paleta_unificada, element="step", ax=ax)
        ax.set_title('Distribución de la Antelación de la Reserva', fontsize=14)
        ax.set_xlabel("Días de Antelación (Lead Time)")
        ax.set_ylabel("Frecuencia de Reservas")
    guardar_formatos(fig, "distribucion_antelacion")

    # --- 4. SEGMENTO DE NEGOCIO ---
    fig, ax = plt.subplots(figsize=(10, 6))
    if 'business_segment' in df.columns:
        sns.countplot(data=df, x='business_segment', hue='status', palette=paleta_unificada, ax=ax)
        ax.set_title('Comportamiento de Cancelación por Segmento de Mercado', fontsize=14)
        ax.set_xlabel("Segmento de Negocio")
        ax.set_ylabel("Cantidad de Reservas")
        plt.xticks(rotation=30, ha='right')
    guardar_formatos(fig, "segmento_mercado")

    # --- 5. TARIFAS (ADR) ---
    fig, ax = plt.subplots(figsize=(10, 6))
    if 'total_adr' in df.columns:
        sns.boxplot(data=df, x='status', y='total_adr', hue='status', palette=paleta_unificada, legend=False, ax=ax)
        ax.set_title('Impacto del Precio en el Estado de la Reserva', fontsize=14)
        ax.set_xlabel("Estado de la Reserva")
        ax.set_ylabel("Tarifa Diaria Promedio (ADR)")
    guardar_formatos(fig, "analisis_tarifas_adr")

    # --- 6. DURACIÓN ESTANCIA ---
    fig, ax = plt.subplots(figsize=(10, 6))
    col_stay = 'stay_length' if 'stay_length' in df.columns else 'length_of_stay'
    if col_stay in df.columns:
        sns.violinplot(data=df, x='status', y=col_stay, hue='status', palette=paleta_unificada, legend=False, ax=ax)
        ax.set_title('Densidad de la Duración de las Estancias', fontsize=14)
        ax.set_xlabel("Estado de la Reserva")
        ax.set_ylabel("Duración de la Estancia (Noches)")
    guardar_formatos(fig, "duracion_estancia")

    # --- 7. MATRIZ DE CORRELACIÓN ---
    fig, ax = plt.subplots(figsize=(12, 10))
    numeric_df = df.select_dtypes(include=['number'])
    sns.heatmap(numeric_df.corr(), annot=True, cmap='mako', fmt=".2f", center=0, ax=ax)
    ax.set_title('Relación entre Variables Numéricas', fontsize=14)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_xlabel("Variables de Negocio")
    ax.set_ylabel("Variables de Negocio")
    guardar_formatos(fig, "matriz_correlacion")
    
    print(f"\n[FINALIZADO] Archivos disponibles en '{base_dir}/pdf' y '{base_dir}/jpg'.")