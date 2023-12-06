from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask import Response
import os

app = Flask(__name__)

# Configuración de MongoDB
MONGO_URI = "mongodb+srv://base_Cripto:rDY39el5cJgqhgPF@cluster0.f9umqk5.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client['pintor']
collection_keys = db['key']
collection_aes = db['aes']
collection_pedidos = db['pedidos']
collection_firmas = db['firmas']
collection_solicitudes = db['solicitudes']
collection_pedidos_terminados = db['pedidos_terminados']

@app.route('/download/key/pintor', methods=['GET'])
def download_public_key_pintor():
    file_data = collection_keys.find_one({"filename": "clave_publica_P-256_pintor.pem"})
    if file_data:
        return Response(file_data['content'], mimetype='application/x-pem-file')
    else:
        return jsonify({"message": "Clave pública del pintor no encontrada"}), 404
    
@app.route('/download/key/<filename>', methods=['GET'])
def download_key(filename):
    file_data = collection_keys.find_one({"filename": filename})
    if file_data:
        return Response(file_data['content'], mimetype='application/x-pem-file',
                        headers={"Content-Disposition": f"attachment;filename={filename}"})
    else:
        return jsonify({"message": "Archivo no encontrado"}), 404

@app.route('/download/solicitudes/<filename>', methods=['GET'])
def download_solicitud(filename):
    file_data = collection_solicitudes.find_one({"filename": filename})
    if file_data:
        return Response(file_data['content'], mimetype='text/plain',
                        headers={"Content-Disposition": f"attachment;filename={filename}"})
    else:
        return jsonify({"message": "Archivo no encontrado"}), 404

@app.route('/download/firmas/<filename>', methods=['GET'])
def download_firma(filename):
    file_data = collection_firmas.find_one({"filename": filename})
    if file_data:
        return Response(file_data['content'], mimetype='text/plain',
                        headers={"Content-Disposition": f"attachment;filename={filename}"})
    else:
        return jsonify({"message": "Archivo no encontrado"}), 404
    
@app.route('/download/pedidos/<filename>', methods=['GET'])
def download_pedido(filename):
    file_data = collection_pedidos.find_one({"filename": filename})
    if file_data:
        return Response(file_data['content'], mimetype='application/octet-stream',
                        headers={"Content-Disposition": f"attachment;filename={filename}"})
    else:
        return jsonify({"message": "Archivo no encontrado"}), 404

@app.route('/download/pedidos_terminados/<filename>', methods=['GET'])
def download_pedido_terminado(filename):
    file_data = collection_pedidos_terminados.find_one({"filename": filename})
    if file_data:
        return Response(file_data['content'], mimetype='application/octet-stream',
                        headers={"Content-Disposition": f"attachment;filename={filename}"})
    else:
        return jsonify({"message": "Archivo no encontrado"}), 404


@app.route('/upload/key', methods=['POST'])
def upload_key():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file:
        collection_keys.insert_one({"filename": file.filename, "content": file.read()})
        return jsonify({"message": "Clave pública subida con éxito"})

    return jsonify({"message": "Error al subir la clave pública"}), 500

@app.route('/upload/pedidos', methods=['POST'])
def upload_pedidos():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file:
        collection_pedidos.insert_one({"filename": file.filename, "content": file.read()})
        return jsonify({"message": "Pedido cifrado subido con éxito"})

    return jsonify({"message": "Error al subir el pedido"}), 500

@app.route('/upload/firmas', methods=['POST'])
def upload_firmas():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file:
        collection_firmas.insert_one({"filename": file.filename, "content": file.read()})
        return jsonify({"message": "Firma subida con éxito"})

    return jsonify({"message": "Error al subir la firma"}), 500

@app.route('/upload/solicitudes', methods=['POST'])
def upload_solicitudes():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file:
        collection_solicitudes.insert_one({"filename": file.filename, "content": file.read()})
        return jsonify({"message": "Solicitud subida con éxito"})

    return jsonify({"message": "Error al subir la solicitud"}), 500

@app.route('/upload/pedidos_terminados', methods=['POST'])
def upload_pedidos_terminados():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file:
        collection_pedidos_terminados.insert_one({"filename": file.filename, "content": file.read()})
        return jsonify({"message": "Pedido terminado subido con éxito"})

    return jsonify({"message": "Error al subir el pedido terminado"}), 500

if __name__ == '__main__':
    app.run(debug=True)