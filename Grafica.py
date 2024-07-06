import matplotlib.pyplot as plt
import requests

import Filtro_Df as fil
import httpx


def obtener_imagen(animal_name, subscription_key, search_url, clase):
    api_key = subscription_key
    image_search_endpoint = search_url

    headers = {'Ocp-Apim-Subscription-Key': api_key}

    query = animal_name + clase

    params = {"q": query, "license": "public", "imageType": "photo", 'count': '50', 'offset': '0'}

    default_image_url = "https://thumbs.dreamstime.com/b/animales-de-la-selva-65642301.jpg"
    try:
        response = httpx.get(image_search_endpoint, headers=headers, params=params)
        response.raise_for_status()  # Lanza una excepción si la respuesta no es exitosa

        resultset = response.json()

        if 'value' in resultset and len(resultset['value']) > 0:
            # Devuelve la URL de la primera imagen encontrada
            return resultset['value'][0]['contentUrl']
        else:
            print(f"No se encontraron resultados de imágenes para {animal_name}")
            return default_image_url
    except httpx.HTTPStatusError as http_err:
        print(f"Error HTTP: {http_err}")
        return default_image_url
    except Exception as err:
        print(f"Otro error: {err}")
        return default_image_url
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

    animal_info = {}
    for animal in top_5_animals:
        animal_data = df_top_5_animals[df_top_5_animals['vernacularName'] == animal].iloc[0]
        image_url = obtener_imagen(animal, subscription_key, search_url, animal_data['class'])
        animal_info[animal] = {
            'image_url': image_url,
            'family': animal_data['family'],
            'locality': animal_data['locality'],
            'habitat': animal_data['habitat'],
            'class': animal_data['class']
        }

    return animal_info
