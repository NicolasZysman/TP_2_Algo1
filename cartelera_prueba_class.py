import tkinter as tk
from tkinter import messagebox
# import os
import qrcode
import requests
from PIL import ImageTk,Image
import cv2
from io import BytesIO
import base64
from datetime import datetime
from random import randint


API_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"
INDICE_CANTIDAD_ENTRADAS: int = 0
INDICE_VALOR_UNITARIO: int = 1

def autorizacion() -> dict:
    '''
    Pre: XXX
    Post: Devuelve un diccionario con la key de la api
    '''
    
    Headers: dict = { "Authorization" : f"Bearer {API_KEY}" }

    return Headers


def get_peliculas() -> list[dict]:
    '''
    Pre: XXX
    Post: Devuelve una lista de diccionarios con la info 
          del endpoint /movies
    '''

    header = autorizacion()

    try:
        respuesta = requests.get("http://vps-3701198-x.dattaweb.com:4000/movies", headers = header)
        respuesta.raise_for_status() # Esto es necesario para que tambien agarre los errores HTTP
    except requests.exceptions.RequestException as e:
        raise SystemExit(e) # Termina el programa y muestra el error
    
    info_peliculas: list[dict] = respuesta.json()

    return info_peliculas


def get_pelicula_por_Id(pelicula_id: int) -> list[dict]:
    '''
    Pre: Recibe un int del id de pelicula
    Post: Devuelve una lista de diccionarios con la info 
          del endpoint /movies/pelicula_id
    '''

    header = autorizacion()

    try:
        respuesta = requests.get(f"http://vps-3701198-x.dattaweb.com:4000/movies/{pelicula_id}", headers = header)
        respuesta.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    info_pelicula_individual: list[dict] = respuesta.json()

    return info_pelicula_individual


def get_poster_por_Id(poster_id: int) -> dict:
    '''
    Pre: Recibe un int del id del poster
    Post: Devuelve un diccionario con la info
          del endpoint /posters/poster_id
    '''

    header = autorizacion()

    try:
        respuesta = requests.get(f"http://vps-3701198-x.dattaweb.com:4000/posters/{poster_id}", headers = header)
        respuesta.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    img_poster: dict = respuesta.json()

    return img_poster


def get_snacks() -> dict:
    '''
    Pre: XXX
    Post: Devuelve un diccionario con la info
          del endpoint /snacks
    '''

    header = autorizacion()

    try:
        respuesta = requests.get(f"http://vps-3701198-x.dattaweb.com:4000/snacks", headers = header)
        respuesta.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    info_snacks: dict = respuesta.json()

    return info_snacks


def get_proyeccion(pelicula_id: int) -> list:
    '''
    Pre: Recibe un int del id de pelicula
    Post: Devuelve una lista con la info 
          del endpoint /movies/pelicula_id/cinemas  
          (donde se proyecta cada pelicula)  
    '''

    header = autorizacion()

    try:
        respuesta = requests.get(f"http://vps-3701198-x.dattaweb.com:4000/movies/{pelicula_id}/cinemas", headers = header)
        respuesta.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    info_proyeccion: list = respuesta.json()

    return info_proyeccion


def get_cines() -> list[dict]:
    '''
    Pre: XXX
    Post: Devuelve una lista de diccionarios con la info
          del endpoint /cinemas
    '''

    header = autorizacion()

    try:
        respuesta = requests.get("http://vps-3701198-x.dattaweb.com:4000/cinemas", headers = header)
        respuesta.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    info_cines: list[dict] = respuesta.json()

    return info_cines


def get_pelis_en_cine(cine_id: int) -> list[dict]:
    '''
    Pre: Recibe un int del id de cine
    Post: Devuelve una lista de diccionarios con la info
          del endpoint /cinemas/movies_id/movies
    '''


    header = autorizacion()

    try:
        respuesta = requests.get(f"http://vps-3701198-x.dattaweb.com:4000/cinemas/{cine_id}/movies", headers = header)
        respuesta.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    info_pelis_en_cine: list[dict] = respuesta.json()

    return info_pelis_en_cine


def lista_poster_id(peliculas: list) -> list[int]:
    '''
    Pre: Recibe una lista de peliculas
    Post: Devuelve una lista con los id de los posters
    '''

    posters_id = []

    for pelicula in peliculas:
        
        info_pelicula = get_pelicula_por_Id(pelicula)
        posters_id.append(info_pelicula["poster_id"])
    
    return posters_id


def lista_img_posters(posters: list) -> list:
    '''
    Pre: Recibe una lista de posters
    Post: Devuelve una lista con la imagen de cada pelicula
    '''
    
    lista_dict_posters: list[dict] = []

    for poster_id in posters:
        lista_dict_posters.append(get_poster_por_Id(poster_id))
    
    lista_str_posters: list[str] = [diccionario["poster_image"] for diccionario in lista_dict_posters]
    
    return lista_str_posters


def obtener_ubicaciones(cines: dict) -> list[str]:
    '''
    Pre: Recibe un diccionario con la info de cines
    Post: Devuelve una lista con las ubicaciones
    '''

    lista_ubicaciones: list[str] = []

    for cine in cines:
        if cine["location"] not in lista_ubicaciones:
            lista_ubicaciones.append(cine["location"])
    
    return lista_ubicaciones


def id_pelis_en_cine(cine_id: int) -> list:
    '''
    Pre: Recibe una int de cine_id
    Post: Devuelve una lista con los id de las peliculas
          disponibles en la ubicacion actual
    '''
    
    pelis_en_cine = get_pelis_en_cine(cine_id)

    for diccionario in pelis_en_cine:
        lista_pelis_en_cine = diccionario["has_movies"]

    return lista_pelis_en_cine


def convertir_imagen(poster: str):
    '''
    Pre: Recibe una str de poster
    Post: Devuelve una imagen en formato legible para tkinter
    '''

    poster = (poster.replace('data:image/jpeg;base64,', ''))
    poster_bytes = base64.b64decode(poster)

    img = Image.open(BytesIO(poster_bytes))
    tk_imagen = ImageTk.PhotoImage(img)

    return tk_imagen


def obtener_ubicaciones_pelicula(info_proyeccion: list, ubicaciones: list[str]) -> list:
    '''
    Pre: Recibe una lista de info_proyeccion y una lista con ubicaciones
    Post: Devuelve una lista con los cines donde se proyecta la pelicula
    '''
    
    peli_en_cine = []
        
    for cine in info_proyeccion:
        int_cine = int(cine)
        nombre_cine = ubicaciones[int_cine - 1]
        peli_en_cine.append(nombre_cine)

    return peli_en_cine


def suma_total(acumulador_precios: list) -> float:
    precio_total: float = 0
    contador_entradas: int = 0
    cantidad_entradas: int = 0
    precio_unitario: int = 0
    precio_entradas: int = 0

    for gasto in acumulador_precios:

        if contador_entradas == 0:
            cantidad_entradas = int(gasto)
            contador_entradas += 1

        elif contador_entradas == 1:
            precio_unitario = int(gasto)

            precio_entradas = cantidad_entradas * precio_unitario
            precio_total += float(precio_entradas)
            contador_entradas += 1

        else:       
            precio_total += float(gasto)

    return precio_total

def cantidad_snacks_elegidos(acumulador_precios: list, info_snacks: dict) -> dict:
    snacks: dict = {}

    for elemento in range(len(acumulador_precios)):

        if elemento != INDICE_CANTIDAD_ENTRADAS or elemento != INDICE_VALOR_UNITARIO:
            contador: int = 0
            for precio in acumulador_precios:

                if precio == acumulador_precios[elemento]:
                    contador += 1

            if contador != 0:

                for snack, valor in info_snacks.items():
                    if valor == acumulador_precios[elemento]:

                        snacks[snack] = contador
            
    return snacks


def mostrar_compra(acumulador_precios: list, info_snacks: dict) -> dict:
    compra: dict = {}

    compra["Cantidad entradas"] = acumulador_precios[INDICE_CANTIDAD_ENTRADAS]
    compra["Valor unitario"] = acumulador_precios[INDICE_VALOR_UNITARIO]

    snacks: dict = cantidad_snacks_elegidos(acumulador_precios, info_snacks)
    compra["Snacks"] = snacks   

    precio_total: float = suma_total(acumulador_precios)
    compra["Precio Total"] = precio_total

    return compra


def imprimir_snacks(self, info_snacks: dict, acumulador_precios: list) -> None:
    '''
    Pre: Recibe la ventana actual, un diccionario con la info de snacks
         y una lista de precios
    Post: Agrega el valor del snack seleccionado a acumulador_precios
    '''

    iterador_fila: int = 4
    
    for snack, valor in info_snacks.items():
        
        iterador_columna: int = 0

        mostrar_snack = tk.Label(self, text=snack)
        mostrar_valor = tk.Button(self, text="Pagar " + valor, command = lambda i = valor: [acumulador_precios.append(i), contador(self, i, acumulador_precios)])
        restar_snack = tk.Button(self, text="-", command=lambda i=valor, snack=snack: [restar(i, acumulador_precios, snack), contador(self, i, acumulador_precios)])
        # sumar_carrito = tk.Button(self, text="+")

        mostrar_snack.grid(row=iterador_fila, column=iterador_columna)
        iterador_columna += 1

        mostrar_valor.grid(row=iterador_fila, column=iterador_columna)
        iterador_columna += 1

        restar_snack.grid(row=iterador_fila, column=iterador_columna)
        iterador_columna += 1

        # sumar_carrito.grid(row=iterador_fila, column=iterador_columna)
        # iterador_columna += 1

        iterador_fila += 1


def contador(self, i, acumulador_precios):

    cantidad_snack = acumulador_precios.count(i)
    tk.Label(self, text=cantidad_snack).grid()

def restar(i, acumulador_precios, snack):

    if i in acumulador_precios:
        acumulador_precios.remove(i)
    else:
        messagebox.showerror("Error", f"No seleccionaste {snack} todavia")


def añadir_botones_reserva(self, controller, 
                           cine_id: int, peli_id: int, acumulador_precios: list) -> None:
    '''
    Pre: Recibe la ventana actual, el controller, un int de cine_id,
    un int de peli_id y una lista de precios
    Post: Da la opcion de agregar los snacks y el boton de carrito
    que cambia de ventana al carrito
    '''
    
    añadir_sanck = tk.Button(self, text="Añadir Snack", bg="orange", command = lambda: imprimir_snacks(self, info_snacks, acumulador_precios))
    añadir_sanck.grid(row=3, column=0)

    info_snacks: dict = get_snacks()
    agregar = tk.Button(
        self, 
        text="Añadir al carro", 
        bg="green" , 
        command = lambda: controller.show_frame(Carrito, cine_id, peli_id, mostrar_compra(acumulador_precios, info_snacks)) 
    )

    agregar.grid(row=11, column=1)


def ingresar_valor_unitario(self, controller, cine_id, peli_id, acumulador_precios: list):
    
    etiqueta_2 = tk.Label(self, text="Valor unitario por entrada")
    etiqueta_2.grid(row=0, column=1)
    
    validacion = (self.register(validar_mensaje), "%P")
    ingresar_valor = tk.Entry(self, width=35, borderwidth=2, validate = "key", validatecommand = validacion)
    ingresar_valor.grid(row=1, column=1)

    self.precio_total: float = tk.DoubleVar()
    boton_random2 = tk.Button(
            self, 
            text="Ingresar", 
            command = lambda: [
                acumulador_precios.append(ingresar_valor.get()),
                añadir_botones_reserva(self, controller, cine_id, peli_id, acumulador_precios)
            ]
        )
    
    boton_random2.grid(row=2, column=1)

    return self.precio_total.get()


def filtrar_busqueda(ventana, get_entry: str, 
        controller, lista_pelis_en_cine: list, cine_id: int) -> None:
    '''
    Pre: Recibe la ventana actual, el nombre de la peli que busca
    el usuario, el controller, las pelis en el cine actual y un int de 
    cine_id
    Post: busca si la pelicula esta en el cine, si no esta lo indica,
    si esta muestra la/las pelis con ese nombre
    '''

    peliculas_totales = get_peliculas()

    nombre_pelis = []
    pelis_encontradas = []
    poster_id = []
    id_peliculas = []

    for peli in peliculas_totales:
        if peli["movie_id"] in lista_pelis_en_cine:
            nombre_pelis.append(peli["name"])

    for titulo in nombre_pelis:
        if get_entry.upper() in titulo:
            pelis_encontradas.append(titulo)
    
    for pelicula in peliculas_totales:
        if pelicula["name"] in pelis_encontradas:
            poster_id.append(pelicula["poster_id"])
            id_peliculas.append(pelicula["movie_id"])


    if len(pelis_encontradas) == 0:
        tk.Label(ventana, text= "No se encuentra la pelicula en este cine").pack(pady = 10)
        
    lista_posters = lista_img_posters(poster_id)

    posters_busqueda(ventana, lista_posters, 
                     id_peliculas, controller, cine_id)


def posters_cartelera(ventana, lista_posters: list[str], 
                      lista_pelis_en_cine: list[int], controller, cine_id: int) -> None:
    '''
    Pre: Recibe la ventana actual, una lista de posters, una
    lista de pelis en cine, el controller u un int de cine_id
    Post: Recorre la lista de posters y los muestra como botones.
    si se apreta un poster te lleva a su ventana con su info
    '''

    columna = 1
    fila = 9

    for i, poster in enumerate(lista_posters):

            tk_imagen = convertir_imagen(poster)

            etiqueta = tk.Label(ventana, image=tk_imagen)
            etiqueta.grid(row=fila, column = columna, pady = 10)
            etiqueta.image = tk_imagen 

            boton = tk.Button(
                ventana, 
                image=tk_imagen, 
                command = lambda i=i: controller.show_frame(Pelicula, cine_id, encontrar_peli_id(i, lista_pelis_en_cine))
            )
            boton.grid(row=fila, column = columna, pady = 10)

            if columna == 4:
                fila += 1

            if columna == 1:
                columna = 4
            else:
                columna = 1
            # boton.grid(row=3, column=2)


def posters_busqueda(ventana, lista_posters: list[str], 
                     id_peliculas: list[int], controller, cine_id: int) -> None:
    '''
    Pre: Recibe la ventana actual, una lista de posters, una
    lista de id de pelis en cine, el controller u un int de cine_id
    Post: Recorre la lista de posters y los muestra como botones.
    si se apreta un poster te lleva a su ventana con su info
    '''

    for i, poster in enumerate(lista_posters):

            tk_imagen = convertir_imagen(poster)

            etiqueta = tk.Label(ventana, image=tk_imagen)
            # etiqueta.grid(row=i+1, column=0, padx=10, pady=10)
            etiqueta.image = tk_imagen 

            boton = tk.Button(
                ventana, 
                image=tk_imagen, 
                command = lambda boton_apretado=i: controller.show_frame(Pelicula, cine_id, encontrar_peli_id(boton_apretado, id_peliculas))
            )
            boton.pack()
            # boton.grid(row=3, column=2)


def encontrar_peli_id(i, lista_pelis_en_cine) -> int:
    '''
    Pre: Recibe un int de boton_apretado y una lista
    de id de pelis en cine
    Post: Devuelve el id de pelicula
    '''
    
    peli_id = lista_pelis_en_cine[i]
    return peli_id

def validar_mensaje(texto: str) -> bool:
    validacion: bool = False
    if texto.isnumeric() == True or texto == "":
        validacion = True
    else:
        messagebox.showerror("Error", "Por favor, ingrese solo números enteros.")

    return validacion

class ventanas(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Cinepolis")  
        self.geometry("1000x1000")

        self.container = tk.Frame(self, height=500, width=500)
        self.container.pack(side="top", fill="both", expand=True)
        
        self.frames: dict = {}
        
        clase_frames = {
            Ubicacion: Ubicacion,
            Cartelera: Cartelera,
            Pelicula: Pelicula,
            Reserva: Reserva,
            Busqueda: Busqueda,
            Carrito: Carrito
        }
        
        for F in clase_frames:
            self.frames[F] = None

        self.show_frame(Ubicacion)

    def show_frame(self, clase, *args):
        '''
        Pre: Recibe la clase y uno o multiples
        argumentos
        Post: Si la clase no se creo la crea, y
        si ya fue creada cambia de ventana 
        '''

        frame = self.frames[clase]
        
        if frame == None:
            
            frame = clase(self.container, self, *args)
            frame.grid(row=0, column=0, sticky="nsew")
        
        else:
            frame.tkraise(*args)


class Ubicacion(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)

        cant_columnas: int = 7

        for col in range(cant_columnas):
            self.grid_columnconfigure(col, weight=1, minsize = 142)

        info_cines: list[dict] = get_cines()
        ubicaciones: list[str] = obtener_ubicaciones(info_cines)

        for i,ubicacion in enumerate(ubicaciones):
                
                boton = tk.Button(
                    self,
                    text=ubicacion,
                    command = lambda cine_id=i + 1: controller.show_frame(Cartelera, cine_id)
                )
                boton.grid(row=0, column=i, padx = 5, sticky="nsew")
    

class Busqueda(tk.Frame):

    def __init__(self, parent, 
                 controller, cine_id: int, lista_pelis_en_cine: list[int]):
    
        tk.Frame.__init__(self, parent)

        titulo = tk.Label(self, text="Ingrese pelicula...")
        titulo.pack(pady = 10)

        self.cine_id: int = cine_id
        self.lista_pelis_en_cine: list[int] = lista_pelis_en_cine


        entrada_busqueda_peli = tk.Entry(self)
        entrada_busqueda_peli.pack(pady = 10)

        boton_busqueda = tk.Button(self, text = "Enter", command = lambda: [filtrar_busqueda(self, entrada_busqueda_peli.get(), controller, lista_pelis_en_cine, self.cine_id)])
        boton_busqueda.pack()
        
        boton_volver = tk.Button(self, text="Volver a Cartelera", command = lambda: controller.show_frame(Cartelera, cine_id))
        boton_volver.pack()


class Cartelera(tk.Frame):
    
    def __init__(self, parent, 
                 controller, cine_id: int):
        
        tk.Frame.__init__(self, parent)

        # Crear canvas
        canvas = tk.Canvas(self, height=1000, width=980) # width = el ancho de la ventana - 20px de scrollbar
        canvas.pack(side="left", fill="both", expand=True)

        # Agregar scrollbar al canvas
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y", expand=True)

        # Configuracion canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

        # Crear frame en el canvas
        segundo_frame = tk.Frame(canvas, bg="green")

        # Agregar el segundo frame a una ventana en el canvas
        canvas.create_window((0,0), window=segundo_frame, anchor="nw")

        cant_columnas: int = 8

        for col in range(cant_columnas):
            segundo_frame.grid_columnconfigure(col, weight=1, minsize = 125)
            

        self.cine_id: int = cine_id
        info_cines: list[dict] = get_cines()
        lista_pelis_en_cine: list[int] = id_pelis_en_cine(self.cine_id)
        posters_id: list[int] = lista_poster_id(lista_pelis_en_cine)
        lista_posters: list[str] = lista_img_posters(posters_id)

        ubicacion: str = info_cines[self.cine_id - 1]["location"]
        tk.Label(segundo_frame, text=ubicacion).grid(row = 0 , column = 2, columnspan = 2, pady = 10)

        boton_busqueda = tk.Button(segundo_frame, text = "Buscar pelicula...", 
                                   command = lambda: controller.show_frame(Busqueda, cine_id, lista_pelis_en_cine))
        boton_busqueda.grid(row = 1, column = 2, columnspan= 2)

        posters_cartelera(segundo_frame, lista_posters, 
                          lista_pelis_en_cine, controller, self.cine_id)

    def actualizar_cine_id(self, cine_id):
        self.cine_id = cine_id


class Pelicula(tk.Frame):

    def __init__(self, parent, 
                 controller, cine_id: int, peli_id: int):
        
        tk.Frame.__init__(self, parent)

        self.peli_id: int = peli_id
        self.cine_id: int = cine_id
        info_peli: list[dict] = get_pelicula_por_Id(peli_id)
        info_cines: list[dict] = get_cines()
        info_proyeccion: list = get_proyeccion(peli_id)
        ubicaciones: list[str] = obtener_ubicaciones(info_cines)

        peli_en_cine: list[str] = obtener_ubicaciones_pelicula(info_proyeccion, ubicaciones)

        poster_id: int = info_peli["poster_id"]
        dict_poster: dict = get_poster_por_Id(poster_id)
        poster: str = dict_poster["poster_image"]
        tk_imagen = convertir_imagen(poster)


        etiqueta = tk.Label(self, image=tk_imagen)
        etiqueta.image = tk_imagen 
        etiqueta.pack()

        nombre: str = info_peli["name"]
        tk.Label(self, text=nombre).pack()

        # sinopsis = info_peli["synopsis"] Da error no se porque
        # tk.Label(self, text=sinopsis).pack()

        genero: str = info_peli["gender"]
        tk.Label(self, text=genero).pack()

        duracion: int = info_peli["duration"]
        tk.Label(self, text=duracion).pack()
        
        actores: str = info_peli["actors"]
        tk.Label(self, text=actores).pack()

        director: str = info_peli["directors"]
        tk.Label(self, text=director).pack()

        pg_rating: int = info_peli["rating"]
        tk.Label(self, text=pg_rating).pack()

        #con el id de la pelicula traer el id de los cines donde se proyecta
        #con los ids meterlos en una lista y mostrarlos
        tk.Label(self, text=peli_en_cine).pack()

        asientos: int = info_cines[cine_id - 1]["available_seats"]
        
        if(asientos > 0):

            boton_reserva = tk.Button(self, text="Reservar", bg="green", 
                                      command = lambda: controller.show_frame(Reserva, cine_id, peli_id))
            boton_reserva.pack()
        else:
            tk.Label(self, text="No hay asientos disponibles", bg="red").pack()

        
        boton_volver = tk.Button(self, text="Volver", 
                                 command = lambda: controller.show_frame(Cartelera, cine_id))
        boton_volver.pack()

    def actualizar_cine_id(self, cine_id):
        self.cine_id = cine_id


class Reserva(tk.Frame):
    
    def __init__(self, parent, 
                 controller, cine_id: int, peli_id: int):
        
        tk.Frame.__init__(self, parent)

        self.cine_id: int = cine_id
        self.peli_id: int = peli_id

        acumulador_precios: list = []

        etiqueta_1 = tk.Label(self, text="Ingrese la cantidad de entradas")
        etiqueta_1.grid(row=0, column=0)

        validacion = (self.register(validar_mensaje), "%P")

        seleccionar_cantidad_entradas = tk.Entry(self, width=35, borderwidth=2, validate = "key", validatecommand = validacion)
        seleccionar_cantidad_entradas.grid(row=1, column=0)

        boton_random1 = tk.Button(
            self, 
            text="Ingresar", 
            command = lambda: [
                acumulador_precios.append(seleccionar_cantidad_entradas.get()),
                ingresar_valor_unitario(self, controller, cine_id, peli_id, acumulador_precios)
                ]
        )

        boton_random1.grid(row=2, column=0)

        boton_volver = tk.Button(self, text="Volver", bg="red", 
                                 command = lambda: controller.show_frame(Pelicula, cine_id, peli_id))
        boton_volver.grid(row=11, column=0)

    def actualizar_cine_id(self, cine_id):
        self.cine_id = cine_id


class Carrito(tk.Frame):

    def __init__(self, parent,
                 controller, cine_id, peli_id, precios):
        
        tk.Frame.__init__(self, parent)

        self.cine_id: int = cine_id
        self.peli_id: int = peli_id
        self.precios = precios

        info_peli = get_pelicula_por_Id(self.peli_id)
        nombre: str = info_peli["name"]

        info_cines: list[dict] = get_cines()
        ubicacion: str = info_cines[self.cine_id - 1]["location"]

        cantidad_entradas = precios["Cantidad entradas"]

        tk.Label(self, text=self.cine_id).pack()
        tk.Label(self, text=self.peli_id).pack()
        tk.Label(self, text=self.precios).pack()

        tk.Label(self, bg="red").pack()

        boton_qr = tk.Button(self, text="Finalizar Compra", 
                             command = lambda: [self.generar_qr(nombre, ubicacion, cantidad_entradas), 
                                                controller.show_frame(Cartelera, cine_id)])
        boton_qr.pack()

        # precios = {
        #     'Cantidad entradas': 2,
        #     'Valor unitario': 100,
        #     'Snacks': {
        #         'doritos': 3,
        #         'popcorn_xl': 1
        #     },
        #     'Precio total': 10700
        # }

    def generar_qr(self, nombre: str, ubicacion: str, cantidad_entradas: int) -> None:
        random_id = randint(1, 5000)
        dt = datetime.now()
        raw_data = (f"{random_id}_{nombre}_{ubicacion}_{cantidad_entradas}{dt}")
        data = raw_data.replace(" ", "")
        img = qrcode.make(data)
        img.save(f"QR/Qr{random_id}.png")

def main():     
    app = ventanas()
    app.mainloop()


main()
