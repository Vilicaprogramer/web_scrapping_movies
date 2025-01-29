# Importamos las librerías necesarias.

import requests # Para hacer solicitudes HTTP
from bs4 import BeautifulSoup # Para extraer información de las páginas web
import pandas as pd # Para trabajar con los datasets
import re # Para trabajar con expresiones regulares

# Inicializamos un DataFrame vacío para almacenar la información de las películas.
# Las columnas representan los datos que vamos a extraer de la página web.
df_peliculas = pd.DataFrame(columns=['Título', 'Fecha de Estreno', 'Duración', 'Género 1', 'Género 2', 'Género 3', 'Dirigida por', 'Actor 1', 'Actor 2', 'Actor 3', 'Medios Rate', 'Usuarios Rate', 'Sensacine Rate', 'Sinopsis', 'Sensacine Opinión'])

# Inicializamos la variable 'pg' para controlar el número de página que vamos a procesar.
pg = 1
# Inicializamos 'last_page' para comparar la página actual con la anterior y detener el bucle si no hay cambios.
last_page = None

# Bucle infinito para recorrer todas las páginas de películas en la página web de Sensacine.
while True:
    # Realizamos la petición GET a la URL de la página actual.
    html_doc = requests.get(f'https://www.sensacine.com/peliculas/todas-peliculas/?page={pg}')
    # Creamos un objeto BeautifulSoup para parsear el HTML de la página.
    soup1 = BeautifulSoup(html_doc.text, 'html.parser')
    
    # Comprobamos si la página actual es igual a la anterior (para detectar que hemos llegado a la última página).
    if soup1 == last_page:
      print('Terminado')
      break # Salimos del bucle si no hay cambios.
    else:
      # Si la página es diferente, actualizamos 'last_page' y continuamos.
      last_page = soup1
      # Buscamos todos los elementos 'li' con clase 'mdl', que corresponden a cada película en la página.
      peliculas = soup1.find_all('li', class_='mdl')
      # Inicializamos un diccionario para guardar los datos de cada película antes de pasarlos al DataFrame.
      dc_peliculas = {}
      print(f'Comenzando la página {pg}') # Indicamos la página que estamos procesando.
      # Iteramos a través de cada película encontrada en la página.
      for pelicula in peliculas:
        # --- Extracción del título de la película ---
        try:
          # Intentamos extraer el título de la película.
          title = pelicula.find('a', class_="meta-title-link").get_text(strip=True)
          dc_peliculas['Título']= title # Guardamos el título en el diccionario.
        except:
          dc_peliculas['Título']= None # Si no encontramos el título, guardamos None.
        # --- Extracción de la fecha de estreno ---
        try:
          # Intentamos extraer la fecha de estreno.
          dc_peliculas['Fecha de Estreno']= pelicula.find('div', class_='meta-body-item meta-body-info').find('span', class_="date").get_text(strip=True)
        except:
          dc_peliculas['Fecha de Estreno']= None
        # --- Extracción de la duración ---
        try:
          # Intentamos extraer la duración de la película.
          dc_peliculas['Duración']= pelicula.find('div', class_='meta-body-item meta-body-info').find(string= re.compile("[0-9]h")).strip()
        except:
          dc_peliculas['Duración']= None

        # --- Extracción de los géneros ---
        try:
          # Intentamos extraer los géneros de la película.
          generos = pelicula.find('div', class_='meta-body-item meta-body-info').find_all('span', class_="dark-grey-link")
          # Extraemos hasta 3 géneros si están disponibles.
          if len(generos) >= 1:
            dc_peliculas['Género 1'] = generos[0].get_text(strip=True)
          else:
            dc_peliculas['Género 1'] = None
          if len(generos) >= 2:
            dc_peliculas['Género 2'] = generos[1].get_text(strip=True)
          else:
            dc_peliculas['Género 2'] = None
          if len(generos) >= 3:
            dc_peliculas['Género 3'] = generos[2].get_text(strip=True)
          else:
            dc_peliculas['Género 3'] = None
        except:
          dc_peliculas['Género 1'], dc_peliculas['Género 2'], dc_peliculas['Género 3']= None # Si no encontramos géneros, guardamos None.

        # --- Extracción del director ---
        try:
          # Intentamos extraer el nombre del director.
          dc_peliculas['Dirigida por']= pelicula.find('div', class_='meta-body-item meta-body-direction').find('span', class_="dark-grey-link").get_text(strip=True)
        except:
          dc_peliculas['Dirigida por']= None

        # --- Extracción de los actores ---
        try:
          # Intentamos extraer los nombres de los actores.
          actores = pelicula.find('div', class_='meta-body-item meta-body-actor').find_all('a', class_="dark-grey-link")
          # Inicializamos los actores a None
          dc_peliculas['Actor 1'] = None
          dc_peliculas['Actor 2'] = None
          dc_peliculas['Actor 3'] = None
          # Guardamos hasta 3 actores si están disponibles.
          if len(actores) == 1:
            dc_peliculas['Actor 1'] = actores[0].get_text(strip=True)
          elif len(actores) == 2:
            dc_peliculas['Actor 1'] = actores[0].get_text(strip=True)
            dc_peliculas['Actor 2'] = actores[1].get_text(strip=True)
          else:
            dc_peliculas['Actor 1'] = actores[0].get_text(strip=True)
            dc_peliculas['Actor 2'] = actores[1].get_text(strip=True)
            dc_peliculas['Actor 3'] = actores[2].get_text(strip=True)
        except:
          dc_peliculas['Actor 1'] = None
          dc_peliculas['Actor 2'] = None
          dc_peliculas['Actor 3'] = None

        # --- Extracción del tercer actor (otra forma que se ve en la web) ---
        try:
          # Intentamos extraer el tercer actor en caso de que no estuviera en los links anteriores
          dc_peliculas['Actor 3']= pelicula.find('div', class_='meta-body-item meta-body-actor').find('span', class_="dark-grey-link").get_text(strip=True)
        except:
          dc_peliculas['Actor 3']= None

        # --- Extracción de las valoraciones ---
        try:
          # Inicializamos las valoraciones a None
          dc_peliculas['Medios Rate']= None
          dc_peliculas['Usuarios Rate']= None
          dc_peliculas['Sensacine Rate']= None
          # Iteramos sobre los tipos de valoración (Medios, Usuarios, Sensacine).
          rate = 1
          while rate <= 4:
            try:
                for i in pelicula.find('div', class_=f'rating-holder rating-holder-{rate}').find_all('span', class_='rating-title'):
                  if i.get_text(strip=True) == 'Usuarios':
                    dc_peliculas['Usuarios Rate'] = i.find_next('span', class_="stareval-note").get_text(strip=True)
                  elif i.get_text(strip=True) == 'Sensacine':
                    dc_peliculas['Sensacine Rate']= i.find_next('span', class_="stareval-note").get_text(strip=True)
                  elif i.get_text(strip=True) == 'Medios':
                    dc_peliculas['Medios Rate'] = i.find_next('span', class_="stareval-note").get_text(strip=True)
                  else:
                    continue
                rate += 1
            except:
              rate += 1
        except:
          dc_peliculas['Medios Rate']= None
          dc_peliculas['Usuarios Rate']= None
          dc_peliculas['Sensacine Rate']= None

        # --- Extracción de la sinopsis ---
        try:
          # Intentamos extraer la sinopsis.
          dc_peliculas['Sinopsis']= pelicula.find('div', class_='synopsis').find_next('div', class_="content-txt").get_text().strip()
        except:
           dc_peliculas['Sinopsis']= None

        # --- Extracción de la opinión de Sensacine ---
        try:
          # Intentamos extraer la URL de la página de la película.
          url = pelicula.find('a', class_="meta-title-link").get('href')
          # Realizamos la petición GET a la URL de la página de la película.
          html_pelicula = requests.get(f'https://www.sensacine.com{url}sensacine/')
          # Creamos un objeto BeautifulSoup para parsear el HTML de la página de la película.
          soup2 = BeautifulSoup(html_pelicula.text, 'html.parser')
          # Intentamos extraer la opinión de Sensacine.
          soup2.find('div', class_="editorial-content cf").get_text().strip()
          dc_peliculas['Sensacine Opinión']= soup2.find('div', class_="editorial-content cf").get_text().strip()
        except:
          dc_peliculas['Sensacine Opinión']= None

        # Agregamos la información de la película al DataFrame
        df_peliculas.loc[len(df_peliculas)] = dc_peliculas
        print(dc_peliculas) # Imprimimos el diccionario con los datos de la película que acabamos de extraer.
      pg += 1 # Incrementamos el número de página para la siguiente iteración.

# Guardamos el DataFrame en un archivo CSV. No olvides cambiar el nombre del archivo y la dirección donde quieres guardarlo.
df_peliculas.to_csv('pon_aqui_el_nombre_de_tu_archivo.csv', index=False)