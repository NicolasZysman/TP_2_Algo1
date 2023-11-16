from tkinter import Frame, Button, Canvas, Tk

class CinemaListingsScreen:
    def __init__(self, master):

        # Creación de todos los contenedores principales
        top_left = Frame(master, bg='green', width=300, height=300)

        # Disposición de todos los contenedores principales
        top_left.grid(row=0, column=0, padx=0, pady=0)

        # Creación de botones
        top_left_button = Button(master, text='Ingresar ID', width=10, height=1, bd='10', command=root.destroy)
        top_middle_button = Button(master, text='Leer QR', width=10, height=1, bd='10', command=root.destroy)
        salir = Button(master, text='Salir', width=10, height=1, bd='10', command=root.destroy)


        top_left_button.place(x=50, y=80)
        top_middle_button.place(x=165, y=80)
        salir.place(x=110, y=160)

root = Tk()
root.title("App QR")
root.geometry("300x300")
display = CinemaListingsScreen(root)

root.mainloop()