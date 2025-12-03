import pandas as pd
import numpy as np

df = pd.read_csv("Datos\Originales\cancellation_data_for_mondragon_unibertsitatea_2024.csv")

#limpiar columnas
df.columns = (
    df.columns.str.strip()
    .str.lower()#minusculas
    .str.replace(" ", "_")#sin espacios
    .str.replace(r"[^\w_]", "", regex=True)#quitar símbolos raros
)

#eliminar duplicados
df = df.drop_duplicates()#2.306 filas duplicadas

#convertir columnas a fechas
columnas_fecha = ["booked_at", "checkin_time", "checkout_time", "cancelled_at"]

for col in columnas_fecha:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

#convertir meses y dias en numeros
month_map = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}

day_map = {
    "Monday": 1, "Tuesday": 2, "Wednesday": 3,
    "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7
}

if "checkin_month" in df.columns:
    df["checkin_month"] = df["checkin_month"].map(month_map)

if "checkin_day" in df.columns:
    df["checkin_day"] = df["checkin_day"].map(day_map)

#crear variable de cancelación(1: si lo ha cancelado)
df["is_cancelled"] = df["cancelled_at"].notna().astype(int)

#detectar errores en las fechas: checkout antes del checkin y cancelaciones antes de reserva
df["fecha_incoherente"] = False#solo hay una, preguntar si merece la pena

df.loc[df["checkout_time"] < df["checkin_time"], "fecha_incoherente"] = True
df.loc[df["cancelled_at"] < df["booked_at"], "fecha_incoherente"] = True

df = df[df["fecha_incoherente"] == False] #hemos decidido borrarla porque este error nos podía dar problemas

#NUEVAS VARIABLES
#días entre reserva y check in
df["days_before_checkin"] = (
    df["checkin_time"] - df["booked_at"]
).where(df["checkin_time"].notna() & df["booked_at"].notna()).dt.days#solo los que no tienen na

#días entre reserva y cancelación(solo cuando hay cancelación)
df["days_before_cancel"] = (
    df["cancelled_at"] - df["booked_at"]
).dt.days

#duración de la estancia(solo en reservas no canceladas)
df["stay_length"] = (
    df["checkout_time"] - df["checkin_time"]
).dt.days


#limpiar los valores de dentro de las columnas categoricas
categoricas = [
    "channel", "reservation_status", "room_type", "payment_method",
    "property_name", "country"
]

for col in categoricas:
    if col in df.columns:
        df[col] = df[col].astype(str).str.lower().str.strip()

#no imputamos porque los missings tienen sentido. no va a haber fecha de cancelación si no ha cancelado y tampoco va a haber chekout_time si lo ha cancelado


#filas problemáticas (>450 o < -1)
df_filtrado = df.loc[(df["days_before_checkin"] > 450) | (df["days_before_checkin"] < -1)].copy()

# Borrar esas filas de df (quedarse con lo contrario)
df = df.loc[(df["days_before_checkin"] <= 450) & (df["days_before_checkin"] >= -1)].copy()
#borrar esta columna ya que como hemos eliminado la unica fecha con error ya no nos hace falta 
df = df.drop(columns=["fecha_incoherente"])

print(df)






