from PIL import Image, ImageTk
import tkinter as tk
import random as rd
import json
import os

#chemins de fichiers
abs_route = os.path.abspath(__file__)
route = os.path.dirname(abs_route)
route_pictures = os.path.join(route, "Pictures")
route_elo_score = os.path.join(route, "files", "Elo score.json")
route_config = os.path.join(route, "files", "config.json")
liste_images = os.listdir(route_pictures)

#lecture du fichier elo
with open(route_elo_score, "r") as file:
    dictionnaire_images = json.load(file)
with open(route_config, "r") as file:
    dictionnaire_config = json.load(file)

#classe
class participant :
    def __init__(self, nom, elo, result, proba = 0):
        self.nom = nom
        self.elo = elo
        self.result = result
        self.proba = proba

#coefficient de mouvement du classement elo
coef = 32

#logique
def top3():
    global top_3
    top_3 = [cle for cle, valeur in sorted(dictionnaire_images.items(), key=lambda x: x[1], reverse=True)][:3]
def prob(itself, oppo):
    return 1 / (1 + 10 ** ((oppo - itself) / 400))
def new_elo():
    image1.elo = image1.elo + coef * (image1.result - image1.proba)
    image2.elo = image2.elo + coef * (image2.result - image2.proba)
    dictionnaire_images[first_challenger] = image1.elo
    dictionnaire_images[second_challenger] = image2.elo
def winner_calcul(winn, looser):
    winn.result = 1
    looser.result = 0
    bouton1.pack_forget()
    bouton2.pack_forget()
def reset_game():
    global image1, image2, first_challenger, second_challenger
    first_challenger = rd.choice(liste_images)
    second_challenger = rd.choice(liste_images)
    if second_challenger == first_challenger:
        while True:
            second_challenger = rd.choice(liste_images)
            if second_challenger != first_challenger:
                break
    image1 = participant(first_challenger, dictionnaire_images[first_challenger],  0, 0)
    image2 = participant(second_challenger, dictionnaire_images[second_challenger], 0, 0)
    image1.proba = prob(image1.elo, image2.elo)
    image2.proba = prob(image2.elo, image1.elo)
    widgets_choix()
    interface_choix()
def new_party(winn, looser):
    winner_calcul(winn, looser)
    new_elo()
    reset_game()
def save_scores():
    global dictionnaire_images, dictionnaire_config
    with open(route_elo_score, "w") as file:
        json.dump(dictionnaire_images, file, indent=4)
    with open(route_config, "w") as file:
        json.dump(dictionnaire_config, file, indent=4)
        fenetre.destroy()
        print("files saved")

#interface graphique
liste_theme = [cle for cle, valeur in dictionnaire_config["fenetre_theme"].items()]
def get_listbox_selected(event):
    result = listbox.curselection()
    if result :
        index = result[0]
        result = listbox.get(index)
        dictionnaire_config["chosen_theme"] = result
        interface_choix()
        fenetre.config(background=fenetre_couleurs("background"))

def fenetre_couleurs(request):
    theme = dictionnaire_config["chosen_theme"]
    if request == "background":
        return dictionnaire_config["fenetre_theme"][theme]["background"]
    elif request == "text":
        return dictionnaire_config["fenetre_theme"][theme]["text"]
    elif request == "button":
        return dictionnaire_config["fenetre_theme"][theme]["button"]
    else:
        print("pas de couleur définie pour cette requête")
def open_image(image, action):
    if action == "openimage":
        theimage = Image.open(os.path.join(route_pictures, image))
        theimage_width, theimage_height = theimage.size
        theimage = resize_image(theimage_width, theimage_height, theimage)
        return theimage

def resize_image(image_width, image_height, image_display, max_size=500):
    zoom_factor = min(max_size / image_width, max_size / image_height)
    new_height = int(image_height * zoom_factor)
    new_width = int(image_width * zoom_factor)
    return image_display.resize((new_width, new_height), Image.Resampling.LANCZOS)
fenetre = tk.Tk()
fenetre.config(background=fenetre_couleurs("background"))
fenetre.geometry("1600x720")
fenetre.title("Elo_scores.py")
def widgets_result():
    global frame1_result_image, frame2_result_image, frame3_result_image, frame1_result_info, frame2_result_info, frame3_result_info, image1_PhotoImage_info, image2_PhotoImage_info, image3_PhotoImage_info
    top3()
    frame1_result_image = tk.Frame(fenetre, bg=fenetre_couleurs("background"))
    frame2_result_image = tk.Frame(fenetre, bg=fenetre_couleurs("background"))
    frame3_result_image = tk.Frame(fenetre, bg=fenetre_couleurs("background"))
    frame1_result_info = tk.Frame(fenetre, bg=fenetre_couleurs("background"))
    frame2_result_info = tk.Frame(fenetre, bg=fenetre_couleurs("background"))
    frame3_result_info = tk.Frame(fenetre, bg=fenetre_couleurs("background"))

    image1_display = open_image(top_3[0], "openimage")
    image2_display = open_image(top_3[1], "openimage")
    image3_display = open_image(top_3[2], "openimage")
    image1_PhotoImage_info = ImageTk.PhotoImage(image1_display)
    image2_PhotoImage_info = ImageTk.PhotoImage(image2_display)
    image3_PhotoImage_info = ImageTk.PhotoImage(image3_display)

    image1_result_label = tk.Label(frame1_result_image, image=image1_PhotoImage_info, background=fenetre_couleurs("background"))
    image2_result_label = tk.Label(frame2_result_image, image=image2_PhotoImage_info, background=fenetre_couleurs("background"))
    image3_result_label = tk.Label(frame3_result_image, image=image3_PhotoImage_info, background=fenetre_couleurs("background"))
    bouton1 = tk.Button(frame2_result_info, text="Retour au jeu", font=("Arial", 20), bg=fenetre_couleurs("button"), fg=fenetre_couleurs("text"), command=interface_choix)
    texte_1 = tk.Label(frame1_result_info, text=f"Votre image préférée : {top_3[0]}", font=("Arial", 15), bg=fenetre_couleurs("background"), fg=fenetre_couleurs("text"))
    texte_2 = tk.Label(frame2_result_info, text=f"Votre top 2 : {top_3[1]}", font=("Arial", 15), bg=fenetre_couleurs("background"), fg=fenetre_couleurs("text"))
    texte_3 = tk.Label(frame3_result_info, text=f"Votre top 3 : {top_3[2]}", font=("Arial", 15), bg=fenetre_couleurs("background"), fg=fenetre_couleurs("text"))

    texte_1.pack(expand=True)
    bouton1.pack(expand=True, side="top")
    texte_2.pack(expand=True)
    texte_3.pack(expand=True)
    image1_result_label.pack(expand=True)
    image2_result_label.pack(expand=True)
    image3_result_label.pack(expand=True)

def widgets_choix():
    global frame1_choix, frame2_choix, frame3_choix, frame4_choix, image1_PhotoImage_choix, image2_PhotoImage_choix, bouton1, bouton2, listbox
    image1_display = open_image(first_challenger, "openimage")
    image2_display = open_image(second_challenger, "openimage")
    image1_PhotoImage_choix= ImageTk.PhotoImage(image1_display)
    image2_PhotoImage_choix = ImageTk.PhotoImage(image2_display)

    frame1_choix = tk.Frame(fenetre, background=fenetre_couleurs("background"))
    frame2_choix = tk.Frame(fenetre, background=fenetre_couleurs("background"))
    frame3_choix = tk.Frame(fenetre, background=fenetre_couleurs("background"))
    frame4_choix = tk.Frame(fenetre, background=fenetre_couleurs("background"))

    texte_jeu = tk.Label(frame3_choix, text="Je choisis :", font=("Arial", 25), bg=fenetre_couleurs("background"), fg=fenetre_couleurs("text"))
    image1_label = tk.Label(frame1_choix, image=image1_PhotoImage_choix, background=fenetre_couleurs("background"))
    image2_label = tk.Label(frame2_choix, image=image2_PhotoImage_choix, background=fenetre_couleurs("background"))
    bouton1 = tk.Button(frame3_choix, text="Gauche", font=("Arial", 20), bg=fenetre_couleurs("button"), fg=fenetre_couleurs("text"), command=lambda: new_party(image1, image2))
    bouton2 = tk.Button(frame3_choix, text="Droite", font=("Arial", 20), bg=fenetre_couleurs("button"), fg=fenetre_couleurs("text"), command=lambda: new_party(image2, image1))
    bouton4 = tk.Button(frame3_choix, text="Votre top", font=("Arial", 20), bg=fenetre_couleurs("button"), fg=fenetre_couleurs("text"), command=interface_result)
    titre_listbox = tk.Label(frame4_choix, text="Thème : ", font=("Arial", 15), bg=fenetre_couleurs("background"), fg=fenetre_couleurs("text"))
    listbox = tk.Listbox(frame4_choix, font=("Arial", 15), bg=fenetre_couleurs("background"), fg=fenetre_couleurs("text"))
    for element in liste_theme :
        listbox.insert(tk.END, element)
    listbox.bind("<<ListboxSelect>>", get_listbox_selected)

    image2_label.pack(expand=True, fill="both")
    image1_label.pack(expand=True, fill="both")
    bouton4.pack()
    texte_jeu.pack(expand=True, fill="both")
    bouton1.pack(side="left")
    bouton2.pack(side="right")
    titre_listbox.pack()
    listbox.pack(side="bottom")

    fenetre.grid_columnconfigure(2, weight=0, minsize=535)
    fenetre.grid_columnconfigure(0, weight=0, minsize=25)

def erase_every():
    for widget in fenetre.winfo_children():
        widget.grid_forget()
def interface_result():
    erase_every()
    widgets_result()
    frame1_result_info.grid(row=0, column=0, sticky="nsew")
    frame2_result_info.grid(row=0, column=1, sticky="nsew")
    frame3_result_info.grid(row=0, column=2, sticky="nsew")
    frame1_result_image.grid(row=1, column=0, sticky="nsew")
    frame2_result_image.grid(row=1, column=1, sticky="nsew")
    frame3_result_image.grid(row=1, column=2, sticky="nsew")

def interface_choix():
    erase_every()
    widgets_choix()
    frame1_choix.grid(row=0, column=1, sticky="nsew")
    frame2_choix.grid(row=0, column=4, sticky="e")
    frame3_choix.grid(row=0, column=2, sticky="nsew")
    frame4_choix.grid(row=1, column=2, sticky="nsew")

reset_game()
widgets_choix()
interface_choix()
fenetre.protocol("WM_DELETE_WINDOW", save_scores)
fenetre.mainloop()