import pandas as pd
import os
import datetime
import numpy as np
import time
import Aemet_API as api
import requests
import warnings
warnings.filterwarnings('ignore')

import json
path_json = os.path.join('..', 'config_files', 'credentials.json')
with open(path_json, 'r') as file:
    data = json.load(file)
API_KEY = data['API_KEY']

estaciones = api.estaciones(api_key = API_KEY)
estaciones.columns = ['idema_code', 'meteorology_station', 'region']

df = pd.read_csv(os.path.join('..', 'Datos', 'Transformados', 'Limpios', 'df_limpio.csv'))
df = df[df['lenght_of_stay'] < 31]

df['checkin_time'] = pd.to_datetime(df['checkin_time'])
df['checkout_time'] = pd.to_datetime(df['checkout_time'])

df['checkin_day_n'] = df['checkin_time'].dt.day.astype('str')
df['checkin_month_n'] = df['checkin_time'].dt.month.astype('str')
df['checkin_year_n'] = df['checkin_time'].dt.year.astype('str')
df['checkout_day_n'] = df['checkout_time'].dt.day.astype('str')
df['checkout_month_n'] = df['checkout_time'].dt.month.astype('str')
df['checkout_year_n'] = df['checkout_time'].dt.year.astype('str')

hoteles = df['asset'].unique().tolist()
idx_hotel = []
for i in df['asset']:
    idx_hotel.append(hoteles.index(i))
ciudades = ['DONOSTIA', 'VITORIA', 'BILBAO', 'BILBAO', 'VALENCIA', 'VALENCIA', 'MADRID', 'MALAGA', 'GRANADA', 'MALAGA', 'CORDOBA', 'PAMPLONA']
cities = []
for i in idx_hotel:
    cities.append(ciudades[i])
df['city'] = cities
df['city'] = df['city'].astype('category')
ciudad_provincia = {'DONOSTIA': 'GIPUZKOA', 'VITORIA': 'ARABA/ALAVA', 'BILBAO': 'BIZKAIA', 'VALENCIA': 'VALENCIA', 'MADRID': 'MADRID', 'MALAGA': 'MALAGA', 'GRANADA': 'GRANADA', 'CORDOBA': 'CORDOBA', 'PAMPLONA': 'NAVARRA'}
df['region'] = df['city'].map(ciudad_provincia)
df['idema_code'] = df.merge(right = estaciones, on = 'region', how = 'left')['idema_code']
if df['idema_code'].isna().sum() != 0:
    a = df[~df['idema_code'].isna()]
    var1404 = df[df['idema_code'].isna()].merge(right = estaciones, on = 'region', how = 'left')
    var1404['idema_code'] = var1404['idema_code_y']
    del var1404['idema_code_x']
    del var1404['idema_code_y']
    df = pd.concat([a, var1404], axis = 0)

del estaciones
del hoteles
del idx_hotel
del ciudades
del cities
del ciudad_provincia
del a
del var1404

df_meteo = pd.DataFrame()
wait = 61
wait2 = 35
for idema_code in df['idema_code'].unique().tolist():
      idema = str(idema_code)
      df_meteo_to_join_1 = api.aemet(fecha_ini = api.fechador(year = 2023, month = 1, day = 1), 
                                     fecha_fin = api.fechador(year = 2023, month = 4, day = 30),
                                     idema = idema,
                                     espera = wait2,
                                     api_key = API_KEY)
      if isinstance(df_meteo_to_join_1, int):
            while isinstance(df_meteo_to_join_1, int):
                  time.sleep(wait)
                  df_meteo_to_join_1 = api.aemet(fecha_ini = api.fechador(year = 2023, month = 1, day = 1), 
                                                fecha_fin = api.fechador(year = 2023, month = 4, day = 30),
                                                idema = idema,
                                                espera = wait2,
                                                api_key = API_KEY)
      print(f'1_{idema_code}')
      #################################################################################################
      df_meteo_to_join_2 = api.aemet(fecha_ini = api.fechador(year = 2023, month = 5, day = 1),
                                     fecha_fin = api.fechador(year = 2023, month = 8, day = 31),
                                     idema = idema,
                                     espera = wait2,
                                     api_key = API_KEY)
      if isinstance(df_meteo_to_join_2, int):
            while isinstance(df_meteo_to_join_2, int):
                  time.sleep(wait)
                  df_meteo_to_join_2 = api.aemet(fecha_ini = api.fechador(year = 2023, month = 5, day = 1), 
                                                fecha_fin = api.fechador(year = 2023, month = 8, day = 31),
                                                idema = idema,
                                                espera = wait2,
                                                api_key = API_KEY)
      print(f'2_{idema_code}')
      #################################################################################################  
      df_meteo_to_join_3 = api.aemet(fecha_ini = api.fechador(year = 2023, month = 9, day = 1),
                                     fecha_fin = api.fechador(year = 2024, month = 2, day = 28),
                                     idema = idema,
                                     espera = wait2,
                                     api_key = API_KEY)
      if isinstance(df_meteo_to_join_3, int):
            while isinstance(df_meteo_to_join_3, int):
                  time.sleep(wait)
                  df_meteo_to_join_3 = api.aemet(fecha_ini = api.fechador(year = 2023, month = 9, day = 1),
                                                fecha_fin = api.fechador(year = 2024, month = 2, day = 28),
                                                idema = idema,
                                                espera = wait2,
                                                api_key = API_KEY)
      print(f'3_{idema_code}')
      #################################################################################################
      df_meteo_to_join = pd.concat([df_meteo_to_join_1, df_meteo_to_join_2, df_meteo_to_join_3], axis = 0)
      df_meteo = pd.concat([df_meteo, df_meteo_to_join], axis = 0)
      print(f'COMPLETO_{idema_code}')
      #################################################################################################
      del df_meteo_to_join
      del df_meteo_to_join_1
      del df_meteo_to_join_2
      del df_meteo_to_join_3

del wait
del wait2
del idema
del idema_code

df_meteo = df_meteo.reset_index()
if 'index' in df_meteo.columns.to_list():
    df_meteo = df_meteo[df_meteo.columns.to_list()[1:]]

lista_fecha_checkin = []
lista_fecha_checkout = []
for i in range(df.shape[0]):
    f_checkin = api.fechador(year = df['checkin_year_n'].tolist()[i], 
                             month = df['checkin_month_n'].tolist()[i], 
                             day = df['checkin_day_n'].tolist()[i])
    f_checkout = api.fechador(year = df['checkout_year_n'].tolist()[i], 
                             month = df['checkout_month_n'].tolist()[i], 
                             day = df['checkout_day_n'].tolist()[i])
    lista_fecha_checkin.append(f_checkin[0:10])
    lista_fecha_checkout.append(f_checkout[0:10])
df_indices_meteo = pd.DataFrame({'F_C_I': lista_fecha_checkin, 'F_C_O': lista_fecha_checkout, 'IDEMA': df['idema_code']})

del lista_fecha_checkin
del lista_fecha_checkout
del i
del f_checkin
del f_checkout

def estadisticos(var, df = df_meteo):
    """Dado el nombre de una variable y el dataframe, devuelve un dataframe con estadísticos de la variable.

    Args:
        var (str): Nombre de la variable.
        df (dataframe): Data Frame. Defaults to df_meteo.

    Returns:
        df: DataFrame de estadísticos de la variable solicitada (Mínimo, Primer, Segundo y Tercer Cuartíl; Máximo, IQR, Media y Desviación Estándar)
    """
    import numpy as np
    import pandas as pd
    v = str(var)
    v_meteorologica = df[v].str.replace(',', '.').astype('float').to_list()
    meteo_min = min(v_meteorologica)
    meteo_Q1 = np.quantile(v_meteorologica, 0.25)
    meteo_Q2 = np.quantile(v_meteorologica, 0.5)
    meteo_Q3 = np.quantile(v_meteorologica, 0.75)
    meteo_med = np.mean(v_meteorologica)
    meteo_IQR = meteo_Q3 - meteo_Q1
    meteo_max = max(v_meteorologica)
    meteo_std = np.std(v_meteorologica)
    instancia_meteo_var = [float(meteo_min), 
                            float(meteo_Q1), 
                            float(meteo_Q2), 
                            float(meteo_Q3), 
                            float(meteo_max), 
                            float(meteo_IQR),
                            float(meteo_med), 
                            float(meteo_std)]
    instancia_var = ['MIN', 'Q1', 'Q2', 'Q3', 'MAX', 'IQR', 'MEAN', 'STD']
    meteo_df = np.transpose(pd.DataFrame({'VALOR': instancia_meteo_var}))
    meteo_df.columns = instancia_var
    return meteo_df

while 'Ip' in df_meteo['prec'].to_list():
    idx_ip = df_meteo['prec'].to_list().index('Ip')
    df_meteo['prec'].iloc[idx_ip] = '0,0'
    del idx_ip

var_meteorologicas = ['tmin', 'tmax', 'tmed', 'prec', 'sol', 'velmedia', 'racha', 'hrMedia']

great_meteo_stat = pd.DataFrame()
for iter in range(df_indices_meteo.shape[0]):
    idema_codigo = df_indices_meteo['IDEMA'].to_list()[iter]
    lim_inf = df_indices_meteo['F_C_I'].tolist()[iter]
    lim_sup = df_indices_meteo['F_C_O'].tolist()[iter]
    boolean_serie_1 = (df_meteo[df_meteo['indicativo'] == str(idema_codigo)]['fecha'] == str(lim_inf))
    range_inf = boolean_serie_1.reset_index()[boolean_serie_1.to_list()]['index']
    boolean_serie_2 = (df_meteo[df_meteo['indicativo'] == str(idema_codigo)]['fecha'] == str(lim_sup))
    range_sup = boolean_serie_2.reset_index()[boolean_serie_2.to_list()]['index']
    meteo_range = range_inf.to_list() + range_sup.to_list()
    var1029 = df_meteo.iloc[meteo_range[0]:meteo_range[1]]
    prec_var = var1029['prec'].to_list()
    if var1029.shape[0] == 0:
        for columna in var1029.columns.to_list():
            var1029[str(columna)] = [0, 0]
            del columna
    for ser in var1029.columns:
        serie = str(ser)
        var1029[serie] = var1029[serie].astype('str')
        del serie
        del ser
    meteo_stat_instance = pd.DataFrame()
    for var in var_meteorologicas:
        meteo_stat = estadisticos(str(var), df = var1029)
        meteo_stat_instance = pd.concat([meteo_stat_instance, meteo_stat], axis = 1)
    great_meteo_stat = pd.concat([great_meteo_stat, meteo_stat_instance], axis = 0)

del boolean_serie_1
del boolean_serie_2
del idema_codigo
del iter
del lim_inf
del lim_sup
del meteo_range
del meteo_stat
del meteo_stat_instance
del prec_var
del range_inf
del range_sup
del var
del var1029
del df_meteo

stat_name = ['MIN', 'Q1', 'Q2', 'Q3', 'MAX', 'IQR', 'MEAN', 'STD']
colnames = []
for meteo in var_meteorologicas:
    for name in stat_name:
        col = str(name) + '_' + str(meteo)
        colnames.append(col)
great_meteo_stat.columns = colnames
great_meteo_stat = great_meteo_stat.reset_index()
great_meteo_stat = great_meteo_stat[colnames]

del var_meteorologicas
del colnames
del col
del meteo
del name
del stat_name

df_fechas = df_indices_meteo.reset_index()
del df_fechas['index']
df_meteo_to_join = pd.concat([df_fechas, great_meteo_stat], axis = 1)

del df_indices_meteo
del df_fechas
del great_meteo_stat

df_cancelation = df.reset_index()
del df_cancelation['index']
df_final = pd.concat([df_cancelation, df_meteo_to_join], axis = 1)

del df_meteo_to_join
del df
del df_cancelation

df = df_final
for var in ['checkin_day_n', 'checkin_month_n', 'checkin_year_n', 'checkout_day_n', 'checkout_month_n', 'checkout_year_n', 'meteorology_station', 'idema_code', 'F_C_I', 'F_C_O']:
    del df[str(var)]

df.to_csv(path_or_buf = os.path.join('..', 'Datos', 'Transformados', 'df_meteorologico.csv'))