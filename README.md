# 🚀 Prueba Técnica - Data Engineer Bia

## 📌 Descripción
Este proyecto implementa dos microservicios en **FastAPI** para procesar coordenadas geográficas de un archivo CSV, obtener códigos postales mediante la API pública **postcodes.io**, y almacenar los datos en una base de datos **PostgreSQL**.

## 📁 Arquitectura
La solución se divide en:
1. **Microservicio uploader**: Recibe el archivo `postcodes_geo.csv` y almacena las coordenadas en la base de datos.
2. **Microservicio processing**: Obtiene los códigos postales de cada coordenada desde `postcodes.io` y los guarda en la base de datos.
3. **Base de Datos (PostgreSQL)**: Almacena los datos procesados.

### 📊 Diagrama de Arquitectura
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