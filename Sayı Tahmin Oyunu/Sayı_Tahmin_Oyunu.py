import tkinter as tk
import random

class SayiTahminOyunu:
    def __init__(self, root):
        self.root = root
        self.root.title("Sayı Tahmin Oyunu")
        self.root.geometry("400x300")
        
        # Enter tuşunu pencereye bağlama
        self.root.bind("<Return>", self.enter_tusa_basma)

        self.hedef_sayi = random.randint(1, 100)

        self.etiket = tk.Label(root, text="1 ile 100 arasında bir sayı tahmin et:")
        self.etiket.pack(pady=10)

        self.tahmin_kutusu = tk.Entry(root)
        self.tahmin_kutusu.pack(pady=5)
        self.tahmin_kutusu.focus_set() # Uygulama açıldığında imleci buraya odaklar

        self.buton = tk.Button(root, text="Tahmin Et", command=self.tahmini_kontrol_et)
        self.buton.pack(pady=5)

        self.geri_bildirim = tk.Label(root, text="")
        self.geri_bildirim.pack(pady=10)

        self.yeni_oyun_butonu = tk.Button(root, text="Yeni Oyun", command=self.yeni_oyun)
        
    def enter_tusa_basma(self, event):
        # Eğer Tahmin Et butonu aktifse, tahmini kontrol et
        if self.buton["state"] == "normal":
            self.tahmini_kontrol_et()
        # Eğer Tahmin Et butonu pasifse (oyun kazanılmış), yeni oyun başlat
        elif self.buton["state"] == "disabled":
            self.yeni_oyun()

    def tahmini_kontrol_et(self):
        try:
            tahmin = int(self.tahmin_kutusu.get())
        except ValueError:
            self.geri_bildirim.config(text="Geçerli bir sayı girin.")
            return

        fark = abs(self.hedef_sayi - tahmin)
        
        if tahmin == self.hedef_sayi:
            self.geri_bildirim.config(text=f"Tebrikler! Doğru tahmin ettin: {self.hedef_sayi}")
            self.buton.config(state="disabled")
            self.yeni_oyun_butonu.pack(pady=10)
        elif fark <= 5:
            self.geri_bildirim.config(text="Çok Sıcak!")
        elif fark <= 15:
            self.geri_bildirim.config(text="Sıcak!")
        elif fark <= 30:
            self.geri_bildirim.config(text="Ilık.")
        else:
            self.geri_bildirim.config(text="Soğuk.")
        
        self.tahmin_kutusu.delete(0, tk.END)

    def yeni_oyun(self):
        self.hedef_sayi = random.randint(1, 100)
        self.tahmin_kutusu.delete(0, tk.END)
        self.geri_bildirim.config(text="")
        self.buton.config(state="normal")
        self.yeni_oyun_butonu.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    oyun = SayiTahminOyunu(root)
    root.mainloop()
