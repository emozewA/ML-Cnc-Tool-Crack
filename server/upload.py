import requests

url = 'http://127.0.0.1:8000/upload-image/'
file_path = 'tooldefect.jpg'

with open(file_path, 'rb') as f:
    files = {'image': f}
    response = requests.post(url, files=files)

print(response.json())
