def aemet(fecha_ini, fecha_fin, idema, api_key, espera = 5):
    """Dada la fecha de inicio de estancia, la fecha final de estancia y el codigo idema de la estacion meteorológica, devuelve la consluta a la API de Aemet. Las fechas no pueden superar un rango mayor a 6 meses.

    Args:
        fecha_ini (str): Fecha de inicio del rango a consultar.
        fecha_fin (str): Fecha final del rango a consultar.
        idema (_type_): Código de la estación meteorológica de interés.
        api_key (str): clave para usar la API.
        espera (int, optional): Espera de 5 segundos para que el problema de la consulta no sea el wifi. Defaults to 5.

    Returns:
        df: df con los datos meteorológicos
    """
    import requests
    import pandas as pd
    import time
    # api_key = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhaW1hci5xdWVyZWphenVAYWx1bW5pLm1vbmRyYWdvbi5lZHUiLCJqdGkiOiJhNDQ4YTE3NS02ZjZiLTQ1NjUtYmNhZC1hYzJlODMxNDQwMmIiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTc2NDE3MDU2MiwidXNlcklkIjoiYTQ0OGExNzUtNmY2Yi00NTY1LWJjYWQtYWMyZTgzMTQ0MDJiIiwicm9sZSI6IiJ9.HvEKAHeogDARZ9WZrnu0d0nfXfpyEP3WIimMcawUzrw"
    # fecha_ini = api.fechador(month = 1, day = 2)
    # fecha_fin = api.fechador(month = 1, day = 4)
    # idema = '9091R'
    headers = {
        "api_key": api_key
    }
    cod_idema = str(idema)
    fecha_inicio = str(fecha_ini)
    fecha_final = str(fecha_fin)

    url = f'https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/{fecha_inicio}/fechafin/{fecha_final}/estacion/{cod_idema}'

    request1 = requests.get(url, headers = headers)
    status = request1.status_code
    request_json = request1.json()
    print(f'Request {status}')
    if status == 200:
        print(f'Código de petición de la API: {status}')
        url2 = request1.json()['datos']
        time.sleep(espera)
        request = requests.get(url = url2)
        contador1 = 0
        while request.status_code != 200:
            contador1 += 1
            time.sleep(espera)
            request = requests.get(url = url2)
            if contador1 <= 10:
                break
        request_json2 = request.json()
        return pd.DataFrame(request_json2)
    else:
        description = request_json['descripcion']
        print(f'Error: {description}')
        return status

def fechador(month, day, year = 2023, hour = 0, min = 0, sec = 0):
    """Dados los datos necesarios para generar una fecha, devuelve el formato de fecha que la API requiere.

    Args:
        month (int): Mes
        day (int): Día
        year (int, optional): Año. Defaults to 2023.
        hour (int, optional): Hora. Defaults to 0.
        min (int, optional): Minuto. Defaults to 0.
        sec (int, optional): Segundo. Defaults to 0.

    Returns:
        str: fecha en el formato que la API solicita.
    """
    a = str(year)
    m = str(month)
    if len(m) == 1:
        mo = '0' + m
    else: 
        mo = m
    d = str(day)
    if len(d) == 1:
        da = '0' + d
    else:
        da = d
    h = str(hour)
    if len(h) == 1:
        ho = '0' + h
    else:
        ho = h
    minut = str(min)
    if len(minut) == 1:
        mi = '0' + minut
    else:
        mi = m
    s = str(sec)
    if len(s) == 1:
        se = '0' + s
    else:
        se = s
    fecha = a + '-' + mo + '-' + da + 'T' + ho + ':' + mi + ':' + se + 'UTC'
    return fecha

def api_info(api_key):
    """Dada la clave de la api, genera un dataframe con la descripción de todas las variables que devuelve la API.

    Args:
        api_key (str): Clave de la API

    Returns:
        df: Descripción de las variables meteorologicas
    """
    import requests
    import pandas as pd
    headers = {
        "api_key": api_key
    }   
    url = f'https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/2023-01-01T14%3A30%3A00UTC/fechafin/2023-01-02T14%3A30%3A00UTC/estacion/9091R'
    dict_variables = requests.get(url = requests.get(url, headers = headers).json()['metadatos']).json()['campos']
    variables = pd.DataFrame(dict_variables)[['id', 'descripcion', 'tipo_datos', 'unidad']]
    variables.columns = ['VARIABLE', 'DESCRIPCIÓN', 'TIPO_DATOS', 'UNIDAD']
    return variables

def estaciones(api_key, interes = True, espera = 65):
    """Dada la clave de la API, devuelve la lista de las estaciones meteorologicas.

    Args:
        api_key (str): Clave de la API.
        interes (bool): Si True, las estaciones meteorológicas son las más cercanas a los hoteles del reto. Si False, devuelve todas las estaciones meteorológicas de España. Defaults to True.
        espera (int, optional): segundos de espera para evitar errores de conexión a Internet. Defaults to 65.

    Returns:
        df: Data Frame con los códigos idema, nombre y provincia de la estación.
    """
    import requests
    import pandas as pd
    import time
    headers = {
        "api_key": api_key
    }   
    url = f'https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/2023-01-01T14%3A30%3A00UTC/fechafin/2023-01-02T14%3A30%3A00UTC/todasestaciones'
    request1 = requests.get(url, headers = headers)
    code = request1.status_code
    print(code)
    if code == 429:
        while code != 200:
            time.sleep(espera)
            request1 = requests.get(url, headers = headers)
            code = request1.status_code
            print(code)
    dict_estaciones = requests.get(url = request1.json()['datos']).json()
    estaciones_meteorologicas = pd.DataFrame(dict_estaciones)[['indicativo', 'nombre', 'provincia']]
    estaciones_meteorologicas.columns = ['COD_IDEMA', 'NOMBRE', 'PROVINCIA']
    codigos_idema_interes = ['9091R', '1082', '5402', '1024E', '5530E', '9263D', '8414A', '6155A', '3129']
    estaciones_reto = estaciones_meteorologicas[estaciones_meteorologicas['COD_IDEMA'].isin(codigos_idema_interes)]
    if interes == True:
        return estaciones_reto
    elif not interes == True:
        return estaciones_meteorologicas
    else:
        print('El argumento interes debe ser booleano')

def read_me():
    """Explicación de como usar las funciones de este archivo .py.
    """
    print('Para hacer consultas a la API, se necesitan 3 datos:')
    print('* La fecha-hora de inicio (fecha_ini)')
    print('* La fecha-hora de final (fecha_fin)')
    print('* El código de la estación emteorológica de interés (idema)')
    print('\n')
    print('Las fechas se formatean con la función fechador, donde hay que indicar el año, el mes, el día, la hora, el minuto y el segundo.')
    print('Aunque la mayoría de las veces solo se necesitaran las primeras 3 ó 4. Por ello, solo es obligatorio especificar esos datos.')
    print('\n')
    print('Para conseguir el código de la estación meteorológica de turno, se puede usar la función estaciones():')
    print('* Si se marca en True (por defecto), saldrán los datos de las que se han considerado las más cercanas a los hoteles de interés.')
    print('* Si se marca en False, saldrán los mismos datos, pero para todas las estaciones meteorológica a las que tiene acceso la API.')
    print('\n')
    print('Para hacer la consulta a la API, hay que usar el comando aemet()')
    print('Cabe destacar que las consultas a la API solo pueden ser de un rango de 6 meses máximo.')
    print('\n')
    print('Finalmente, hay otro comando más, llamado api_info(), que al ejecutarlo dará la información de cada variable de las consultas de la API.')
    print('\n')
    print('Para evitar posibles errores en la cantidad de peticiones por minuto, todas las funciones generadas tendrán en pretiempo de actuación por defecto de un minuto.')