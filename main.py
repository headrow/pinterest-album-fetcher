import os
import requests

def get_pins(username: str, bookmark: str = "", numOfImgs: int = 0):
    link = "https://pt.pinterest.com/resource/UserPinsResource/get/?source_url=/" + username + "/pins/&data={\"options\":{\"is_own_profile_pins\":true,\"username\":\"" + username + "\",\"field_set_key\":\"grid_item\",\"pin_filter\":null, \"bookmarks\":[\"" + bookmark + "\"]},\"context\":{}}"
    req = requests.get(link, timeout=5)
    response = req.json()["resource_response"]

    if (req.status_code == 200):
        if (os.path.isdir(f"output/{username}/pins") == False):
            os.makedirs(f"output/{username}/pins")

        for pin in response["data"]:
            imgName = pin["id"]
            imgUrl = pin["images"]["orig"]["url"]
            imgExt = imgUrl[imgUrl.rfind("."):]
            imgData = requests.get(imgUrl).content

            print(f"Saving the pin {imgName}")
            print(f"File extension is {imgExt}")

            with open(f"output/{username}/pins/{imgName}{imgExt}", "wb") as imgCopy:
                imgCopy.write(imgData)

            numOfImgs += 1
        
        if (response["bookmark"] != ""):
            get_pins(username=username, bookmark=response["bookmark"], numOfImgs=numOfImgs)
        else:
            print(f"Fetched {numOfImgs} images.")
    else:
        print(f"There was a {req.status_code} error with your search: {response["error"]["message"]}")

username = input("Insert your Pinterest username: ")
get_pins(username=username)
