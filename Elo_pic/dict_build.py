import json
import os

abs_route = os.path.abspath(__file__)
route = os.path.dirname(abs_route)
route_pictures = os.path.join(route, "Pictures")
route_elo_score = os.path.join(route, "files", "Elo score.json")

dictionnaire = {}

def dic_create():
    for nom in os.listdir(route_pictures):
        file = os.path.join(route_pictures, nom)
        if os.path.isfile(file) :
            dictionnaire[nom] = 1000
        else:
            print("impossible de trouver le dossier")

dic_create()
with open(route_elo_score, "w") as f:
    json.dump(dictionnaire, f, indent=4)