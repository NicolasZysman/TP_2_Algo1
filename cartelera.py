import tkinter as tk
# import os
# import qrcode
import requests
from PIL import ImageTk,Image
import cv2
from io import BytesIO
import base64


API_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"


def autorizacion() -> dict:
    
    Headers: dict = { "Authorization" : f"Bearer {API_KEY}" }

    return Headers


def get_peliculas() -> list[dict]:

    header = autorizacion()

    try:
        respuesta = requests.get("http://vps-3701198-x.dattaweb.com:4000/movies", headers = header)
        respuesta.raise_for_status() # Esto es necesario para que tambien agarre los errores HTTP
    except requests.exceptions.RequestException as e:
        raise SystemExit(e) # Termina el programa y muestra el error
    
    info_peliculas: list[dict] = respuesta.json()

    return info_peliculas


def get_pelicula_por_Id(pelicula_id: int) -> dict:

    header = autorizacion()

    try:
        respuesta = requests.get(f"http://vps-3701198-x.dattaweb.com:4000/movies/{pelicula_id}", headers = header)
        respuesta.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    info_pelicula_individual: list[dict] = respuesta.json()

    return info_pelicula_individual


def get_poster_por_Id(poster_id: int) -> dict:

    header = autorizacion()

    try:
        respuesta = requests.get(f"http://vps-3701198-x.dattaweb.com:4000/posters/{poster_id}", headers = header)
        respuesta.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    img_poster: dict = respuesta.json()

    return img_poster


def lista_img_posters(posters: list) -> list:
    
    lista_dict_posters: list[dict] = []

    for poster_id in posters:
        lista_dict_posters.append(get_poster_por_Id(poster_id))
    
    lista_str_posters: list[str] = [diccionario["poster_image"] for diccionario in lista_dict_posters]
    
    return lista_str_posters


def get_snacks() -> dict:

    header = autorizacion()

    try:
        respuesta = requests.get(f"http://vps-3701198-x.dattaweb.com:4000/snacks", headers = header)
        respuesta.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    info_snacks: dict = respuesta.json()

    return info_snacks


def get_proyeccion(pelicula_id: int) -> list:

    header = autorizacion()

    try:
        respuesta = requests.get(f"http://vps-3701198-x.dattaweb.com:4000/movies/{pelicula_id}/cinemas", headers = header)
        respuesta.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    info_proyeccion: list = respuesta.json()

    return info_proyeccion


def get_cines() -> list[dict]:

    header = autorizacion()

    try:
        respuesta = requests.get("http://vps-3701198-x.dattaweb.com:4000/cinemas", headers = header)
        respuesta.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    info_cines: list[dict] = respuesta.json()

    return info_cines


def get_pelis_en_cine(cine_id: int) -> list[dict]:

    header = autorizacion()

    try:
        respuesta = requests.get(f"http://vps-3701198-x.dattaweb.com:4000/cinemas/{cine_id}/movies", headers = header)
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


def lista_poster_id(peliculas: list) -> list[int]:

    poster_id = [diccionario["poster_id"] for diccionario in peliculas]
    print(poster_id)

    return poster_id


def botones_ubicacion(ventana_ubicaciones, ubicaciones: list) -> None:
    
    for i,ubicacion in enumerate(ubicaciones):
        boton = tk.Button(ventana_ubicaciones, text=ubicacion, command=lambda e= i+1: onbutton_click(e))
        boton.grid(row=0, column=i)
    
    salir = tk.Button(ventana_ubicaciones, text = "Salir", command = ventana_ubicaciones.quit)
    salir.grid(row = 0, column = (i + 1))


def mostrar_posters(lista_posters: list, ventana_ubicaciones) -> None:

    for i, poster in enumerate(lista_posters):
        poster = (poster.replace('data:image/jpeg;base64,', ''))
        poster_bytes = base64.b64decode(poster)

        img = Image.open(BytesIO(poster_bytes))
        tk_imagen = ImageTk.PhotoImage(img)

        etiqueta = tk.Label(ventana_ubicaciones, image=tk_imagen)
        etiqueta.grid(row=i+1, column=0, padx=10, pady=10)
        etiqueta.image = tk_imagen 

        boton = tk.Button(ventana_ubicaciones, image=tk_imagen)
        boton.grid(row=3, column=2)


def crear_ventana_ubicaciones() -> None:

    ventana_ubicaciones = tk.Tk(className = "Cartelera")
    ventana_ubicaciones.geometry("500x500")

    return ventana_ubicaciones

# def obtener_id_poster_por_nombre(nombre_pelicula: str) -> str:

#     dict_peliculas: dict = get_peliculas()

#     for peli in dict_peliculas:
#         if nombre_pelicula == peli["name"]:
#             return peli["poster_id"]


def onbutton_click(cine_id: int) -> int:

    #Hay que hacer que cambie de pagina a la pagina principal con todas las peliculas   

    ventana_peliculas = tk.Toplevel()
    ventana_peliculas.geometry("1000x500")

    portada_1 = tk.Button(ventana_peliculas, text="Pelicula 1", width=50, borderwidth=5, command=ventana_peliculas.destroy)
    portada_1.pack()

    entrada_busqueda_peli = tk.Entry(ventana_peliculas)
    entrada_busqueda_peli.pack(pady = 10)
    retorno_busqueda_peli: str = entrada_busqueda_peli.get()

    # poster_id: str = obtener_id_poster_por_nombre(retorno_busqueda_peli)

    boton_busqueda = tk.Button(ventana_peliculas, text = "Buscar pelicula...") # command = lambda: mostrar_pelicula_en_cine(ventana_peliculas, cine_id, get_entry)
    boton_busqueda.pack()

    return cine_id


def main() -> None:

    info_peliculas = get_peliculas()
    # posters_id = lista_poster_id(info_peliculas)
    posters_id = [1, 2, 3, 4, 5, 9, 10, 14]

    lista_posters = lista_img_posters(posters_id)
    # info_pelicula_individual = get_pelicula_por_Id(Headers, pelicula_id)
    # img_poster = get_poster_por_Id(Headers, poster_id)

    info_snacks = get_snacks()
    # info_proyeccion = get_proyeccion(Headers, pelicula_id)

    info_cines = get_cines()
    ubicaciones = obtener_ubicaciones(info_cines)
    ventana_ubicaciones = crear_ventana_ubicaciones()

    botones_ubicacion(ventana_ubicaciones, ubicaciones)

    mostrar_posters(lista_posters, ventana_ubicaciones)

    ventana_ubicaciones.mainloop()
    # info_pelis_en_cine = get_pelis_en_cine(Headers, cine_id)
    # lista_pelis_en_cine: list = [diccionario["has_movies"] for diccionario in info_pelis_en_cine]
    # print(info_pelis_en_cine)
    
main()
