import requests

response = requests.get('https://randomfox.ca/floof')
if response.status_code == 200:
    print(response.text)
    fox = response.json()
    print(f"Image link: {fox['image']}")

else:
    print('Unsuccessfull in getting data')