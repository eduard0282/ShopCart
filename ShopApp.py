import tkinter as tk
import json
import tkinter.messagebox

def adauga_produs():
    produs = produs_entry.get()
    cantitate = cantitate_entry.get()

    # Verificăm dacă câmpul de introducere pentru produs nu este gol
    if produs:
        # Creăm un dicționar cu informațiile noului produs
        produs_nou = {"produs": produs, "cantitate": cantitate}

        # Încărcăm datele existente din fișierul JSON (dacă există)
        try:
            with open("lista_cumparaturi.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        # Adăugăm noul produs în lista de cumpărături
        data.append(produs_nou)

        # Serializăm și stocăm datele în format JSON
        with open("lista_cumparaturi.json", "w") as file:
            json.dump(data, file)

        # Afișăm un mesaj de confirmare
        tk.messagebox.showinfo("Info", f"Produsul '{produs}' a fost adăugat în listă.")

        # Ștergem conținutul câmpurilor de introducere după adăugare
        produs_entry.delete(0, tk.END)
        cantitate_entry.delete(0, tk.END)
    else:
        # Afișăm un mesaj de eroare dacă câmpul de introducere pentru produs este gol
        tk.messagebox.showerror("Eroare", "Introduceți un nume de produs.")

def afiseaza_lista():
    try:
        with open("lista_cumparaturi.json", "r") as file:
            data = json.load(file)

        lista_window = tk.Toplevel(root)
        lista_window.title("Lista de cumpărături")

        lista_window.geometry(root.geometry())

        lista_box = tk.Listbox(lista_window, selectmode=tk.MULTIPLE, font=("Helvetica", 12))
        lista_box.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        for produs in data:
            lista_box.insert(tk.END, f"{produs['produs']}: {produs['cantitate']}")

        def sterge_selectate():
            selected_indices = lista_box.curselection()
            if selected_indices:
                selected_indices = list(selected_indices)
                selected_indices.sort(reverse=True)
                for index in selected_indices:
                    data.pop(index)

                with open("lista_cumparaturi.json", "w") as file:
                    json.dump(data, file)

                lista_box.delete(0, tk.END)
                for produs in data:
                    lista_box.insert(tk.END, f"{produs['produs']}: {produs['cantitate']}")

        sterge_button = tk.Button(lista_window, text="Șterge selectate", command=sterge_selectate, font=("Helvetica", 12))
        sterge_button.pack(pady=10)
    except FileNotFoundError:
        tk.messagebox.showinfo("Lista de cumpărături", "Lista este goală.")

root = tk.Tk()
root.title("Lista de cumpărături")
root.geometry("450x300")

titlu_label = tk.Label(root, text="Lista de cumpărături", font=("Helvetica", 20))
titlu_label.pack()

adauga_cadru = tk.Frame(root)
adauga_cadru.pack(pady=10)

produs_label = tk.Label(adauga_cadru, text="Produs:", font=("Helvetica", 12))
produs_label.grid(row=0, column=0, sticky="e")
produs_entry = tk.Entry(adauga_cadru, font=("Helvetica", 12))
produs_entry.grid(row=0, column=1, padx=5, pady=5)

cantitate_label = tk.Label(adauga_cadru, text="Cantitate:", font=("Helvetica", 12))
cantitate_label.grid(row=1, column=0, sticky="e")

# Textbox "Cantitate:" fără validare
cantitate_entry = tk.Entry(adauga_cadru, font=("Helvetica", 12))
cantitate_entry.grid(row=1, column=1, padx=5, pady=5)

adauga_button = tk.Button(adauga_cadru, text="Adaugă", command=adauga_produs, font=("Helvetica", 12))
adauga_button.grid(row=2, columnspan=2, pady=10)

afiseaza_button = tk.Button(root, text="Afișează lista", command=afiseaza_lista, font=("Helvetica", 12))
afiseaza_button.pack(pady=10)

root.mainloop()
