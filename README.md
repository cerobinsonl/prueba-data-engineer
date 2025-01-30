# 🚀 **Prueba Técnica - Data Engineer Bia**

## 📌 **Descripción**
Este proyecto implementa dos microservicios en **FastAPI** para procesar coordenadas geográficas desde un archivo CSV, obtener códigos postales mediante la API pública **postcodes.io**, y almacenar los datos en una base de datos **PostgreSQL**.

---

## 📁 **Arquitectura**
### 🛠️ **Componentes Principales**
1. **Microservicio Uploader**:  
   - Recibe un archivo **CSV** con coordenadas (`latitude`, `longitude`) y las almacena en la base de datos.
  
2. **Microservicio Processing**:  
   - Obtiene los códigos postales de cada coordenada usando la API pública **postcodes.io**.
   - Almacena los datos procesados en la base de datos.

3. **Base de Datos (PostgreSQL)**:  
   - Guarda la información de coordenadas y códigos postales.

### 📊 **Diagrama de Arquitectura**
```plaintext
+------------------+       +---------------------+       +----------------+
| Cliente (CSV)    | ----> | Microservicio 1     | ----> | Base de Datos  |
| (Upload CSV)     |       | (Guarda coordenadas)|       | (PostgreSQL)   |
+------------------+       +---------------------+       +----------------+
                                                      |      ▲
                                                      |      |
                                                      v      |
+------------------+       +---------------------+       +----------------+
|                 | ----> | Microservicio 2     | ----> | API postcodes.io |
|                 |       | (Consulta API y     |       | (Retorna Postcode)|
|                 |       | actualiza BD)       |       +----------------+
+------------------+       +---------------------+  
```

---

## 🛠 **Requisitos**
- **Docker** y **Docker Compose** instalados.
- **PostgreSQL** (se ejecuta dentro del contenedor).
- **Python 3.9** (si deseas correr el código localmente).

---

## 🚀 **Instalación y Ejecución**
### 1️⃣ **Clonar el repositorio**
```bash
git clone https://github.com/tu_usuario/prueba-data-engineer.git
cd prueba-data-engineer
```

### 2️⃣ **Levantar los servicios con Docker**
Ejecuta el siguiente comando para iniciar los microservicios y la base de datos:
```bash
docker-compose up --build
```
Esto iniciará:
- **PostgreSQL** en `localhost:5432`
- **Microservicio Uploader** en `http://localhost:8000`
- **Microservicio Processing** en `http://localhost:8001`

---

## 🔥 **Uso de los Microservicios**
Aquí tienes ejemplos de cómo probar los endpoints usando **Postman** o `cURL`.

### 📤 **1. Subir un archivo CSV**
- **Endpoint:** `POST http://localhost:8000/upload/`
- **Formato del CSV (`text/csv`):**
```csv
latitude,longitude
51.509865,-0.118092
52.486243,-1.890401
```
- **Ejemplo en `cURL`:**
```bash
curl -X POST "http://localhost:8000/upload/" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@postcodes_geo.csv"
```

- **Ejemplo en Postman**:
  - Método: `POST`
  - URL: `http://localhost:8000/upload/`
  - Body → **form-data**:
    - `key`: **file**
    - `value`: (subir archivo `postcodes_geo.csv`)
    - `Content-Type`: `text/csv`

📌 **Respuesta esperada (JSON):**
```json
{
  "rows_processed": 2,
  "message": "Archivo procesado correctamente"
}
```

---

### 📡 **2. Procesar coordenadas y obtener códigos postales**
- **Endpoint:** `POST http://localhost:8001/process_batch/`
- **Formato JSON:**
```json
{
  "coordinates": [
    {"latitude": 51.509865, "longitude": -0.118092},
    {"latitude": 52.486243, "longitude": -1.890401}
  ]
}
```
- **Ejemplo en `cURL`:**
```bash
curl -X POST "http://localhost:8001/process_batch/" \
     -H "Content-Type: application/json" \
     -d '{"coordinates": [{"latitude": 51.509865, "longitude": -0.118092},{"latitude": 52.486243, "longitude": -1.890401}]}'
```

📌 **Respuesta esperada (JSON):**
```json
{
  "message": "Códigos postales actualizados en la base de datos"
}
```

---

## 🛠 **Ejecución de Pruebas**
Para ejecutar los tests unitarios en los contenedores:
```bash
docker-compose up --build test_uploader test_processing
```
Esto ejecutará `pytest` sobre ambos microservicios y mostrará los resultados.

---

## 📚 **Tecnologías Utilizadas**
- **FastAPI** - Framework web para APIs en Python.
- **PostgreSQL** - Base de datos relacional.
- **Docker** - Contenerización de microservicios.
- **pytest** - Framework de testing en Python.

---

## 🔄 **Flujo de Trabajo Implementado**

### 🏁 **1. Inicio del Proyecto**
El desarrollo comenzó con una implementación **directa** de dos microservicios en FastAPI:
- **Microservicio Uploader**: Recibía un archivo CSV con coordenadas y lo almacenaba en la base de datos.
- **Microservicio Processing**: Leía las coordenadas desde la base de datos, consultaba la API pública **postcodes.io** para obtener los códigos postales y actualizaba los registros en la base de datos.

Inicialmente, estos microservicios fueron desarrollados **y probados de forma local** sin contenerización. Esto permitía iterar rápidamente sobre la funcionalidad principal antes de pensar en despliegue.

---

### 🐳 **2. Contenerización con Docker**
Una vez verificado que los microservicios funcionaban localmente, se decidió contenerizarlos usando **Docker** para garantizar la portabilidad y facilitar el despliegue.

Se creó un `docker-compose.yaml` para levantar los siguientes servicios:
- **PostgreSQL** (como base de datos interna).
- **Microservicio Uploader** (`http://localhost:8000`).
- **Microservicio Processing** (`http://localhost:8001`).

Los **Dockerfiles** correspondientes fueron configurados con las dependencias necesarias para cada microservicio.

✅ **Estado del sistema:**
- Se podían levantar ambos microservicios con `docker-compose up`.
- Se verificó que la base de datos se iniciaba correctamente y que los microservicios podían comunicarse con ella.

---

### 📤 **3. Carga del Archivo CSV**
Para probar el **Microservicio Uploader**, se realizó una primera carga de prueba con un CSV de coordenadas geográficas:

#### **Ejemplo de archivo `postcodes_geo.csv`**
```csv
latitude,longitude
51.509865,-0.118092
52.486243,-1.890401
```

#### **Ejemplo de solicitud en `cURL`**
```bash
curl -X POST "http://localhost:8000/upload/" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@postcodes_geo.csv"
```

📌 **Respuesta esperada:**
```json
{
  "rows_processed": 2,
  "message": "Archivo procesado correctamente"
}
```

✅ **Estado del sistema:**
- El archivo CSV se guardó correctamente en la base de datos.
- Cada fila quedó registrada con coordenadas, pero sin código postal.

---

### 📡 **4. Procesamiento de Coordenadas**
Una vez que las coordenadas estaban almacenadas en la base de datos, se implementó el **Microservicio Processing** para obtener los códigos postales correspondientes.

Este servicio:
1. Lee las coordenadas desde la base de datos.
2. Consulta la API pública `postcodes.io`.
3. Almacena el código postal en la base de datos.

#### **Ejemplo de solicitud en `cURL`**
```bash
curl -X POST "http://localhost:8001/process_batch/" \
     -H "Content-Type: application/json" \
     -d '{"coordinates": [{"latitude": 51.509865, "longitude": -0.118092},{"latitude": 52.486243, "longitude": -1.890401}]}'
```

📌 **Respuesta esperada:**
```json
{
  "message": "Códigos postales actualizados en la base de datos"
}
```

✅ **Estado del sistema:**
- Se verificó que los códigos postales se obtenían correctamente y se actualizaban en la base de datos.

---

### 🛠 **5. Implementación de Pruebas**
Para validar la funcionalidad de cada microservicio, se implementaron pruebas unitarias usando `pytest`.

Las pruebas cubrieron los siguientes casos:
- ✅ **Microservicio Uploader**:
  - Verificar que se acepta un archivo CSV y se almacenan las coordenadas en la base de datos.
  - Manejo de archivos mal formateados.
  - Validación de datos incompletos.
  
- ✅ **Microservicio Processing**:
  - Verificar que se obtienen códigos postales correctamente desde la API.
  - Manejo de respuestas inválidas o errores en la API externa.
  - Verificación de la actualización correcta de la base de datos.

Para ejecutar las pruebas en los contenedores:
```bash
docker-compose up --build test_uploader test_processing
```

