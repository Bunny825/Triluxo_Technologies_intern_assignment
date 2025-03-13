import requests
url="http://127.0.0.1:5000/ask"
headers={"Content-Type":"application/json"}
data={"query":"explain about the course LEARN CLOUD COMPUTING BASICS-AWS"}

response=requests.post(url, json=data, headers=headers)
print(response.status_code)
print(response.json())

