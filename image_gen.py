import requests
import json
import os
from dotenv import load_dotenv
import time

# Load the .env file
load_dotenv()

# Specify the API key and headers
api_key = os.getenv("TAKOMO_API_KEY")
#api_key = 'xx_xxxxxxxxxxxxxxxxxxxx'
print(f'Bearer {api_key}')
headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

print(headers)
# Specify the data you want to send
#data = {    
#    "data": {
#        "Text_y1kw": "A quick brown fox jumped over the lazy dog."
#        }
#}


# Print the response

def dalle_image(input):
    # Specify the API key and headers
    oai_api_key = os.getenv("OPENAI_API_KEY")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {oai_api_key}'
    }

    # Specify the data you want to send
    data = {
    "prompt": f"{input}",
    "n":1,
    "size":"1024x1024"
    }
    # Specify the URL
    url = 'https://api.openai.com/v1/images/generations'
    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))
    # Print the response
    image_url = response.json()['data'][0]['url']
    print(image_url)
    return image_url



def make_image(input):
    print("will make an image!: "+input)
    data1 = {"Text_y1kw": f"{input} in a masterful and artistic style, in style of dgtlv2", #mj-gs
             "size": 500} 
    # Specify the URL
    url = 'https://api.takomo.ai/20999f55-b359-49c6-ae08-fb2089693d7c'

    # Make the POST request
    print(url, headers, json.dumps(data1))
    response = requests.post(url, headers=headers, json=data1)

    print(response.json())
    print(response.status_code)
    if response.status_code == 201:
        data = response.json()
        int_url = f"https://api.takomo.ai/20999f55-b359-49c6-ae08-fb2089693d7c/inferences"
        time.sleep(3)
        #tempid = "816c9879-05b3-42c8-8712-8bcee4bc14df"
        print(f"{int_url}/{data['id']}")
        
        while True:
            response2 = requests.get(f"{int_url}/{data['id']}", headers=headers)
            #response2 = requests.get(f"{int_url}/{tempid}", headers=headers)
            intf_data = response2.json()

            if response2.status_code == 200:
                if intf_data['status'] == 'successful':
                    print('Found data:', intf_data)
                    image_url = intf_data['data']['Image_dols']['downloadUrl']
                    return image_url
                else:
                    print('Still in queue, trying again in 2 seconds.')
                    time.sleep(2) # Waiting 5 seconds before the next attempt
            
            else:
                print(f"Error occurred: {response2.status_code}, {response2.text}")
                time.sleep(2)
                #break
    # If the request was successful

#https://api.takomo.ai/20999f55-b359-49c6-ae08-fb2089693d7c/inferences/816c9879-05b3-42c8-8712-8bcee4bc14df
    

#print("Our image link is: " + make_image("a quick brown elegant fox hunting in the woods"))

