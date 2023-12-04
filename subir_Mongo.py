import pymongo
import gridfs
from bson import ObjectId

# Cadena de conexión (reemplaza con tu propia URL)
MONGO_URI = "mongodb+srv://base_Cripto:rDY39el5cJgqhgPF@cluster0.f9umqk5.mongodb.net/?retryWrites=true&w=majority"

try:
    # Conexión al clúster
    client = pymongo.MongoClient(MONGO_URI)
    
    # Intenta listar las colecciones como una forma de verificar la conexión
    client.list_database_names()
    print("Conexión a MongoDB exitosa.")

except pymongo.errors.ConnectionFailure as e:
    print(f"Fallo al conectar a MongoDB: {e}")
    exit()

db = client['pedidos']  # Reemplaza con el nombre de tu base de datos

# Usar GridFS para archivos grandes
fs = gridfs.GridFS(db)

# Función para subir un archivo
def subir_archivo(ruta_archivo):
    with open(ruta_archivo, 'rb') as archivo:
        contenido = archivo.read()
        archivo_id = fs.put(contenido, filename=ruta_archivo)
        return archivo_id

# Ejemplo de uso
try:
    archivo_id = subir_archivo('archivoprueba.txt')
    print(f"Archivo subido con ID: {archivo_id}")
except Exception as e:
    print(f"Error al subir el archivo: {e}")