# Proyecto 06 – Líbere: Predicción de cancelaciones de reservas

## 1. Introducción

Este repositorio contiene el desarrollo completo del **Reto 6**, cuyo objetivo es la predicción de la cancelación de reservas en la empresa **Líbere** mediante técnicas de análisis de datos, enriquecimiento con información externa, modelización, segmentación de clientes y análisis de opiniones.

El proyecto integra distintas disciplinas vistas a lo largo del curso, incluyendo:

* **Programación y tratamiento de datos.**
* **Análisis exploratorio y visualización.**
* **Enriquecimiento mediante APIs externas (AEMET).**
* **Modelos de clasificación.**
* **Clusterización.**
* **Web scraping y técnicas de NLP.**
* **Diseño de un ecosistema Big Data con ElasticSearch.**

---

## 2. Estructura del repositorio

Todo el desarrollo se encuentra dentro de la carpeta `proyecto_vs_gvc`, cuya estructura es la siguiente:

```text
proyecto_vs_gvc/
│
├── config_files/
│   └── Archivos de configuración del proyecto
│
├── Datos/
│   ├── Originales/            <-- (Crear esta carpeta manualmente)
│   │    └── [Aquí deben ir los datos originales]
│   ├── Datos procesados
│   └── Datos meteorológicos almacenados
│
├── Graficos/
│   └── Visualizaciones generadas en las distintas fases del proyecto
│
├── packages/
│   └── Funciones reutilizables (API AEMET, EDA, preprocesamiento, etc.)
│
├── Resultado_Datos/
│   └── Resultados de los modelos de clasificación
│
├── 01-Ingesta_Limpieza_Tratado.ipynb
├── 02_1Datos_Meteo_API.ipynb
├── 02-EDA_Visualizacion.ipynb
├── 04-Clusterizacion.ipynb
├── 04-Clusterizacion2.ipynb
├── 05-Web_Scrapping.ipynb
├── 06-NLP.ipynb
├── 07-ElasticSearch.ipynb
│
├── entorno_RETO06.yml
├── indicaciones_entorno_virtual_conda.txt
└── README.md




3. Orden de ejecución del proyecto

⚠️ La ejecución del proyecto debe realizarse siguiendo estrictamente el orden indicado.
Cada notebook depende de los resultados generados en los anteriores, por lo que no se recomienda ejecutar fases de forma aislada.

Flujo de ejecución:

01-Ingesta_Limpieza_Tratado.ipynb
Carga de los datos originales y limpieza inicial (tratamiento de nulos, transformaciones y creación de variables).

02_1Datos_Meteo_API.ipynb
Enriquecimiento del dataset mediante variables meteorológicas obtenidas a través de la API de AEMET.

02-EDA_Visualizacion.ipynb
Análisis exploratorio de los datos y generación de visualizaciones.

04-Clusterizacion.ipynb
Primera fase de segmentación de clientes mediante técnicas de clusterización.

04-Clusterizacion2.ipynb
Segunda fase de clusterización y refinamiento de los segmentos obtenidos.

05-Web_Scrapping.ipynb
Web scraping de la plataforma Booking para la obtención de comentarios de usuarios.

06-NLP.ipynb
Selección, limpieza y análisis de los comentarios obtenidos mediante técnicas de Procesamiento del Lenguaje Natural (NLP).

07-ElasticSearch.ipynb
Indexación de los datos en ElasticSearch como parte del ecosistema Big Data.

⚠️ Este notebook solo puede ejecutarse en una máquina virtual con ElasticSearch en funcionamiento, por lo que no es ejecutable en un entorno local estándar.

4. Entorno de ejecución

Para garantizar la reproducibilidad del proyecto, se proporciona un entorno virtual basado en Conda.
Archivo base del entorno:
entorno_RETO06.yml
Instrucciones detalladas para su creación:
indicaciones_entorno_virtual_conda.txt
Se recomienda crear y activar el entorno antes de ejecutar cualquier notebook.

5. Datos meteorológicos y ejecución offline

El enriquecimiento con datos meteorológicos se realiza mediante la API de AEMET. No obstante, este proceso puede presentar fallos ocasionales debido a problemas de conectividad y supone un coste elevado en tiempo de ejecución.

Por este motivo:

Los datos meteorológicos ya descargados se han almacenado en la carpeta Datos/.
Si estos archivos están disponibles, no es necesario volver a ejecutar la llamada a la API.
Esto permite continuar el flujo del proyecto desde el siguiente notebook sin repetir todo el proceso.
Esta decisión mejora la eficiencia, la reproducibilidad y la experiencia de ejecución del proyecto.

6. Tiempo máximo de ejecución

⏱️ Tiempo máximo estimado de ejecución completa del proyecto: 2 horas y 30 minutos.
Este tiempo incluye:
Ejecución de todos los notebooks.
Llamadas a APIs externas.
Procesos de web scraping, NLP y modelización.
El uso de los datos meteorológicos previamente almacenados reduce significativamente el tiempo total.

7. Clave de la API de AEMET

Para obtener una clave de la API de AEMET es necesario acceder al portal oficial:
https://opendata.aemet.es/centrodedescargas/inicio

Pasos a seguir:
Pulsar en “Obtención de API Key”.
Introducir una dirección de correo electrónico válida.
Seguir las instrucciones recibidas por correo electrónico.
La clave deberá configurarse en el notebook correspondiente o en los archivos de configuración utilizados por las funciones del proyecto.

8. Consideraciones finales

El código está modularizado y apoyado en funciones reutilizables ubicadas en la carpeta packages/.
Las visualizaciones se almacenan en la carpeta Graficos/.
Los resultados de los modelos de clasificación se guardan en Resultado_Datos/.
El proyecto cumple con los requisitos de estructura, documentación y reproducibilidad exigidos en el reto.
