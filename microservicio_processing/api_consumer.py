import requests

API_URL = "https://api.postcodes.io/postcodes"

def fetch_postcode(latitude: float, longitude: float):
    """
    Consulta la API de postcodes.io para obtener el código postal más cercano a unas coordenadas.
    Retorna el código postal si existe, de lo contrario devuelve None.
    """
    url = API_URL+f"?lon={longitude}&lat={latitude}"
    try:
        response = requests.get(url,timeout=5)
        response.raise_for_status()
                
        data = response.json()

        if "result" not in data:
            print(f"Respuesta de la API sin 'result': {data}")
            return None

        if isinstance(data["result"], list) and len(data["result"]) > 0:
            return data["result"][0].get("postcode", None)
        
        if isinstance(data["result"], dict):
            return data["result"].get("postcode", None)
    
    except requests.exceptions.RequestException as e:
        print(f"Error en API externa: {e}")    
    except Exception as e:
        print(f"Estructura inesperada en la respuesta de la API: {e}")
    return None

def fetch_postcodes_batch(coordinates):
    """
    Consulta la API de postcodes.io en batch para obtener múltiples códigos postales.
    Retorna un diccionario { (lat, lon): postcode } si existen, de lo contrario omite.
    """
    if not coordinates:
        print("Llamado con lista vacía.")
        return {}
    payload = {
        "geolocations": [{"latitude": lat, "longitude": lon} for lat, lon in coordinates]
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()
        print(f"debug de API batch: {data}")

        if "result" not in data or not isinstance(data["result"], list):
            print(f"Respuesta de la API sin 'result': {data}")
            return {}

        result_dict = {}

        for item in data["result"]:
            if not isinstance(item, dict) or "query" not in item or "result" not in item:
                print(f"Elemento inesperado en la respuesta batch: {item}")
                continue
            
            query = item["query"]
            if "latitude" not in query or "longitude" not in query:
                print(f"Faltan coordenadas en `query`: {query}")
                continue

            lat, lon = query["latitude"], query["longitude"]

            result = item["result"]
            if isinstance(result, list) and len(result) > 0 and "postcode" in result[0]:
                result_dict[(lat, lon)] = result[0]["postcode"]
            elif isinstance(result, dict) and "postcode" in result:
                result_dict[(lat, lon)] = result["postcode"]
            else:
                print(f"No se encontró postcode para {lat}, {lon}")

        print(f"Postcodes procesados en batch: {result_dict}")
        return result_dict
    
    except requests.exceptions.RequestException as e:
        print(f"Error en API externa: {e}")    
    except Exception as e:
        print(f"Estructura inesperada en el llamado en batch de la API: {e}")
    return {}