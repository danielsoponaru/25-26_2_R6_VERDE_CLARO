import pandas as pd
import numpy as np

df = pd.read_csv("DATOS/cancellation_data_for_mondragon_unibertsitatea_2024.csv")
print(df)

#limpiar columnas
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace(r"[^\w_]", "", regex=True)
)

#eliminar duplicados
df = df.drop_duplicates()

#convertir en fecha
columnas_fecha = [
    "booked_at",
    "checkin_time",
    "checkout_time",
    "cancelled_at"
]

for col in columnas_fecha:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")
#convertir checkin_month en números del 1 al 12 y checkin_day del 1 al 7
#meses
month_map = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}

#días
day_map = {
    "Monday": 1, "Tuesday": 2, "Wednesday": 3,
    "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7
}

df["checkin_month"] = df["checkin_month"].map(month_map)
df["checkin_day"]   = df["checkin_day"].map(day_map)

#no imputamos porque los missings tienen sentido. no va a haber fecha de cancelación si no ha cancelado y tampoco va a haber chekout_time si lo ha cancelado



