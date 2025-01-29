# 🎬 Sensacine Scraper: ¡Descubre el Cine con un Click!🍿

¡Hola a todos los cinéfilos y entusiastas del código! 👋  
Este repositorio contiene un script de Python creado para extraer información de películas del sitio web Sensacine.  
¿Quieres saber qué películas son las más populares, cuáles son sus géneros y quiénes son sus protagonistas?  
¡Este script te lo pone fácil!

---

## ✨ ¿Qué hace este script?

Este script de web scraping se encarga de:

- **Recolectar información** de películas de todas las páginas de Sensacine.
- **Extraer detalles clave**, como:
  - Título, fecha de estreno y duración.
  - Géneros, director y actores principales.
  - Valoraciones de medios, usuarios y Sensacine.
  - Sinopsis y opiniones de Sensacine.
- **Organizar los datos** en un DataFrame de Pandas para su fácil manejo.

---

## 🚀 ¿Cómo usarlo?

1.  **Clona este repositorio:**
    ```bash
     git clone https://github.com/Vilicaprogramer/web_scrapping_movies.git
    ```
2.  **Instala las dependencias:**
    ```bash
    pip install pandas requests beautifulsoup4
    ```
3.  **Ejecuta el script:**
    ```bash
    python Ingesta_datos_Sensacine.py
    ```
4.  **Explora los datos:** Antes de ejecutar el archivo recuerda cambiar en la última linea del código la ubicación y el nombre del archivo csv que se genrará
    ```python
    df_peliculas.to_csv('pon_aqui_el_nombre_de_tu_archivo.csv', index=False, encoding='utf-8')
    ```

## 🛠️ ¡Contribuye!

¡Este proyecto es para la comunidad! Si tienes ideas para mejorar el script, como:

*   Añadir nuevos campos de datos a extraer.
*   Hacer el script más eficiente y rápido.
*   Adaptarlo para otros sitios web de cine.
*   Cualquier otra mejora que se te ocurra!

¡No dudes en abrir un issue o enviar un pull request!  Toda la ayuda es bienvenida. 🙏

## 🤝 Feedback

Si usas el script y tienes alguna pregunta, comentario o sugerencia, por favor, ¡no dudes en contactarme! Tu feedback es fundamental para seguir mejorando.
```
