import tkinter as tk
from tkinter import messagebox
import time
import pygame

# Inicializar pygame para usar sonidos
pygame.mixer.init()

class CronometroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crono")
        self.root.geometry("170x220")
        self.root.resizable(False, False)

        # Hacer que la ventana esté siempre al frente
        self.root.attributes('-topmost', 1)

        self.inicio = 0
        self.timeout = None
        self.intervaloSonido = 35  # Intervalo por defecto en segundos
        self.ciclos = 0
        self.tiempoTotal = 0

        # Cambiar la ruta del sonido por el archivo local
        self.sonido = pygame.mixer.Sound("button-15.mp3")  # Ruta local del archivo

        # UI
        self.titulo = tk.Label(self.root, text="C&G", bg="#007BFF", fg="white", font=("Arial", 10), width=10)
        self.titulo.pack(fill=tk.X)

        self.crono_label = tk.Label(self.root, text="00:00:00:000", font=("Arial", 12))
        self.crono_label.pack(pady=2)

        self.start_button = tk.Button(self.root, text="Empezar", command=self.empezar_detener, width=4)
        self.start_button.pack(pady=2)

        self.intervalo_label = tk.Label(self.root, text="Intervalo (segundos):", font=("Arial", 10))
        self.intervalo_label.pack(pady=2)

        self.intervalo_entry = tk.Entry(self.root)
        self.intervalo_entry.insert(0, "35")
        self.intervalo_entry.pack(pady=2)

        self.config_button = tk.Button(self.root, text="Configurar Intervalo", command=self.verificar_contrasena, width=14)
        self.config_button.pack(pady=2)

        self.ciclos_label = tk.Label(self.root, text="Ciclos: 0", font=("Arial", 10))
        self.ciclos_label.pack(pady=2)

        self.tiempo_total_label = tk.Label(self.root, text="Tiempo total: 00:00", font=("Arial", 10))
        self.tiempo_total_label.pack(pady=2)

    def verificar_contrasena(self):
        # Crear ventana para pedir la contraseña
        self.contrasena_ventana = tk.Toplevel(self.root)
        self.contrasena_ventana.title("Verificar Contraseña")
        self.contrasena_ventana.geometry("250x200")
        self.contrasena_ventana.resizable(False, False)

        # Etiqueta y campo de entrada de contraseña
        self.contrasena_label = tk.Label(self.contrasena_ventana, text="Ingrese la contraseña:")
        self.contrasena_label.pack(pady=10)

        self.contrasena_entry = tk.Entry(self.contrasena_ventana, show="*")
        self.contrasena_entry.pack(pady=5)

        self.confirmar_button = tk.Button(self.contrasena_ventana, text="Confirmar", command=self.cambiar_intervalo)
        self.confirmar_button.pack(pady=10)

    def cambiar_intervalo(self):
        contrasena = self.contrasena_entry.get()

        # Contraseña predeterminada (puedes cambiarla)
        contrasena_correcta = "280298"

        if contrasena == contrasena_correcta:
            try:
                segundos = int(self.intervalo_entry.get())
                if segundos > 0:
                    self.intervaloSonido = segundos
                    messagebox.showinfo("Configuración", f"Intervalo de reinicio configurado a {segundos} segundos.")
                    self.contrasena_ventana.destroy()  # Cerrar ventana de contraseña
                else:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingrese un valor válido de segundos.")
        else:
            messagebox.showerror("Error", "Contraseña incorrecta.")
            self.contrasena_ventana.destroy()  # Cerrar ventana de contraseña si es incorrecta

    def empezar_detener(self):
        if self.timeout is None:
            self.start_button.config(text="Detener")
            self.inicio = time.time()
            self.funcionando()
        else:
            self.start_button.config(text="Empezar")
            self.timeout = None
            self.ciclos = 0
            self.tiempoTotal = 0
            self.reset_display()

    def funcionando(self):
        self.timeout = self.root.after(10, self.actualizar_cronometro)

    def actualizar_cronometro(self):
        if self.timeout is None:
            return

        actual = time.time()
        diff = actual - self.inicio

        horas = int(diff // 3600)
        minutos = int((diff % 3600) // 60)
        segundos = int(diff % 60)
        milisegundos = int((diff % 1) * 1000)

        result = f"{self.format_time(horas)}:{self.leading_zero(minutos)}:{self.leading_zero(segundos)}:{self.leading_zero_milisegundos(milisegundos)}"
        self.crono_label.config(text=result)

        if diff >= self.intervaloSonido - 3 and not hasattr(self, 'parpadeo_intervalo'):
            self.parpadear_icono()

        if diff >= self.intervaloSonido:
            self.sonido.play()
            self.inicio = time.time()
            self.ciclos += 1
            self.tiempoTotal += self.intervaloSonido
            self.update_display()
            self.detener_parpadeo()

        self.timeout = self.root.after(10, self.actualizar_cronometro)

    def parpadear_icono(self):
        self.parpadeo_intervalo = True
        self.root.after(500, self.toggle_title)

    def toggle_title(self):
        if hasattr(self, 'parpadeo_intervalo'):
            if self.root.title() == "¡Atención!":
                self.root.title("Cronómetro CCN")
            else:
                self.root.title("¡Atención!")
            self.root.after(500, self.toggle_title)
        else:
            self.root.title("Cronómetro CCN")

    def detener_parpadeo(self):
        if hasattr(self, 'parpadeo_intervalo'):
            del self.parpadeo_intervalo
            self.root.title("Cronómetro CCN")

    def reset_display(self):
        self.crono_label.config(text="00:00:00:000")
        self.ciclos_label.config(text="Ciclos: 0")
        self.tiempo_total_label.config(text="Tiempo total: 00:00")

    def update_display(self):
        minutos_acumulados = int(self.tiempoTotal // 60)
        segundos_acumulados = int(self.tiempoTotal % 60)
        self.tiempo_total_label.config(text=f"Tiempo total: {self.leading_zero(minutos_acumulados)}:{self.leading_zero(segundos_acumulados)}")
        self.ciclos_label.config(text=f"Ciclos: {self.ciclos}")

    def leading_zero(self, time):
        return f"{time:02}"

    def leading_zero_milisegundos(self, time):
        return f"{time:03}"

    def format_time(self, time):
        return f"{time:02}"

if __name__ == "__main__":
    root = tk.Tk()
    app = CronometroApp(root)
    root.mainloop()

