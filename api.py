import requests
import os
from dotenv import load_dotenv

def send_create_log(img_path: str, type: str):
  try:
    print("Sending POST log")
    load_dotenv()
    api_path = os.getenv("API_URL")

    if not api_path:
      raise ValueError("API_PATH is missing in .env file")

    api_path = api_path + "/logs"

    payload = {
      "img_path": img_path,
      "type": type
    }

    response = requests.post(url=api_path, json=payload)  

    if response.status_code == 200:
      print("Success:", response.json())
    else:
      print("Error:", response.status_code, response.json())

  except Exception as e:
    print(f"Error sending POST request to API: {e}")
