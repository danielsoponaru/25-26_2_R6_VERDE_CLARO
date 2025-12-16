import pandas as pd
import numpy as np
import warnings
import os

# Configuración global
warnings.filterwarnings("ignore", category=UserWarning, module='pandas')

# ==============================================================================
# MACRO-FUNCIÓN 1: CARGA DE DATOS
# ==============================================================================
def cargar_datos_raw(ruta_archivo):
    """
    Carga el CSV original desde la ruta especificada sin aplicar transformaciones.
    """
    try:
        print(f"--- Cargando archivo desde: {ruta_archivo} ---")
        # Leemos el CSV
        df = pd.read_csv(ruta_archivo)
        print(f"-> Carga exitosa. Filas cargadas: {len(df)}")
        return df
    except Exception as e:
        print(f"!!! Error al cargar el archivo: {e}")
        return None

# ==============================================================================
# MACRO-FUNCIÓN 2: PIPELINE DE LIMPIEZA Y TRANSFORMACIÓN
# ==============================================================================
def ejecutar_pipeline_limpieza(df_input, ruta_guardado=None):
    """
    Recibe el dataframe crudo, lo limpia y, si se indica ruta_guardado, 
    exporta el resultado a CSV.
    """
    print("\n" + "="*40)
    print("INICIANDO PROCESO DE LIMPIEZA Y TRANSFORMACIÓN")
    print("="*40)
    
    # FASE A: PREPARACIÓN TÉCNICA
    df = df_input.copy()

    # 1. Normalización de nombres
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^\w_]", "", regex=True)
    )

    # 2. Eliminación de duplicados
    df = df.drop_duplicates()

    # 3. Variables Económicas
    cols_dinero = ["reservation_net_value", "total_adr"]
    for col in cols_dinero:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "reservation_net_value" in df.columns:
        df = df[df["reservation_net_value"] > 0].copy()

    # 4. Conversión de Fechas (Incluyendo last_entry...)
    columnas_fecha = [
        "booked_at", "checkin_time", "checkout_time", 
        "cancelled_at", "asset_opening_date",
        "last_entry_form_completed_at"
    ]

    for col in columnas_fecha:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # FASE B: MAPEOS
    month_map = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
    day_map = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7}

    if "checkin_month" in df.columns: df["checkin_month"] = df["checkin_month"].map(month_map)
    if "checkin_day" in df.columns: df["checkin_day"] = df["checkin_day"].map(day_map)

    categoricas = ["channel", "reservation_status", "room_type", "payment_method", "property_name", "country", "origin", "requested_category", "business_segment", "asset_type", "status"]
    for col in categoricas:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().str.strip()

    # FASE C: INGENIERÍA
    df["is_cancelled"] = df["cancelled_at"].notna().astype(int)
    
    df["fecha_incoherente"] = False
    if "checkout_time" in df.columns and "checkin_time" in df.columns:
        df.loc[df["checkout_time"] < df["checkin_time"], "fecha_incoherente"] = True
    if "cancelled_at" in df.columns and "booked_at" in df.columns:
        df.loc[df["cancelled_at"] < df["booked_at"], "fecha_incoherente"] = True
        
    df = df[df["fecha_incoherente"] == False]

    df["days_before_checkin"] = (df["checkin_time"] - df["booked_at"]).where(df["checkin_time"].notna() & df["booked_at"].notna()).dt.days
    df["days_before_cancel"] = (df["cancelled_at"] - df["booked_at"]).dt.days
    df["stay_length"] = (df["checkout_time"] - df["checkin_time"]).dt.days

    # FASE D: FILTROS DE NEGOCIO
    if "lead_time" in df.columns:
        df = df[df["lead_time"] >= 0]

    col_stay = "lenght_of_stay" if "lenght_of_stay" in df.columns else "length_of_stay"
    if col_stay in df.columns:
        df = df[(df[col_stay] > 0) & (df[col_stay] <= 30)]

    df = df.loc[(df["days_before_checkin"] <= 450) & (df["days_before_checkin"] >= -1)].copy()
    df = df.drop(columns=["fecha_incoherente"])

    if "stay_length" in df.columns:
        df = df[df["stay_length"] <= 30]

    # --- NUEVO: GUARDAR CSV ---
    if ruta_guardado:
        try:
            # Crea la carpeta si no existe (ej: Datos/Transformados/Limpios)
            os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)
            
            df.to_csv(ruta_guardado, index=False)
            print(f"\n[EXPORTACIÓN] -> Archivo guardado exitosamente en: {ruta_guardado}")
        except Exception as e:
            print(f"\n[ERROR] No se pudo guardar el archivo CSV: {e}")

    print(f"PROCESO COMPLETADO. DataFrame Final: {len(df)} filas.")
    return df