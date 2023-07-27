import requests

url = "http://127.0.0.1:8000/home/Followers_ids/"

payload = {}
headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
                   'eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkxMDM0OTAyLCJpYXQiOjE2OTA0MzAxMDIsImp0aSI6'
                   'IjNhNTQ1MmJlMjY5YzQyZTY4MDY2ZjAwNWU1NWEyNmFiIiwidXNlcl9pZCI6M30.OZ3PJ4Rk-XdwLKus_fb4a'
                   'EVSMbZsclNw_q_6k9HWn-Y',
  'Cookie': 'csrftoken=JajeAlFw8jXzrk37rIBmLjnpUiE6U2kY'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)