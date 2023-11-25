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

# def obtener_id_poster_por_nombre(nombre_pelicula: str) -> str:

#     dict_peliculas: dict = get_peliculas()

#     for peli in dict_peliculas:
#         if nombre_pelicula == peli["name"]:
#             return peli["poster_id"]

def id_pelis_en_cine(cine_id) -> list:
    
    
    pelis_en_cine = get_pelis_en_cine(cine_id)

    for diccionario in pelis_en_cine:
        lista_pelis_en_cine = diccionario["has_movies"]

    return lista_pelis_en_cine


def lista_poster_id(peliculas: list) -> list[int]:

    posters_id = []

    for pelicula in peliculas:
        
        info_pelicula = get_pelicula_por_Id(pelicula)
        posters_id.append(info_pelicula["poster_id"])
    
    return posters_id


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


def convertir_imagen(poster):

    poster = (poster.replace('data:image/jpeg;base64,', ''))
    poster_bytes = base64.b64decode(poster)

    img = Image.open(BytesIO(poster_bytes))
    tk_imagen = ImageTk.PhotoImage(img)

    return tk_imagen


def obtener_ubicaciones_pelicula(info_proyeccion: list, ubicaciones: list[str]) -> list:
    
    peli_en_cine = []
        
    for cine in info_proyeccion:
        int_cine = int(cine)
        nombre_cine = ubicaciones[int_cine - 1]
        peli_en_cine.append(nombre_cine)

    return peli_en_cine

def suma_total(acumulador_precios: list):
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

    print("Tenes que pagar ", precio_total, " pesos")

def imprimir_snacks(self, info_snacks: dict, acumulador_precios: list):
    iterador_fila: int = 4
    for snack, valor in info_snacks.items():
        iterador_columna: int = 0

        mostrar_snack = tk.Label(self, text=snack)
        mostrar_valor = tk.Button(self, text="Pagar " + valor, command = lambda i = valor: acumulador_precios.append(i))
        # sumar_carrito = tk.Button(self, text="+")

        mostrar_snack.grid(row=iterador_fila, column=iterador_columna)
        iterador_columna += 1

        mostrar_valor.grid(row=iterador_fila, column=iterador_columna)
        iterador_columna += 1

        # sumar_carrito.grid(row=iterador_fila, column=iterador_columna)
        # iterador_columna += 1

        iterador_fila += 1

def añadir_botones_reserva(self, acumulador_precios: list):
    añadir_sanck = tk.Button(self, text="Añadir Snack", bg="orange", command = lambda: imprimir_snacks(self, info_snacks, acumulador_precios))
    añadir_sanck.grid(row=3, column=0)

    info_snacks: dict = get_snacks()

    agregar = tk.Button(
        self, 
        text="Añadir al carro", 
        bg="green" , 
        command = lambda: suma_total(acumulador_precios)
    )

    agregar.grid(row=11, column=1)

def ingresar_valor_unitario(self, acumulador_precios: list):
    etiqueta_2 = tk.Label(self, text="Valor unitario por entrada")
    etiqueta_2.grid(row=0, column=1)
    
    ingresar_valor = tk.Entry(self, width=35, borderwidth=2)
    ingresar_valor.grid(row=1, column=1)

    boton_random2 = tk.Button(
            self, 
            text="Ingresar", 
            command = lambda: [
                acumulador_precios.append(ingresar_valor.get()),
                añadir_botones_reserva(self, acumulador_precios)
            ]
        )
    
    boton_random2.grid(row=2, column=1)

class ventanas(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Cinepolis")
        """
        # self.geometry("500x500")

        # self.container = tk.Frame(self, height=500, width=500)
        # self.container.pack(side="top", fill="both", expand=True)
        

        # self.frames: dict = {}
        
    #     for F in (Ubicacion, Cartelera, Pelicula, Reserva):

    #         frame = F(container, self)
    #         self.frames[F] = frame
    #         frame.grid(row=0, column=0, sticky="nsew")

    #     self.show_frame(Ubicacion)

    # def show_frame(self, cont, cine_id=None):
    #     frame = self.frames[cont]
    
    #     if cont == Cartelera and cine_id is not None:
    #             frame.update_cine_id(cine_id)
    
    #     frame.tkraise()
        """
        
        self.geometry("500x500")

        self.container = tk.Frame(self, height=500, width=500)
        self.container.pack(side="top", fill="both", expand=True)
        
        self.frames: dict = {}
        
        clase_frames = {
            Ubicacion: Ubicacion,
            Cartelera: Cartelera,
            Pelicula: Pelicula,
            Reserva: Reserva
        }
        
        for F in clase_frames:
            self.frames[F] = None

        self.show_frame(Ubicacion)

    def show_frame(self, clase, *args):
        frame = self.frames[clase]
        if frame == None:
            frame = clase(self.container, self, *args)
            frame.grid(row=0, column=0, sticky="nsew")
        else:
            frame.tkraise(*args)


class Ubicacion(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)

        info_cines = get_cines()
        ubicaciones = obtener_ubicaciones(info_cines)

        for i,ubicacion in enumerate(ubicaciones):
                
                boton = tk.Button(
                    self,
                    text=ubicacion,
                    command = lambda cine_id=i + 1: controller.show_frame(Cartelera, cine_id)
                )
                boton.grid(row=0, column=i)
    


def posters_cartelera(ventana, lista_posters, controller, cine_id):

    for _, poster in enumerate(lista_posters):

            tk_imagen = convertir_imagen(poster)

            etiqueta = tk.Label(ventana, image=tk_imagen)
            # etiqueta.grid(row=i+1, column=0, padx=10, pady=10)
            etiqueta.image = tk_imagen 

            boton = tk.Button(
                ventana, 
                image=tk_imagen, 
                command = lambda: controller.show_frame(Pelicula, cine_id)
            )
            boton.pack()
            # boton.grid(row=3, column=2)


def filtrar_busqueda(get_entry, posters_id):

    peliculas_totales = get_peliculas()
    posters_id = []
    for p in peliculas_totales:
        if get_entry == p["name"]:
            posters_id.append(p["poster_id"])

    # print(posters_id)
    return posters_id


class Cartelera(tk.Frame):
    
    def __init__(self, parent, controller, cine_id):
        
        tk.Frame.__init__(self, parent)

       
        
        self.cine_id = cine_id
        info_cines = get_cines()
        lista_pelis_en_cine = id_pelis_en_cine(self.cine_id)
        posters_id = lista_poster_id(lista_pelis_en_cine)
        lista_posters = lista_img_posters(posters_id)

        ubicacion = info_cines[self.cine_id - 1]["location"]
        tk.Label(self, text=ubicacion).pack()

        entrada_busqueda_peli = tk.Entry(self)
        entrada_busqueda_peli.pack(pady = 10)

        # poster_id: str = obtener_id_poster_por_nombre(retorno_busqueda_peli)

        boton_busqueda = tk.Button(self, text = "Buscar pelicula...", command = lambda: filtrar_busqueda(entrada_busqueda_peli.get(), posters_id)) # command = lambda: filtrar_busqueda(ventana_peliculas, cine_id, get_entry)
        boton_busqueda.pack()

        posters_cartelera(self, lista_posters, controller, self.cine_id)

    def actualizar_cine_id(self, cine_id):
        self.cine_id = cine_id



class Pelicula(tk.Frame):

    def __init__(self, parent, controller, cine_id):
        
        tk.Frame.__init__(self, parent)

        peli_id = 8
        self.cine_id = cine_id
        info_peli = get_pelicula_por_Id(peli_id)
        info_cines = get_cines()
        info_proyeccion = get_proyeccion(peli_id)
        ubicaciones = obtener_ubicaciones(info_cines)

        peli_en_cine = obtener_ubicaciones_pelicula(info_proyeccion, ubicaciones)

        poster_id = info_peli["poster_id"]
        dict_poster = get_poster_por_Id(poster_id)
        poster = dict_poster["poster_image"]
        tk_imagen = convertir_imagen(poster)


        etiqueta = tk.Label(self, image=tk_imagen)
        etiqueta.image = tk_imagen 
        etiqueta.pack()

        nombre = info_peli["name"]
        tk.Label(self, text=nombre).pack()

        # sinopsis = info_peli["synopsis"] Da error no se porque
        # tk.Label(self, text=sinopsis).pack()

        genero = info_peli["gender"]
        tk.Label(self, text=genero).pack()

        duracion = info_peli["duration"]
        tk.Label(self, text=duracion).pack()
        
        actores = info_peli["actors"]
        tk.Label(self, text=actores).pack()

        director = info_peli["directors"]
        tk.Label(self, text=director).pack()

        pg_rating = info_peli["rating"]
        tk.Label(self, text=pg_rating).pack()

        #con el id de la pelicula traer el id de los cines donde se proyecta
        #con los ids meterlos en una lista y mostrarlos
        tk.Label(self, text=peli_en_cine).pack()

        asientos = info_cines[cine_id - 1]["available_seats"]
        
        if(asientos > 0):

            boton_reserva = tk.Button(self, text="Reservar", bg="green", command = lambda: controller.show_frame(Reserva, cine_id))
            boton_reserva.pack()
        else:
            tk.Label(self, text="No hay asientos disponibles", bg="red").pack()

        
        boton_volver = tk.Button(self, text="Volver", command = lambda: controller.show_frame(Cartelera, cine_id))
        boton_volver.pack()

    def actualizar_cine_id(self, cine_id):
        self.cine_id = cine_id

class Reserva(tk.Frame):
    
    def __init__(self, parent, controller, cine_id):
        
        tk.Frame.__init__(self, parent)

        self.cine_id = cine_id

        acumulador_precios: list = []

        etiqueta_1 = tk.Label(self, text="Ingrese la cantidad de entradas")
        etiqueta_1.grid(row=0, column=0)

        seleccionar_cantidad_entradas = tk.Entry(self, width=35, borderwidth=2)
        seleccionar_cantidad_entradas.grid(row=1, column=0)

        boton_random1 = tk.Button(
            self, 
            text="Ingresar", 
            command = lambda: [
                acumulador_precios.append(seleccionar_cantidad_entradas.get()),
                ingresar_valor_unitario(self, acumulador_precios)]
        )

        boton_random1.grid(row=2, column=0)

        boton_volver = tk.Button(self, text="Volver", bg="red", command = lambda: controller.show_frame(Pelicula, cine_id))
        boton_volver.grid(row=11, column=0)

    def actualizar_cine_id(self, cine_id):
        self.cine_id = cine_id


def main():     
    app = ventanas()
    app.mainloop()


main()
