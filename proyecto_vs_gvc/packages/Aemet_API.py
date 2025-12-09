def aemet(fecha_ini, fecha_fin, idema, api_key = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhaW1hci5xdWVyZWphenVAYWx1bW5pLm1vbmRyYWdvbi5lZHUiLCJqdGkiOiJhNDQ4YTE3NS02ZjZiLTQ1NjUtYmNhZC1hYzJlODMxNDQwMmIiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTc2NDE3MDU2MiwidXNlcklkIjoiYTQ0OGExNzUtNmY2Yi00NTY1LWJjYWQtYWMyZTgzMTQ0MDJiIiwicm9sZSI6IiJ9.HvEKAHeogDARZ9WZrnu0d0nfXfpyEP3WIimMcawUzrw"):
    import requests
    import pandas as pd
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
    if status == 200:
        request = requests.get(url = request1.json()['datos']).json()
        return pd.DataFrame(request)
    else:
        description = request1.json()['descripcion']
        return print(f'Error: código de petición: {status}, {}')

def fechador(month, day, year = 2023, hour = 0, min = 0, sec = 0):
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

def api_info():
    import requests
    import pandas as pd
    API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhaW1hci5xdWVyZWphenVAYWx1bW5pLm1vbmRyYWdvbi5lZHUiLCJqdGkiOiJhNDQ4YTE3NS02ZjZiLTQ1NjUtYmNhZC1hYzJlODMxNDQwMmIiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTc2NDE3MDU2MiwidXNlcklkIjoiYTQ0OGExNzUtNmY2Yi00NTY1LWJjYWQtYWMyZTgzMTQ0MDJiIiwicm9sZSI6IiJ9.HvEKAHeogDARZ9WZrnu0d0nfXfpyEP3WIimMcawUzrw"
    headers = {
        "api_key": API_KEY
    }   
    url = f'https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/2023-01-01T14%3A30%3A00UTC/fechafin/2023-01-02T14%3A30%3A00UTC/estacion/9091R'
    dict_variables = requests.get(url = requests.get(url, headers = headers).json()['metadatos']).json()['campos']
    variables = pd.DataFrame(dict_variables)[['id', 'descripcion', 'tipo_datos', 'unidad']]
    variables.columns = ['VARIABLE', 'DESCRIPCIÓN', 'TIPO_DATOS', 'UNIDAD']
    return variables

def estaciones(interes = True):
    import requests
    import pandas as pd
    API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhaW1hci5xdWVyZWphenVAYWx1bW5pLm1vbmRyYWdvbi5lZHUiLCJqdGkiOiJhNDQ4YTE3NS02ZjZiLTQ1NjUtYmNhZC1hYzJlODMxNDQwMmIiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTc2NDE3MDU2MiwidXNlcklkIjoiYTQ0OGExNzUtNmY2Yi00NTY1LWJjYWQtYWMyZTgzMTQ0MDJiIiwicm9sZSI6IiJ9.HvEKAHeogDARZ9WZrnu0d0nfXfpyEP3WIimMcawUzrw"
    headers = {
        "api_key": API_KEY
    }   
    url = f'https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/2023-01-01T14%3A30%3A00UTC/fechafin/2023-01-02T14%3A30%3A00UTC/todasestaciones'
    dict_estaciones = requests.get(url = requests.get(url, headers = headers).json()['datos']).json()
    estaciones_meteorologicas = pd.DataFrame(dict_estaciones)[['indicativo', 'nombre', 'provincia']]
    estaciones_meteorologicas.columns = ['COD_IDEMA', 'NOMBRE', 'PROVINCIA']
    codigos_idema_interes = ['9091R', '1082', '5402', '1024E', '5515X', '9263D', '8416X', '6156X', '3195']
    estaciones_reto = estaciones_meteorologicas[estaciones_meteorologicas['COD_IDEMA'].isin(codigos_idema_interes)]
    if interes == True:
        return estaciones_reto
    elif not interes == True:
        return estaciones_meteorologicas
    else:
        print('El argumento interes debe ser booleano')

def read_me():
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