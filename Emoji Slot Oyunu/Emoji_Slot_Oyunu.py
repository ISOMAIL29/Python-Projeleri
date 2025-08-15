import tkinter as tk
import random

class EmojiSlotOyunu:
    def __init__(self, ana_pencere):
        self.ana_pencere = ana_pencere
        self.ana_pencere.title("Emoji Slot Makinesi")
        self.ana_pencere.geometry("400x250")
        self.ana_pencere.configure(bg="#2c3e50")

        self.secenekler = ("😊", "😎", "😂")
        
        self.cerceve = tk.Frame(ana_pencere, bg="#2c3e50")
        self.cerceve.pack(expand=True)

        self.emoji_etiketleri = []
        for _ in range(3):
            etiket = tk.Label(self.cerceve, text="?", font=("Segoe UI Emoji", 50), bg="#2c3e50", fg="#ecf0f1")
            etiket.pack(side=tk.LEFT, padx=10)
            self.emoji_etiketleri.append(etiket)

        self.geri_bildirim_etiketi = tk.Label(ana_pencere, text="Hadi Oynayalım!", font=("Arial", 16), bg="#2c3e50", fg="#ecf0f1")
        self.geri_bildirim_etiketi.pack(pady=10)

        self.cevirme_butonu = tk.Button(ana_pencere, text="Çevir", font=("Arial", 14, "bold"), bg="#e74c3c", fg="#ecf0f1", activebackground="#c0392b", command=self.cevirmeyi_baslat)
        self.cevirme_butonu.pack(pady=10, ipadx=20)
        
    def cevirmeyi_baslat(self):
        self.cevirme_butonu.config(state=tk.DISABLED)
        self.geri_bildirim_etiketi.config(text="")
        
        emojiler = [random.choice(self.secenekler) for _ in range(3)]
        
        for i, emoji in enumerate(emojiler):
            self.emoji_etiketleri[i].config(text=emoji)

        if emojiler[0] == emojiler[1] == emojiler[2]:
            self.geri_bildirim_etiketi.config(text="Tebrikler! Kazandın!", fg="#2ecc71")
        else:
            self.geri_bildirim_etiketi.config(text="Üzgünüm, kaybettin.", fg="#e74c3c")

        self.cevirme_butonu.config(state=tk.NORMAL)

if __name__ == "__main__":
    ana_pencere = tk.Tk()
    uygulama = EmojiSlotOyunu(ana_pencere)
    ana_pencere.mainloop()