#### IMPORT FOR CLASSIC POKEMON CLASS ####
from random import randint
from math import *
from flask import Flask, render_template, request
####  IMPORT FOR API REQUEST IMAGES #### 
import requests
from PIL import Image
import PIL  
from io import BytesIO

app = Flask("Ma Super App")


class Pokemon:
    def __init__(self, nm: str, pv: int, at: int, de: int, vi: int, ex: int):
        assert type(nm) == str and (type(pv) == int and pv > 0) and (type(at) == int and at > 0) and (
            type(de) == int and de > 0) and (type(vi) == int and vi > 0) and (type(ex) == int and ex > 0)

        self.nm = nm
        self.pv = pv
        self.at = at
        self.de = de
        self.vi = vi
        self.ex = ex

    def set_nm(self, nm):
        self.nm = nm

    def set_pv(self, pv):
        self.pv = pv

    def set_at(self, at):
        self.at = at

    def set_de(self, de):
        self.de = de

    def set_ex(self, ex):
        self.ex = ex

    def set_vi(self, vi):
        self.vi = vi

    def info(self):
        print(f"Nom : {self.nm}")
        print(f"Points de vie : {self.pv}")
        print(f"Attaque : {self.at}")
        print(f"Défense : {self.de}")
        print(f"Vitesse : {self.vi}")
        print(f"Expérience : {self.ex}")

    def attaquer(self, poke):
        # print(f"############# ATTAQUE DE {self.nm}##########")
        alea = randint(1, 6)
        if alea % 2 == 0:
            assaut = (self.at + alea)*(self.ex/100)
        else:
            assaut = (self.at - alea)*(self.ex/100)

        # print(f"Valeur de assaut {assaut}")
        if assaut > poke.de:
            poke.pv = poke.pv-floor(assaut-poke.de)
            print(
                f"{self.nm} inflige {floor(assaut-poke.de)} dégâts à son adversaire {poke.nm}")
            # print(f"Valeur de l'attaque {floor(assaut-poke.de)}")
        else:
            print(f"{self.nm} est contrée par son adversaire {poke.nm}")

        return(poke.pv, self)

    def main(self, poke2):

        poke1 = self
        if poke1.vi < poke2.vi:
            poke1, poke2 = poke2, poke1
        elif (poke2.vi == poke1.vi) and (randint(1, 2) == 1):
            poke1, poke2 = poke2, poke1

        print(f"Début du combat : le pokémon {poke1.nm} commence")

        for i in range(0, 5):
            # print("\n----------------\n")
            # print(f"{poke1.nm} a {poke1.pv} points de vies")
            # print(f"{poke2.nm} a {poke2.pv} points de vies")
            if poke1.attaquer(poke2)[0] <= 0:
                print(f"{poke2.nm} a perdu le combat")
                print(f"{poke1.nm} gagne, il lui reste {poke1.pv} point(s) de vie")
                return("END")
            else:
                poke1, poke2 = poke2, poke1

    def levotre(self):
        self.nm = str(input("Entrez le nom de votre pokémon : "))
        self.pv = input(f"Entrez le nombre de points de vie de {self.nm}: ")
        self.at = input(f"Entrez le nombre de points d'attaque de {self.nm}: ")
        self.de = input(
            f"Entrez le nombre de points de défense de {self.nm}: ")
        self.vi = input(
            f"Entrez le nombre de points de vitesse de {self.nm}: ")
        self.ex = input(
            f"Entrez le nombre de points d'expérience de {self.nm}: ")


dracau = Pokemon("Dracaufeu", 78, 84, 78, 100, 80)
flamia = Pokemon("Flamiaou", 45, 65, 40, 70, 80)

# dracau.info()
# flamia.info()

# dracau.main(flamia)

##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################



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
    return str("/static/"+pokemon+".png")
    # img.show()

 


# @app.route('/')
def page():
    data = []
    pokemon1 = {"nm": "Dracaufeu",
                "pv": "65",
                "at": "65",
                "de": "65",
                "vi": "65",
                "ex": "65"}
    pokemon2 = {"nm": "Pickachu",
                "pv": "65",
                "at": "65",
                "de": "65",
                "vi": "65",
                "ex": "65"}

    data.append(pokemon1)
    data.append(pokemon2)

    return render_template('index.html', data=data)


@app.route('/form')
def form():
    return render_template('form.html')


# @app.route('/data/', methods=['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        # text = request.form["nm"]
        # processed_text = text.upper()
        # return processed_text
        form_data = request.form
        pokeimage = getpokeimage(form_data["Nom du pokémon"])


        pokedata = []
        for key, values in form_data.items() :
            pokedata[key].append(values)

        print(pokedata)


        return render_template('data.html',form_data = form_data, pokeimage = pokeimage)

@app.route('/data/', methods=['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        # text = request.form["nm"]
        # processed_text = text.upper()
        # return processed_text
        
        form_data = request.form
        # pokeimage = getpokeimage(form_data["nm"])

        pokedata = dict()
        for key, values in form_data.items() :
            # print("clé : ", key)
            # print("donnée : ", values)
            pokedata[key] = values

        pokedata["img"] = getpokeimage(pokedata["nm"])

        print(pokedata)
        list_pokemons = []
        list_pokemons.append(pokedata)

        return render_template('main.html',pokemons = list_pokemons)


dracaufeu_img = getpokeimage("charizard")


@app.route('/')
def main():
    list_pokemons = []
    pokemon = {"nm": "Pickachu",
                "img" : "/static/pikachu.png",
                "pv": "15",
                "at": "15",
                "de": "15",
                "vi": "15",
                "ex": "15"}
    list_pokemons.append(pokemon)
    pokemon = {"nm": "Dracaufeu",
                "img" : "/static/charizard.png",
                "pv": "30",
                "at": "30",
                "de": "30",
                "vi": "30",
                "ex": "30"}
    list_pokemons.append(pokemon)

    
    return render_template('main.html', pokemons = list_pokemons)
        

app.run(host='0.0.0.0', port=2768)

