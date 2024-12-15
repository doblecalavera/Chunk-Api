import requests
import random
import numpy as np
import time
import os

# URL base del servidor
base_url = "http://127.0.0.1:6969"

# Función para hacer login y obtener un ID de usuario
def login():
    response = requests.get(f"{base_url}/login")
    if response.status_code == 200:
        data = response.json()
        print(f"Login exitoso: {data}")
        return data["id"]
    else:
        print(f"Error en login: {response.status_code}")
        return None

# Función para mandar posición
def mandar_posicion(id, x, y):
    response = requests.post(f"{base_url}/posicion/{id}/{x}/{y}")
    if response.status_code == 200:
        print(f"Posición enviada: {response.json()}")
    else:
        print(f"Error al enviar posición: {response.status_code}")


# Función para pedir objeto
def pedir_objeto(x, y):
    response = requests.get(f"{base_url}/objects/{x}/{y}")
    if response.status_code == 200:
        ruta = f"peticion_cliente/{x}/{y}/object.npy" 
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "wb") as f:
            f.write(response.content)
        print(f"Objeto recibido y guardado en: {ruta}")
        return np.load(ruta)
    else:
        print(f"Error al pedir objeto: {response.status_code}")
        return None

# Función para pedir bioma
def pedir_bioma(x, y):
    response = requests.get(f"{base_url}/biomes/{x}/{y}")
    if response.status_code == 200:
        ruta = f"peticion_cliente/{x}/{y}/biome.npy"
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "wb") as f:
            f.write(response.content)
        print(f"Bioma recibido y guardado en: {ruta}")
        return np.load(ruta)
    else:
        print(f"Error al pedir bioma: {response.status_code}")
        return None


# Función para obtener posiciones
def obtener_posiciones(id_cliente):
    response = requests.get(f"{base_url}/lista_posiciones/{id_cliente}")
    if response.status_code == 200:
        print(f"Posiciones recibidas: {response.json()}")
    else:
        print(f"Error al obtener posiciones: {response.status_code}")

# Función para hacer logout
def logout(id):
    response = requests.post(f"{base_url}/logout/{id}")
    if response.status_code == 200:
        print(f"Logout exitoso: {response.json()}")
    else:
        print(f"Error en logout: {response.status_code}")

def main():
    # Login
    user_id = login()
    if user_id is None:
        exit()

    # Mandar posición aleatoria
    x, y = random.randint(0, 10), random.randint(0, 10)
    mandar_posicion(user_id, x, y)

    # Pedir objeto y guardarlo en una variable
    objeto = pedir_objeto(x, y)

    # Mandar otra posición aleatoria
    time.sleep(30)
    x, y = random.randint(0, 10), random.randint(0, 10)
    mandar_posicion(user_id, x, y)

    # Pedir bioma
    bioma = pedir_bioma(x, y)

    # Obtener posiciones
    obtener_posiciones(user_id)

    # Logout
    time.sleep(60)
    logout(user_id)

if __name__ == "__main__":
    main()