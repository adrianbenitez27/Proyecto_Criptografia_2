import tkinter as tk
from tkinter import filedialog, messagebox
from pymongo import MongoClient
import bson

# Conexión a MongoDB
MONGO_URI = "mongodb+srv://base_Cripto:rDY39el5cJgqhgPF@cluster0.f9umqk5.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["pedidos"]
collection = db["Imagenes"]

# Función para seleccionar archivo
def seleccionar_archivo():
    global filename
    filename = filedialog.askopenfilename()
    entry_upload.delete(0, tk.END)
    entry_upload.insert(0, filename)

# Función para subir archivo a una colección como datos binarios
def subir_archivo():
    global filename
    if filename:
        try:
            with open(filename, 'rb') as file:
                contenido_binario = file.read()
                documento = {"nombre_archivo": filename.split('/')[-1], "contenido": bson.binary.Binary(contenido_binario)}
                collection.insert_one(documento)
                messagebox.showinfo("Subir Archivo", "Archivo subido con éxito a la colección")
        except Exception as e:
            messagebox.showerror("Subir Archivo", "Error al subir archivo: " + str(e))
    else:
        messagebox.showwarning("Subir Archivo", "No se ha seleccionado ningún archivo")

# Función para recuperar un archivo
def recuperar_archivo():
    nombre_archivo = entry_download.get()
    if nombre_archivo:
        documento = collection.find_one({"nombre_archivo": nombre_archivo})
        if documento:
            contenido_binario = documento['contenido']
            with open(nombre_archivo, 'wb') as file:
                file.write(contenido_binario)
            messagebox.showinfo("Recuperar Archivo", f"Archivo '{nombre_archivo}' recuperado con éxito")
        else:
            messagebox.showerror("Recuperar Archivo", "Archivo no encontrado en la base de datos")
    else:
        messagebox.showwarning("Recuperar Archivo", "No se ha especificado el nombre del archivo")

# Crear ventana de Tkinter
root = tk.Tk()
root.title("Gestor de Archivos MongoDB")

# Crear y colocar widgets para subir archivo
label_upload = tk.Label(root, text="Subir Archivo:")
label_upload.pack(padx=10, pady=5)

entry_upload = tk.Entry(root, width=50)
entry_upload.pack(padx=10, pady=5)

boton_seleccionar = tk.Button(root, text="Seleccionar Archivo", command=seleccionar_archivo)
boton_seleccionar.pack(padx=10, pady=5)

boton_subir = tk.Button(root, text="Subir Archivo", command=subir_archivo)
boton_subir.pack(padx=10, pady=5)

# Crear y colocar widgets para descargar archivo
label_download = tk.Label(root, text="Recuperar Archivo por Nombre:")
label_download.pack(padx=10, pady=5)

entry_download = tk.Entry(root, width=50)
entry_download.pack(padx=10, pady=5)

boton_recuperar = tk.Button(root, text="Recuperar Archivo", command=recuperar_archivo)
boton_recuperar.pack(padx=10, pady=5)

# Iniciar el bucle de eventos
root.mainloop()

