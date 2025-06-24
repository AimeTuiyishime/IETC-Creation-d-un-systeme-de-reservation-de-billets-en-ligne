import tkinter as tk
from package.package_class_additionnel import Paiement

paiement = None  # ✅ Déclaré ici pour être accessible partout

def test_paiement():
    global paiement
    paiement = Paiement(1, 123, 50.0)
    if paiement.effectuerPaiement():
        result.set("Paiement effectué avec succès.")
    else:
        result.set("Paiement déjà effectué.")

def rembourser():
    if paiement and paiement.statutPaiement == "Payé":
        paiement.rembourserPaiement()
        result.set("Paiement remboursé.")
    else:
        result.set("Impossible de rembourser.")

# Interface minimaliste
root = tk.Tk()
root.title("Test Paiement")

result = tk.StringVar()

btn_payer = tk.Button(root, text="Effectuer Paiement", command=test_paiement)
btn_payer.pack(pady=10)

btn_rembourser = tk.Button(root, text="Rembourser", command=rembourser)
btn_rembourser.pack(pady=10)

label_result = tk.Label(root, textvariable=result)
label_result.pack(pady=10)

root.mainloop()

