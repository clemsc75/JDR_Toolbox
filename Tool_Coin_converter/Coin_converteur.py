import tkinter as tk
from tkinter import filedialog
import json
from PIL import Image, ImageTk

data = {}
pieces = ["Ouvrir fichier de taux de conversion", "Ouvrir fichier de taux de conversion"]

def get_pieces_from_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return list(data.keys())

def convertir_monnaie():
    global data
    try:
        montant_str = entry_var1.get()
        if not montant_str.strip():
            label_texte.config(text="Valeur après conversion")
            return
        montant = float(montant_str)
        piece_gauche = var1.get()
        piece_droite = var2.get()
        if not data or piece_gauche not in data or piece_droite not in data[piece_gauche]:
            label_texte.config(text="Erreur de conversion")
            return
        taux = data[piece_gauche][piece_droite]
        resultat = montant * taux
        label_texte.config(text=f"{resultat:.2f}")
    except Exception:
        label_texte.config(text="Erreur de conversion")

def choisir_fichier_json():
    global pieces, data
    filepath = filedialog.askopenfilename(
        title="Choisir un fichier JSON",
        filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")]
    )
    if filepath:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        pieces = list(data.keys())
        menu1['menu'].delete(0, 'end')
        menu2['menu'].delete(0, 'end')
        for piece in pieces:
            menu1['menu'].add_command(label=piece, command=tk._setit(var1, piece))
            menu2['menu'].add_command(label=piece, command=tk._setit(var2, piece))
        var1.set(pieces[0])
        var2.set(pieces[1])

def set_background_image(fenetre, image_path):
    def resize_bg(event=None):
        img = Image.open(image_path)
        img = img.resize((fenetre.winfo_width(), fenetre.winfo_height()), Image.Resampling.LANCZOS)
        bg_img = ImageTk.PhotoImage(img)
        background_label.config(image=bg_img)
        background_label.image = bg_img  # Garde la référence

    img = Image.open(image_path)
    img = img.resize((fenetre.winfo_width(), fenetre.winfo_height()), Image.Resampling.LANCZOS)
    bg_img = ImageTk.PhotoImage(img)
    background_label = tk.Label(fenetre, image=bg_img)
    background_label.image = bg_img
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    fenetre.bind("<Configure>", resize_bg)

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Convertisseur de pièces")

set_background_image(fenetre, "Parchemin_img.jpg")

label = tk.Label(fenetre, text="Bienvenue dans le convertisseur de pièces !")
label.pack(padx=20, pady=10)

frame_main = tk.Frame(fenetre)
frame_main.pack(padx=20, pady=10)

# Colonne gauche
frame_left = tk.Frame(frame_main)
frame_left.pack(side=tk.LEFT, padx=5)
var1 = tk.StringVar(fenetre)
var1.set(pieces[0])
menu1 = tk.OptionMenu(frame_left, var1, *pieces)
menu1.pack(pady=2)
entry_var1 = tk.StringVar()
entry1 = tk.Entry(frame_left, textvariable=entry_var1, width=10)
entry1.pack(pady=2)

# Séparateur
label_arrow = tk.Label(frame_main, text="=>")
label_arrow.pack(side=tk.LEFT, padx=10)

# Colonne droite
frame_right = tk.Frame(frame_main)
frame_right.pack(side=tk.LEFT, padx=5)
var2 = tk.StringVar(fenetre)
var2.set(pieces[1])
menu2 = tk.OptionMenu(frame_right, var2, *pieces)
menu2.pack(pady=2)
label_texte = tk.Label(frame_right, text="Valeur après conversion")
label_texte.pack(pady=2)

# Ajout des traces pour la conversion automatique
entry_var1.trace_add("write", lambda *args: convertir_monnaie())
var1.trace_add("write", lambda *args: convertir_monnaie())
var2.trace_add("write", lambda *args: convertir_monnaie())

# Bouton pour choisir le fichier JSON
btn_choisir = tk.Button(fenetre, text="Choisir un fichier de taux de conversion", command=choisir_fichier_json)
btn_choisir.pack(pady=10)

fenetre.mainloop()