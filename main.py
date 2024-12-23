import os
import requests

def correct_name(name: str):
    restricted_chars = {'\\', '/', ':', '*', '?', '"', '<', '>', '|'}
    fixed_name = name

    for char in restricted_chars:
        fixed_name = fixed_name.replace(char, "")

    return (fixed_name)

def save_image(name: str, url: str, album: str):
    folder = f"output/{username}/{album}"
    ext = url[url.rfind("."):]
    data = requests.get(url=url).content

    if (os.path.isdir(folder) == False):
        os.makedirs(folder)

    with open(f"{folder}/{name}{ext}", "wb") as imgCopy:
        imgCopy.write(data)

    print(f"Saved the pin {name}")

def get_pins(bookmark: str = "", numOfImgs: int = 0):
    link = "https://www.pinterest.com/resource/UserPinsResource/get/?data={\"options\":{\"username\":\"" + username + "\", \"bookmarks\":[\"" + bookmark + "\"]}}"
    req = requests.get(url=link, cookies={"_pinterest_sess": cookie}, timeout=5)
    response = req.json()["resource_response"]

    if (req.status_code == 200):
        for pin in response["data"]:
            if ("node_id" not in pin):
                continue

            imgName = pin["id"]
            imgAlbum = correct_name(pin["board"]["name"])

            if ("videos" in pin) and (pin["videos"] != None):
                imgUrl = pin["videos"]["video_list"]["V_720P"]["url"]
            else:
                imgUrl = pin["images"]["orig"]["url"]
            
            save_image(name=imgName, url=imgUrl, album=imgAlbum)
            numOfImgs += 1
        
        if ("bookmark" in response):
            get_pins(bookmark=response["bookmark"], numOfImgs=numOfImgs)
        else:
            print(f"Fetched {numOfImgs} images.")
    else:
        print(f"There was a {req.status_code} error with your search: {response["error"]["message"]} ({response["error"]["code"]})")

def get_album(id: str, bookmark: str = "", numOfImgs: int = 0):
    link = "https://www.pinterest.com/resource/BoardFeedResource/get/?data={\"options\":{\"board_id\":\"" + id + "\", \"bookmarks\":[\"" + bookmark + "\"]}}"
    req = requests.get(url=link, cookies={"_pinterest_sess": cookie}, headers={"X-Pinterest-Pws-Handler": "www/[username]/[slug].js"}, timeout=5)
    response = req.json()["resource_response"]

    if (req.status_code == 200):
        for pin in response["data"]:
            if ("node_id" not in pin):
                continue

            imgName = pin["id"]
            imgAlbum = correct_name(pin["board"]["name"])

            if ("videos" in pin) and (pin["videos"] != None):
                imgUrl = pin["videos"]["video_list"]["V_720P"]["url"]
            else:
                imgUrl = pin["images"]["orig"]["url"]
            
            save_image(name=imgName, url=imgUrl, album=imgAlbum)
            numOfImgs += 1
        
        if ("bookmark" in response):
            get_album(id=id, bookmark=response["bookmark"], numOfImgs=numOfImgs)
        else:
            print(f"Fetched {numOfImgs} images.")
    else:
        print(f"There was a {req.status_code} error with your search: {response["error"]["message"]} ({response["error"]["code"]})")

def find_album():
    link = "https://www.pinterest.com/resource/BoardsResource/get/?data={\"options\":{\"username\":\"" + username + "\"}}"
    req = requests.get(url=link, cookies={"_pinterest_sess": cookie}, timeout=5)
    response = req.json()["resource_response"]

    if (req.status_code == 200):
        for alb in response["data"]:
            if (alb["name"].lower() == album):
                get_album(id=alb["id"])
                return

        print("Album wasn't found")
    else:
        print(f"There was a {req.status_code} error with your search: {response["error"]["message"]} ({response["error"]["code"]})")

username = input("Insert your Pinterest username: ").lower()
album = input("Insert your Pinterest albums name: ").lower()
cookie = input("Insert your \"_pinterest_sess\" cookie (Can be left empty): ")

if (album == "pins"):
    get_pins()
else:
    find_album()