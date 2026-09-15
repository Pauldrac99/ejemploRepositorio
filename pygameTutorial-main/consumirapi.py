import requests
 
URL = "http://10.121.16.118.7010/api/enviar" 
response = requests.get(URL)
 
if response.status_code == 200:
    print('Solicitud exitosa')
    print('Data:', response.json())
else:
    print('Error en la solicitud, detalles:', response.text)