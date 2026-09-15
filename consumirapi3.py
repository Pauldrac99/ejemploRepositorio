import requests
 
URL = "http://10.121.16.118:7010/api/enviar"
DATA = {
    "imagen":[126, 126, 96, 126, 126, 6, 126,126]
}
 
response = requests.post(URL, json=DATA)
 
if response.status_code:
    data = response.json()
 
    print('Post creado de forma exitosa')
    print('Respuesta:', data)
else:
    print('Error en la solicitud, detalles:', response.text)