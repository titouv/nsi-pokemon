import requests
from PIL import Image
import PIL  
from io import BytesIO


def getpokeimage(name):

    # pokemon = input("Rentrez le nom de votre pokémon : ")
    pokemon = name

    url1 = "https://pokeapi.co/api/v2/pokemon/"+str(pokemon)


    response = requests.get(url1)
    pokeid = response.json()["id"]

    url = "https://pokeres.bastionbot.org/images/pokemon/"+str(pokeid)+".png"

    responsepoke = requests.get(url)


    img = Image.open(BytesIO(responsepoke.content))
    img = img.convert("RGBA")
    img2 = img.save(str("static/"+pokemon+".png"))
    # img.show()

 