import asyncio
import websockets
import json
import os
import numpy as np

async def enviar_posicion(websocket, x, y):
    mensaje = {
        "type": "posicion",
        "x": x,
        "y": y
    }
    await websocket.send(json.dumps(mensaje))
    print(f"Posición enviada: {mensaje}")

async def recibir_posiciones(websocket):
    mensaje = {
        "type": "recibir_posiciones"
    }
    await websocket.send(json.dumps(mensaje))
    while True:
        respuesta = await websocket.recv()
        data = json.loads(respuesta)
        print(f"Posiciones recibidas: {data}")
        break

async def recibir_chunk(websocket, chunk_id):
    mensaje = {
        "type": "recibir_chunk",
        "chunk_id": chunk_id
    }
    await websocket.send(json.dumps(mensaje))
    
    # Recibir el primer chunk
    chunk1 = await websocket.recv()
    # Recibir el segundo chunk
    chunk2 = await websocket.recv()
    
    p1, p2 = chunk_id.split(',')
    p1 = int(p1)
    p2 = int(p2)
    
    ruta1 = f"peticion_cliente/{p1}/{p2}/chunk.npy"
    ruta2 = f"peticion_cliente/{p1}/{p2}/obstaculos.npy"
    
    # Crear directorios si no existen
    os.makedirs(os.path.dirname(ruta1), exist_ok=True)
    
    # Guardar el contenido de los chunks en los archivos
    chunk1_np = np.array(json.loads(chunk1))
    chunk2_np = np.array(json.loads(chunk2))
    np.save(ruta1, chunk1_np)
    np.save(ruta2, chunk2_np)
    
    print(f"Chunks recibidos y guardados en: {ruta1} y {ruta2}")

async def main():
    uri = "ws://localhost:6969/ws"  # Cambia esto a la URL de tu servidor
    async with websockets.connect(uri) as websocket:
        print("Conexión establecida con el servidor.")
        
        while True:
            entrada = input("Escribe tu comando: ")
            
            if entrada.lower() == "cerrar":
                print("Cerrando conexión...")
                break
            
            elif "," in entrada:
                # Recibir chunk
                await recibir_chunk(websocket, entrada)
            
            elif entrada.lower() == "recibir posiciones":
                # Recibir posiciones
                await recibir_posiciones(websocket)
            
            else:
                try:
                    # Mandar posición
                    x, y = map(float, entrada.split())
                    await enviar_posicion(websocket, x, y)
                except ValueError:
                    print("Entrada no válida. Por favor, escribe las coordenadas en formato 'x y'.")

        await websocket.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    asyncio.run(main())
