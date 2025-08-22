import tkinter as tk
import random

class LabirentOyunu:
    def __init__(self, ana_pencere, satir_sayisi, sutun_sayisi, hucre_boyutu):
        self.ana_pencere = ana_pencere
        self.satir_sayisi = satir_sayisi
        self.sutun_sayisi = sutun_sayisi
        self.hucre_boyutu = hucre_boyutu
        self.canvas = tk.Canvas(ana_pencere, width=sutun_sayisi * hucre_boyutu, height=satir_sayisi * hucre_boyutu, bg='blue')
        self.canvas.pack()

        self.baslangic_konumu = (0, 0)
        self.bitis_konumu = (satir_sayisi - 1, sutun_sayisi - 1)
        self.oyuncu_konumu = self.baslangic_konumu
        self.oyuncu_yolu = [self.baslangic_konumu]
        self.yeniden_baslat_butonu = None
        self.is_surukleme = False

        self.labirenti_olustur()
        self.labirenti_ciz()
        self.oyuncuyu_ciz()
        
        # Sürükle-bırak için olayları bağla
        self.canvas.bind('<Button-1>', self.fare_basildi)
        self.canvas.bind('<B1-Motion>', self.surukle)
        self.canvas.bind('<ButtonRelease-1>', self.fare_birakildi)

    def labirenti_olustur(self):
        self.izgara = [[{'duvarlar': {'ust': True, 'sag': True, 'alt': True, 'sol': True}, 'ziyaret_edildi': False} for _ in range(self.sutun_sayisi)] for _ in range(self.satir_sayisi)]
        yigin = []
        mevcut_hucre = (0, 0)
        self.izgara[mevcut_hucre[0]][mevcut_hucre[1]]['ziyaret_edildi'] = True
        yigin.append(mevcut_hucre)

        while yigin:
            mevcut_hucre = yigin[-1]
            ziyaret_edilmemis_komsular = self.ziyaret_edilmemis_komsulari_al(mevcut_hucre)

            if ziyaret_edilmemis_komsular:
                yon, sonraki_hucre = random.choice(ziyaret_edilmemis_komsular)
                self.duvarlari_kaldir(mevcut_hucre, sonraki_hucre, yon)
                self.izgara[sonraki_hucre[0]][sonraki_hucre[1]]['ziyaret_edildi'] = True
                yigin.append(sonraki_hucre)
            else:
                yigin.pop()

        self.rastgele_yollar_ekle()

    def rastgele_yollar_ekle(self):
        # Labirentin rastgele %17'sinde duvarları kaldırır, böylelikle çatallanma olur.
        acik_hucre_sayisi = int(self.satir_sayisi * self.sutun_sayisi * 0.17)
        for _ in range(acik_hucre_sayisi):
            r = random.randint(0, self.satir_sayisi - 1)
            c = random.randint(0, self.sutun_sayisi - 1)
            
            # Rastgele bir yöndeki duvarı seçme işlemi
            yon = random.choice(['ust', 'sag', 'alt', 'sol'])
            
            if yon == 'ust' and r > 0:
                self.izgara[r][c]['duvarlar']['ust'] = False
                self.izgara[r - 1][c]['duvarlar']['alt'] = False
            elif yon == 'sag' and c < self.sutun_sayisi - 1:
                self.izgara[r][c]['duvarlar']['sag'] = False
                self.izgara[r][c + 1]['duvarlar']['sol'] = False
            elif yon == 'alt' and r < self.satir_sayisi - 1:
                self.izgara[r][c]['duvarlar']['alt'] = False
                self.izgara[r + 1][c]['duvarlar']['ust'] = False
            elif yon == 'sol' and c > 0:
                self.izgara[r][c]['duvarlar']['sol'] = False
                self.izgara[r][c - 1]['duvarlar']['sag'] = False

    def ziyaret_edilmemis_komsulari_al(self, hucre):
        komsular = []
        r, c = hucre
        if r > 0 and not self.izgara[r - 1][c]['ziyaret_edildi']:
            komsular.append(('ust', (r - 1, c)))
        if c < self.sutun_sayisi - 1 and not self.izgara[r][c + 1]['ziyaret_edildi']:
            komsular.append(('sag', (r, c + 1)))
        if r < self.satir_sayisi - 1 and not self.izgara[r + 1][c]['ziyaret_edildi']:
            komsular.append(('alt', (r + 1, c)))
        if c > 0 and not self.izgara[r][c - 1]['ziyaret_edildi']:
            komsular.append(('sol', (r, c - 1)))
        return komsular

    def duvarlari_kaldir(self, mevcut_hucre, sonraki_hucre, yon):
        r1, c1 = mevcut_hucre
        r2, c2 = sonraki_hucre
        
        if yon == 'ust':
            self.izgara[r1][c1]['duvarlar']['ust'] = False
            self.izgara[r2][c2]['duvarlar']['alt'] = False
        elif yon == 'sag':
            self.izgara[r1][c1]['duvarlar']['sag'] = False
            self.izgara[r2][c2]['duvarlar']['sol'] = False
        elif yon == 'alt':
            self.izgara[r1][c1]['duvarlar']['alt'] = False
            self.izgara[r2][c2]['duvarlar']['ust'] = False
        elif yon == 'sol':
            self.izgara[r1][c1]['duvarlar']['sol'] = False
            self.izgara[r2][c2]['duvarlar']['sag'] = False

    def labirenti_ciz(self):
        self.canvas.delete('all')
        for r in range(self.satir_sayisi):
            for c in range(self.sutun_sayisi):
                x1 = c * self.hucre_boyutu
                y1 = r * self.hucre_boyutu
                x2 = x1 + self.hucre_boyutu
                y2 = y1 + self.hucre_boyutu
                
                if self.izgara[r][c]['duvarlar']['ust']:
                    self.canvas.create_line(x1, y1, x2, y1, fill='white')
                if self.izgara[r][c]['duvarlar']['sag']:
                    self.canvas.create_line(x2, y1, x2, y2, fill='white')
                if self.izgara[r][c]['duvarlar']['alt']:
                    self.canvas.create_line(x1, y2, x2, y2, fill='white')
                if self.izgara[r][c]['duvarlar']['sol']:
                    self.canvas.create_line(x1, y1, x1, y2, fill='white')
        
        kucult = self.hucre_boyutu * 0.1
        baslangic_x1 = self.baslangic_konumu[1] * self.hucre_boyutu + kucult
        baslangic_y1 = self.baslangic_konumu[0] * self.hucre_boyutu + kucult
        baslangic_x2 = (self.baslangic_konumu[1] + 1) * self.hucre_boyutu - kucult
        baslangic_y2 = (self.baslangic_konumu[0] + 1) * self.hucre_boyutu - kucult
        self.canvas.create_rectangle(baslangic_x1, baslangic_y1, baslangic_x2, baslangic_y2, fill='lime', outline='')

        bitis_x1 = self.bitis_konumu[1] * self.hucre_boyutu + kucult
        bitis_y1 = self.bitis_konumu[0] * self.hucre_boyutu + kucult
        bitis_x2 = (self.bitis_konumu[1] + 1) * self.hucre_boyutu - kucult
        bitis_y2 = (self.bitis_konumu[0] + 1) * self.hucre_boyutu - kucult
        self.canvas.create_rectangle(bitis_x1, bitis_y1, bitis_x2, bitis_y2, fill='red', outline='')

    def oyuncuyu_ciz(self):
        self.canvas.delete('oyuncu')
        r, c = self.oyuncu_konumu
        x1 = c * self.hucre_boyutu + self.hucre_boyutu // 4
        y1 = r * self.hucre_boyutu + self.hucre_boyutu // 4
        x2 = x1 + self.hucre_boyutu // 2
        y2 = y1 + self.hucre_boyutu // 2
        self.canvas.create_oval(x1, y1, x2, y2, fill='cyan', tags='oyuncu')

    def fare_basildi(self, olay):
        # Fare basıldığında topun üzerinde olup olmadığını kontrol et
        items_at_click = self.canvas.find_overlapping(olay.x, olay.y, olay.x, olay.y)
        for item_id in items_at_click:
            tags = self.canvas.gettags(item_id)
            if 'oyuncu' in tags:
                self.is_surukleme = True
                self.oyuncu_konumu_baslangici = self.oyuncu_konumu
                self.canvas.delete('yol') # Yeni bir sürükleme başladığında eski yolu temizle
                self.oyuncu_yolu = [self.oyuncu_konumu]
                return

    def surukle(self, olay):
        if not self.is_surukleme:
            return

        yeni_sutun = olay.x // self.hucre_boyutu
        yeni_satir = olay.y // self.hucre_boyutu
        hedef_konum = (yeni_satir, yeni_sutun)

        if hedef_konum == self.oyuncu_konumu:
            return
        
        # Sadece komşu hücreye geçişe izin ver
        r_fark = abs(hedef_konum[0] - self.oyuncu_konumu[0])
        c_fark = abs(hedef_konum[1] - self.oyuncu_konumu[1])

        if (r_fark == 1 and c_fark == 0) or (r_fark == 0 and c_fark == 1):
            if not self.duvar_var_mi(self.oyuncu_konumu, hedef_konum):
                self.oyuncu_konumu = hedef_konum
                self.oyuncu_yolu.append(self.oyuncu_konumu)
                self.oyuncu_yolunu_ciz()
                self.oyuncuyu_ciz()
                self.kazanmayi_kontrol_et()

    def fare_birakildi(self, olay):
        self.is_surukleme = False

    def duvar_var_mi(self, hucre1, hucre2):
        r1, c1 = hucre1
        r2, c2 = hucre2
        
        if r1 > r2:
            return self.izgara[r1][c1]['duvarlar']['ust']
        elif r1 < r2:
            return self.izgara[r1][c1]['duvarlar']['alt']
        elif c1 > c2:
            return self.izgara[r1][c1]['duvarlar']['sol']
        elif c1 < c2:
            return self.izgara[r1][c1]['duvarlar']['sag']
        return False

    def oyuncu_yolunu_ciz(self):
        self.canvas.delete('yol')
        if len(self.oyuncu_yolu) > 1:
            noktalar = []
            for r, c in self.oyuncu_yolu:
                x = c * self.hucre_boyutu + self.hucre_boyutu // 2
                y = r * self.hucre_boyutu + self.hucre_boyutu // 2
                noktalar.append(x)
                noktalar.append(y)
            self.canvas.create_line(noktalar, fill='cyan', width=2, tags='yol')

    def kazanmayi_kontrol_et(self):
        if self.oyuncu_konumu == self.bitis_konumu:
            self.canvas.create_text(self.sutun_sayisi * self.hucre_boyutu / 2, self.satir_sayisi * self.hucre_boyutu / 2, text='KAZANDIN!', fill='white', font=('Georgia', 50, 'bold'))
            self.yeniden_baslat_butonunu_goster()

    def yeniden_baslat_butonunu_goster(self):
        if self.yeniden_baslat_butonu:
            self.yeniden_baslat_butonu.destroy()
        
        kazanma_yazisi_y = self.satir_sayisi * self.hucre_boyutu / 2
        buton_y = kazanma_yazisi_y + self.hucre_boyutu * 2

        self.yeniden_baslat_butonu = tk.Button(self.ana_pencere, text="TEKRAR OYNA", command=self.oyunu_sifirla, font=('Georgia', 12, 'bold'))
        self.canvas.create_window(self.sutun_sayisi * self.hucre_boyutu / 2, buton_y, window=self.yeniden_baslat_butonu)

    def oyunu_sifirla(self):
        if self.yeniden_baslat_butonu:
            self.yeniden_baslat_butonu.destroy()
            self.yeniden_baslat_butonu = None
        
        self.oyuncu_konumu = self.baslangic_konumu
        self.oyuncu_yolu = [self.baslangic_konumu]
        self.labirenti_olustur()
        self.labirenti_ciz()
        self.oyuncuyu_ciz()

def main():
    kok_pencere = tk.Tk()
    kok_pencere.title("Labirent Oyunu")
    LabirentOyunu(kok_pencere, satir_sayisi=15, sutun_sayisi=15, hucre_boyutu=30)
    kok_pencere.mainloop()

if __name__ == "__main__":
    main()
