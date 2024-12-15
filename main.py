from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from Game_generation_utils import generator
import os

app = FastAPI()
fichero_informacion = "informacion.txt"
usuarios_conectados = {}
cont = 0
id_disponibles = []

SEEDTEMP = 13532
SEEDALTU = 131312
SEEDHUME = 31253

generador = generator(
    seedTemp=SEEDTEMP,
    seedAltu=SEEDALTU,
    seedHume=SEEDHUME,
    seedRios=31234,
    tamRios=7,
    varRios=128
)


# FUNCION PARA ESCRIBIR EN EL FICHERO EL USUARIO:
def escribir_usuario(id: int):
    with open(fichero_informacion, "a+") as file:
        file.write(f"{id}\n")


# FUNCION PARA ELIMINAR EL USUARIO:
def eliminar_usuario(id: int):
    if os.path.exists(fichero_informacion):
        with open(fichero_informacion, "r") as file:
            lineas = file.readlines()
        with open(fichero_informacion, "w") as file:
            for linea in lineas:
                if linea.strip("\n") != str(id):
                    file.write(linea)


@app.get("/login")
async def asignar_id():
    global cont, id_disponibles
    if id_disponibles:
        id = id_disponibles.pop()
    else: id = cont
    cont += 1
    escribir_usuario(id)
    usuarios_conectados[id] = None
    return {"status": "success", "id": id}


@app.post("/logout/{id}")
async def logout(id: int):
    if id not in usuarios_conectados:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    eliminar_usuario(id)
    usuarios_conectados.pop(id, None)
    id_disponibles.append(id)
    return {"status": "success", "message":f"Usuario {id} desconectado y eliminado"}


# FUNCION PARA DEVOLVER POSICIONES DE USUARIOS:
@app.get("/lista_posiciones/{id_cliente}")
async def devolver_posiciones(id_cliente: int):
    if len(usuarios_conectados) <= 1:
        return {"status": "success", "posiciones":[]}
    else:
        posiciones = [pos for uid, pos in usuarios_conectados.items() if uid != id_cliente]
        return {"status": "success", "posiciones":posiciones}


@app.get("/biomes/{x}/{y}")
async def root(x: int, y: int):
    generador.getChunk(x, y)
    return FileResponse(f"./Chunks/T_{SEEDTEMP}A_{SEEDTEMP}H_{SEEDTEMP}/{x}/C_{y}.npy")


@app.get("/objects/{x}/{y}")
async def root(x: int, y: int):
    generador.getChunk(x, y)
    return FileResponse(f"./Chunks/T_{SEEDTEMP}A_{SEEDTEMP}H_{SEEDTEMP}/{x}/O_{y}.npy")


# FUNCION POST PARA RECIBIR UNA POSICION DEL USUARIO:
@app.post("/posicion/{id}/{x}/{y}")
async def mandar_posicion(id: int, x: int, y: int):
    if id not in usuarios_conectados:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    else:
        usuarios_conectados[id] = (x, y)
        return {"id": id, "posicion": (x, y)}