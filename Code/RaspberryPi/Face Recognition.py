from compreface import CompreFace
from compreface.service import VerificationService
import requests

#Config
DOMAIN = 'http://localhost:8000'
API_KEY = 'b11379e5-70d2-4362-9cff-f1eaaa7018e7'

#Image paths
image1_path = './person1.jpg'
image2_path = './person2.jpg'

#API URL and headers
url = f'{DOMAIN}/api/v1/verification/verify'
headers = {
    'x-api-key': API_KEY
}

#Prepare files
files = {
    'source_image': open(image1_path, 'rb'),
    'target_image': open(image2_path, 'rb'),
}

#POST request
response = requests.post(url, headers=headers, files=files)

#Check the response
if response.status_code == 200:
    result = response.json()
    print("Face verification result:")
    print(result)
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)



