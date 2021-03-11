import requests

url = f'http://localhost:8888/reviews/3'
r = requests.put(url, json={'title': '77777777777 test_title', 'review': '777777777777 test reviews'})
data = r.json()
print(r.status_code)
print(data)
print()

