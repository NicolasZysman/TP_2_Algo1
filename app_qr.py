import tkinter as tk

class windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Adding a title to the window
        self.wm_title("App QR")
        self.geometry("300x300")

        # creating a frame and assigning it to container
        container = tk.Frame(self, height=300, width=300)
        # specifying the region where the frame is packed in root
        container.pack(side="top", fill="both", expand=True)

        # configuring the location of the container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # We will now create a dictionary of frames
        self.frames = {}
        # we'll create the frames themselves later but let's add the components to the dictionary.
        for F in (MainPage, SidePage, SidePage1):
            frame = F(container, self)

            # the windows class acts as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Using a method to switch frames
        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        # raises the current frame to the top
        frame.tkraise()


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Menu principal")
        label.pack(padx=10, pady=10)

        # We use the switch_window_button in order to call the show_frame() method as a lambda function
        salir = tk.Button(
            self,
            text="Salir",
            command=controller.destroy
        )
        salir.pack(side="bottom", fill=tk.X)

        switch_window_button1 = tk.Button(
            self,
            text="Leer QR",
            command=lambda: controller.show_frame(SidePage1),
        )
        switch_window_button1.pack(side="bottom", fill=tk.X)

        switch_window_button2 = tk.Button(
            self,
            text="Ingresar ID",
            command=lambda: controller.show_frame(SidePage),
        )
        switch_window_button2.pack(side="bottom", fill=tk.X)


class SidePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Ingresar ID")
        label.pack(padx=10, pady=10)

        switch_window_button = tk.Button(
            self,
            text="Volver al menu",
            command=lambda: controller.show_frame(MainPage),
        )
        switch_window_button.pack(side="bottom", fill=tk.X)
        
        test_button = tk.Button(
            self,
            text="Test",
            command=lambda: test(),
        )
        test_button.pack(side="bottom", fill=tk.X)


class SidePage1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Leer QR")
        label.pack(padx=10, pady=10)

        switch_window_button = tk.Button(
            self,
            text="Volver al menu",
            command=lambda: controller.show_frame(MainPage),
        )
        switch_window_button.pack(side="bottom", fill=tk.X)

        test_button = tk.Button(
            self,
            text="Prueba",
            command=lambda: test1(),
        )
        test_button.pack(side="bottom", fill=tk.X)

def test():
    print("TEST")

def test1():
    print("PRUEBA")

def main():
    if __name__ == "__main__":
        testObj = windows()
        testObj.mainloop()

main()