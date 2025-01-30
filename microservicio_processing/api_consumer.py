import requests

API_URL = "https://api.postcodes.io/postcodes"

def fetch_postcode(latitude: float, longitude: float):
    url = API_URL+f"?lon={longitude}&lat={latitude}"
    try:
        response = requests.get(url,timeout=5)
        
        if response.status_code != 200:
            print(f"Error en API externa: {response.status_code} - {response.text}")
            return None
        
        data = response.json()

        print(f"Respuesta API: {data}")

        if isinstance(data["result"], list) and len(data["result"]) > 0:
            return data["result"][0].get("postcode", None)
        
        if isinstance(data["result"], dict):
            return data["result"].get("postcode", None)
    
    except Exception as e:
        print(f"Estructura inesperada en la respuesta de la API: {e}")
    return None
