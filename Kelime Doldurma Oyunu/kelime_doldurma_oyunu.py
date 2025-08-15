import tkinter as tk

def hikaye_olustur():
    isim1 = girdi_isim1.get()
    fiil1 = girdi_fiil1.get()
    isim2 = girdi_isim2.get()
    fiil2 = girdi_fiil2.get()
    sifat1 = girdi_sifat1.get()

    hikaye = f"""
Bir varmış bir yokmuş, uzak diyarların birinde, {sifat1} bir {isim1} yaşarmış. Bu {isim1}'ın en sevdiği şey bütün gün {fiil1} yapmakmış.

Bir gün, kapı gıcırdamış ve içeri {isim2} girmiş. {isim2}, {isim1}'ı tam da {fiil1} yaparken görünce gözlerine inanamamış.

{isim2}: "Hayrola, ne yapıyorsun böyle?"
{isim1}: "Hiç ya, öyle {fiil1} yapıyordum. Neden bu kadar şaşırdın?"
{isim2}: "Böyle {fiil1} yaparken seni hiç görmemiştim. Çok {sifat1} görünüyorsun!"
{isim1}: "Haklısın valla. En iyisi bir mola vereyim."
{isim2}: "Aklın yolu bir! Gel de biz de biraz {fiil2} yapalım."
{isim1}: "Durur muyum? Hadi gidelim, çok iyi olur!"

Ve böylece, {isim2} ile {isim1}, {fiil2} yapmaya gitmişler.
Gökten üç elma düşmüş; biri hikayeyi anlatanın başına, biri bu oyunu oynayanın başına, biri de bu hikayeyi dinleyenlerin başına.
"""
    hikaye_metni.delete("1.0", tk.END)
    hikaye_metni.insert(tk.END, hikaye)

ana_pencere = tk.Tk()
ana_pencere.title("Kelime Oyunu")
ana_pencere.geometry("650x550")

giris_cercevesi = tk.Frame(ana_pencere, padx=10, pady=10)
giris_cercevesi.pack()

tk.Label(giris_cercevesi, text="Bir isim girin:").grid(row=0, column=0, sticky="w", pady=5)
girdi_isim1 = tk.Entry(giris_cercevesi)
girdi_isim1.grid(row=0, column=1)

tk.Label(giris_cercevesi, text="Bir fiil girin (geniş zaman):").grid(row=1, column=0, sticky="w", pady=5)
girdi_fiil1 = tk.Entry(giris_cercevesi)
girdi_fiil1.grid(row=1, column=1)

tk.Label(giris_cercevesi, text="Bir isim girin:").grid(row=2, column=0, sticky="w", pady=5)
girdi_isim2 = tk.Entry(giris_cercevesi)
girdi_isim2.grid(row=2, column=1)

tk.Label(giris_cercevesi, text="Bir fiil girin (geniş zaman):").grid(row=3, column=0, sticky="w", pady=5)
girdi_fiil2 = tk.Entry(giris_cercevesi)
girdi_fiil2.grid(row=3, column=1)

tk.Label(giris_cercevesi, text="Bir sıfat girin:").grid(row=4, column=0, sticky="w", pady=5)
girdi_sifat1 = tk.Entry(giris_cercevesi)
girdi_sifat1.grid(row=4, column=1)

olustur_butonu = tk.Button(ana_pencere, text="Hikayeyi Oluştur", command=hikaye_olustur)
olustur_butonu.pack(pady=10)

hikaye_metni = tk.Text(ana_pencere, wrap="word", height=20, width=65)
hikaye_metni.pack(padx=10, pady=10)

ana_pencere.mainloop()