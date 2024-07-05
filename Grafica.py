import matplotlib.pyplot as plt
import requests

import Filtro_Df as fil
import httpx


def obtener_imagen(animal_name, subscription_key, search_url):
    api_key = subscription_key
    image_search_endpoint = search_url

    headers = {'Ocp-Apim-Subscription-Key': api_key}

    query = animal_name + " animal"

    params = {"q": query, "license": "public", "imageType": "photo", 'count': '50', 'offset': '0'}

    try:
        response = httpx.get(image_search_endpoint, headers=headers, params=params)
        response.raise_for_status()  # Lanza una excepción si la respuesta no es exitosa

        resultset = response.json()

        if 'value' in resultset and len(resultset['value']) > 0:
            # Devuelve la URL de la primera imagen encontrada
            return resultset['value'][0]['contentUrl']
        else:
            print(f"No se encontraron resultados de imágenes para {animal_name}")
            return None
    except httpx.HTTPStatusError as http_err:
        print(f"Error HTTP: {http_err}")
        return None
    except Exception as err:
        print(f"Otro error: {err}")
        return None
def graficar(df, mun,subscription_key, search_url):

    df_municipality = fil.filtro_Municipio(df,mun)

    animal_counts = df_municipality['vernacularName'].value_counts()

    top_5_animals = animal_counts.head(5).index


    df_top_5_animals = fil.filtro_Animales(df_municipality,top_5_animals)

    top_5_counts = df_top_5_animals['vernacularName'].value_counts()

    plt.figure(figsize=(10, 6))
    plt.pie(top_5_counts, labels=top_5_counts.index, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')

    image_path = 'static/images/grafica.png'
    plt.savefig(image_path)
    plt.close()

    animal_images = {animal: obtener_imagen(animal, subscription_key, search_url) for animal in top_5_animals}

    return image_path, animal_images
