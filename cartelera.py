import tkinter as tk
# import os
# import qrcode
import requests

API_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"


def autorizacion() -> dict:
    
    Headers: dict = { "Authorization" : f"Bearer {API_KEY}" }

    return Headers


def get_peliculas(Headers: dict) -> list[dict]:

    try:
        respuesta = requests.get("http://vps-3701198-x.dattaweb.com:4000/movies", headers=Headers)
        respuesta.raise_for_status() # Esto es necesario para que tambien agarre los errores HTTP
    except requests.exceptions.RequestException as e:
        raise SystemExit(e) # Termina el programa y muestra el error
    
    info_peliculas: list[dict] = respuesta.json()

    return info_peliculas


def get_pelicula_por_Id(Headers: dict, pelicula_id: int) -> dict:

    try:
        respuesta = requests.get(f"http://vps-3701198-x.dattaweb.com:4000/movies/{pelicula_id}", headers=Headers)
        respuesta.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    info_pelicula_individual: list[dict] = respuesta.json()

    return info_pelicula_individual


def get_poster_por_Id(Headers: dict, poster_id: int) -> dict:

    try:
        respuesta = requests.get(f"http://vps-3701198-x.dattaweb.com:4000/posters/{poster_id}", headers=Headers)
        respuesta.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    img_poster: dict = respuesta.json()

    return img_poster


def get_snacks(Headers: dict) -> dict:

    try:
        respuesta = requests.get(f"http://vps-3701198-x.dattaweb.com:4000/snacks", headers=Headers)
        respuesta.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    info_snacks: dict = respuesta.json()

    return info_snacks


def get_proyeccion(Headers: dict, pelicula_id: int) -> list:

    try:
        respuesta = requests.get(f"http://vps-3701198-x.dattaweb.com:4000/movies/{pelicula_id}/cinemas", headers=Headers)
        respuesta.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    info_proyeccion: list = respuesta.json()

    return info_proyeccion


def get_cines(Headers: dict) -> list[dict]:

    try:
        respuesta = requests.get("http://vps-3701198-x.dattaweb.com:4000/cinemas", headers=Headers)
        respuesta.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    info_cines: list[dict] = respuesta.json()

    return info_cines


def get_pelis_en_cine(Headers: dict, cine_id: int) -> list[dict]:

    try:
        respuesta = requests.get(f"http://vps-3701198-x.dattaweb.com:4000/cinemas/{cine_id}/movies", headers=Headers)
        respuesta.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    info_pelis_en_cine: list[dict] = respuesta.json()

    return info_pelis_en_cine


def obtener_ubicaciones(cines: dict) -> list[str]:

    lista_ubicaciones: list[str] = []

    for cine in cines:
        if cine["location"] not in lista_ubicaciones:
            lista_ubicaciones.append(cine["location"])
    
    return lista_ubicaciones

def lista_poster_id(info_peliculas: dict) -> list[int]:

    poster_id = [diccionario["poster_id"] for diccionario in info_peliculas]
    print(poster_id)

    return poster_id


def onbutton_click(cine_id: int) -> int:

    #Hay que hacer que cambie de pagina a la pagina principal con todas las peliculas    
    print(cine_id)
    return cine_id

def crear_ventana_ubicaciones() -> None:
    ventana_ubicaciones = tk.Tk(className = "Cartelera")
    ventana_ubicaciones.geometry("500x500")

    return ventana_ubicaciones


def botones_ubicacion(ventana_ubicaciones, ubicaciones: list) -> None:
    
    for i,ubicacion in enumerate(ubicaciones):
        boton = tk.Button(ventana_ubicaciones, text=ubicacion, command=lambda e= i+1: onbutton_click(e))
        boton.grid(row=0, column=i)

def main() -> None:
    
    Headers = autorizacion()

    info_peliculas = get_peliculas(Headers)
    poster_id = lista_poster_id(info_peliculas)
    # info_pelicula_individual = get_pelicula_por_Id(Headers, pelicula_id)
    # img_poster = get_poster_por_Id(Headers, poster_id)
    info_snacks = get_snacks(Headers)
    # info_proyeccion = get_proyeccion(Headers, pelicula_id)
    info_cines = get_cines(Headers)
    ubicaciones = obtener_ubicaciones(info_cines)
    ventana_ubicaciones = crear_ventana_ubicaciones()
    botones_ubicacion(ventana_ubicaciones, ubicaciones)
    ventana_ubicaciones.mainloop()
    # info_pelis_en_cine = get_pelis_en_cine(Headers, cine_id)
    # lista_pelis_en_cine: list = [diccionario["has_movies"] for diccionario in info_pelis_en_cine]
    # print(info_pelis_en_cine)
    
main()