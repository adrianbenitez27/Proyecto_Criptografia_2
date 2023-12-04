from pymongo import MongoClient
import gridfs
from bson import ObjectId  # Importa ObjectId

# Conexión a MongoDB
uri = "mongodb+srv://base_Cripto:rDY39el5cJgqhgPF@cluster0.f9umqk5.mongodb.net/?retryWrites=true&w=majority"
try:
    client = MongoClient(uri)
    # Intenta obtener los nombres de las bases de datos para verificar la conexión
    client.list_database_names()
    print("Conexión a MongoDB exitosa.")
except Exception as e:
    print(f"Fallo al conectar a MongoDB: {e}")
    # Salir del script si la conexión falla
    exit()

db = client["pedidos"]
fs = gridfs.GridFS(db)

# Función para recuperar un archivo
def recuperar_archivo(archivo_id):
    # Convierte la cadena a ObjectId
    archivo_id_obj = ObjectId(archivo_id)

    if not fs.exists(archivo_id_obj):
        print("Archivo no encontrado")
        return

    archivo = fs.get(archivo_id_obj)
    contenido = archivo.read()
    
    # Define un nuevo nombre de archivo agregando '_recuperado'
    nuevo_nombre = archivo.filename.split('.')[0] + '_recuperado.' + archivo.filename.split('.')[1]

    # Guardar el contenido en un archivo local con el nuevo nombre
    with open(nuevo_nombre, 'wb') as f:
        f.write(contenido)

    print(f"Archivo recuperado")

# Ejemplo de uso
archivo_id = "656d2b11ff7f305300fa96a7"
recuperar_archivo(archivo_id)