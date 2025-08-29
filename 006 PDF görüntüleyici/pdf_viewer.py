import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import fitz  # PyMuPDF
from PIL import Image, ImageTk
import os
import io

class PDFViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Görüntüleyici")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # PDF document variables
        self.pdf_document = None
        self.current_page = 0
        self.total_pages = 0
        self.zoom_factor = 1.0
        self.rotation = 0
        self.auto_fit = True  # Otomatik sığdırma modu
        
        # Create GUI
        self.create_menu()
        self.create_toolbar()
        self.create_main_area()
        self.create_status_bar()
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.open_pdf())
        self.root.bind('<Left>', lambda e: self.previous_page())
        self.root.bind('<Right>', lambda e: self.next_page())
        self.root.bind('<Control-plus>', lambda e: self.zoom_in())
        self.root.bind('<Control-minus>', lambda e: self.zoom_out())
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())
        self.root.bind('<Configure>', self.on_window_resize)  # Pencere boyutu değişikliği
        
    def create_menu(self):
        """Ana menü çubuğunu oluştur"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Dosya menüsü
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Dosya", menu=file_menu)
        file_menu.add_command(label="PDF Aç...", command=self.open_pdf, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Çıkış", command=self.root.quit)
        
        # Görünüm menüsü
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Görünüm", menu=view_menu)
        view_menu.add_command(label="Yakınlaştır", command=self.zoom_in, accelerator="Ctrl++")
        view_menu.add_command(label="Uzaklaştır", command=self.zoom_out, accelerator="Ctrl+-")
        view_menu.add_command(label="Gerçek Boyut", command=self.reset_zoom)
        view_menu.add_separator()
        view_menu.add_command(label="Sayfaya Sığdır", command=self.fit_to_page)
        view_menu.add_command(label="Genişliğe Sığdır", command=self.fit_to_width)
        view_menu.add_separator()
        view_menu.add_command(label="Saat Yönünde Döndür", command=self.rotate_clockwise)
        view_menu.add_command(label="Saat Yönü Tersine Döndür", command=self.rotate_counterclockwise)
        view_menu.add_separator()
        view_menu.add_command(label="Tam Ekran", command=self.toggle_fullscreen, accelerator="F11")
        
        # Yardım menüsü
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Yardım", menu=help_menu)
        help_menu.add_command(label="Klavye Kısayolları", command=self.show_shortcuts)
        help_menu.add_command(label="Hakkında", command=self.show_about)
    
    def create_toolbar(self):
        """Araç çubuğunu oluştur"""
        toolbar_frame = tk.Frame(self.root, bg='#e0e0e0', relief=tk.RAISED, bd=1)
        toolbar_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Dosya işlemleri
        tk.Button(toolbar_frame, text="📁 Aç", command=self.open_pdf, 
                 relief=tk.FLAT, bg='#e0e0e0').pack(side=tk.LEFT, padx=2, pady=2)
        
        tk.Frame(toolbar_frame, width=2, bg='gray').pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Sayfa navigasyonu
        tk.Button(toolbar_frame, text="⬅️ Önceki", command=self.previous_page,
                 relief=tk.FLAT, bg='#e0e0e0').pack(side=tk.LEFT, padx=2, pady=2)
        
        tk.Button(toolbar_frame, text="➡️ Sonraki", command=self.next_page,
                 relief=tk.FLAT, bg='#e0e0e0').pack(side=tk.LEFT, padx=2, pady=2)
        
        # Sayfa numarası girişi
        tk.Label(toolbar_frame, text="Sayfa:", bg='#e0e0e0').pack(side=tk.LEFT, padx=(10,2))
        self.page_entry = tk.Entry(toolbar_frame, width=5)
        self.page_entry.pack(side=tk.LEFT, padx=2)
        self.page_entry.bind('<Return>', self.go_to_page)
        
        tk.Frame(toolbar_frame, width=2, bg='gray').pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Zoom kontrolü
        tk.Button(toolbar_frame, text="🔍+ Yakınlaştır", command=self.zoom_in,
                 relief=tk.FLAT, bg='#e0e0e0').pack(side=tk.LEFT, padx=2, pady=2)
        
        tk.Button(toolbar_frame, text="🔍- Uzaklaştır", command=self.zoom_out,
                 relief=tk.FLAT, bg='#e0e0e0').pack(side=tk.LEFT, padx=2, pady=2)
        
        tk.Button(toolbar_frame, text="📏 Sığdır", command=self.fit_to_page,
                 relief=tk.FLAT, bg='#e0e0e0').pack(side=tk.LEFT, padx=2, pady=2)
        
        # Zoom seviyesi göstergesi
        self.zoom_label = tk.Label(toolbar_frame, text="100%", bg='#e0e0e0')
        self.zoom_label.pack(side=tk.LEFT, padx=5)
        
        tk.Frame(toolbar_frame, width=2, bg='gray').pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Döndürme
        tk.Button(toolbar_frame, text="↻ Döndür", command=self.rotate_clockwise,
                 relief=tk.FLAT, bg='#e0e0e0').pack(side=tk.LEFT, padx=2, pady=2)
    
    def create_main_area(self):
        """Ana görüntüleme alanını oluştur"""
        # Ana çerçeve
        main_frame = tk.Frame(self.root)
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Canvas ile scrollbar - gri arka plan PDF okuma deneyimi için
        self.canvas = tk.Canvas(main_frame, bg='#f5f5f5')
        
        # Scrollbarlar
        v_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Layout
        self.canvas.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Mouse events for canvas
        self.canvas.bind('<Button-1>', self.canvas_click)
        self.canvas.bind('<MouseWheel>', self.mouse_wheel)
        
        # Hoş geldin mesajı
        self.show_welcome_message()
    
    def create_status_bar(self):
        """Durum çubuğunu oluştur"""
        self.status_frame = tk.Frame(self.root, relief=tk.SUNKEN, bd=1)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = tk.Label(self.status_frame, text="PDF dosyası açmak için Dosya > PDF Aç menüsünü kullanın", 
                                   anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        self.page_info_label = tk.Label(self.status_frame, text="", anchor=tk.E)
        self.page_info_label.pack(side=tk.RIGHT, padx=5, pady=2)
    
    def show_welcome_message(self):
        """Hoş geldin mesajını göster"""
        welcome_text = """
        🔍 PDF Görüntüleyici
        
        PDF dosyalarını görüntülemek için:
        • Dosya > PDF Aç menüsünü kullanın
        • Veya Ctrl+O tuşlarına basın
        
        Klavye Kısayolları:
        • ← → : Sayfa değiştir
        • Ctrl + + : Yakınlaştır  
        • Ctrl + - : Uzaklaştır
        • F11 : Tam ekran
        
        Başlamak için bir PDF dosyası açın!
        """
        
        self.canvas.create_text(500, 300, text=welcome_text, font=("Arial", 12), 
                               fill="gray", justify=tk.CENTER)
    
    def open_pdf(self):
        """PDF dosyası aç"""
        file_path = filedialog.askopenfilename(
            title="PDF Dosyası Seç",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                # Önceki dökümanı kapat
                if self.pdf_document:
                    self.pdf_document.close()
                
                # Yeni dökümanı aç
                self.pdf_document = fitz.open(file_path)
                self.total_pages = len(self.pdf_document)
                self.current_page = 0
                self.zoom_factor = 1.0
                self.rotation = 0
                
                # İlk sayfayı göster ve otomatik sığdır
                self.fit_to_page()
                
                # UI güncelle
                self.update_ui()
                
                # Durum çubuğunu güncelle
                filename = os.path.basename(file_path)
                self.status_label.config(text=f"Açılan dosya: {filename}")
                
            except Exception as e:
                messagebox.showerror("Hata", f"PDF dosyası açılamadı:\n{str(e)}")
    
    def display_page(self):
        """Mevcut sayfayı görüntüle"""
        if not self.pdf_document:
            return
        
        try:
            # Sayfayı al
            page = self.pdf_document[self.current_page]
            
            # Dönüş matrisini oluştur
            mat = fitz.Matrix(self.zoom_factor, self.zoom_factor)
            if self.rotation != 0:
                mat = mat * fitz.Matrix(self.rotation)
            
            # Sayfayı pixmap'e çevir
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("ppm")
            
            # PIL Image'a çevir
            img = Image.open(io.BytesIO(img_data))
            
            # Tkinter PhotoImage'a çevir
            self.photo = ImageTk.PhotoImage(img)
            
            # Canvas'ı temizle
            self.canvas.delete("all")
            
            # Canvas boyutlarını al
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            # Görüntü boyutlarını al
            img_width = img.width
            img_height = img.height
            
            # Ortalama pozisyonunu hesapla
            x_center = max(0, (canvas_width - img_width) // 2)
            y_center = max(0, (canvas_height - img_height) // 2)
            
            # Görüntüyü canvas'a ortalanmış olarak ekle
            self.canvas.create_image(x_center, y_center, anchor=tk.NW, image=self.photo)
            
            # Canvas scroll bölgesini güncelle - ortalama için genişletilmiş alan
            scroll_width = max(canvas_width, img_width)
            scroll_height = max(canvas_height, img_height)
            self.canvas.configure(scrollregion=(0, 0, scroll_width, scroll_height))
            
        except Exception as e:
            messagebox.showerror("Hata", f"Sayfa görüntülenemedi:\n{str(e)}")
    
    def next_page(self):
        """Sonraki sayfa"""
        if self.pdf_document and self.current_page < self.total_pages - 1:
            self.current_page += 1
            if self.auto_fit:
                self.fit_to_page()
            else:
                self.display_page()
            self.update_ui()
    
    def previous_page(self):
        """Önceki sayfa"""
        if self.pdf_document and self.current_page > 0:
            self.current_page -= 1
            if self.auto_fit:
                self.fit_to_page()
            else:
                self.display_page()
            self.update_ui()
    
    def go_to_page(self, event=None):
        """Belirtilen sayfaya git"""
        if not self.pdf_document:
            return
        
        try:
            page_num = int(self.page_entry.get()) - 1  # 0-indexed
            if 0 <= page_num < self.total_pages:
                self.current_page = page_num
                if self.auto_fit:
                    self.fit_to_page()
                else:
                    self.display_page()
                self.update_ui()
            else:
                messagebox.showwarning("Uyarı", f"Sayfa numarası 1-{self.total_pages} arasında olmalıdır.")
        except ValueError:
            messagebox.showwarning("Uyarı", "Geçerli bir sayfa numarası girin.")
    
    def zoom_in(self):
        """Yakınlaştır"""
        if self.pdf_document:
            self.zoom_factor *= 1.2
            self.auto_fit = False  # Manuel zoom yapıldığında auto_fit'i kapat
            self.display_page()
            self.update_ui()
    
    def zoom_out(self):
        """Uzaklaştır"""
        if self.pdf_document:
            self.zoom_factor /= 1.2
            self.auto_fit = False  # Manuel zoom yapıldığında auto_fit'i kapat
            self.display_page()
            self.update_ui()
    
    def reset_zoom(self):
        """Zoom'u sıfırla"""
        if self.pdf_document:
            self.zoom_factor = 1.0
            self.auto_fit = False
            self.display_page()
            self.update_ui()
    
    def fit_to_page(self):
        """Sayfayı pencere boyutuna sığdır"""
        if not self.pdf_document:
            return
        
        try:
            # Mevcut sayfayı al
            page = self.pdf_document[self.current_page]
            page_rect = page.rect
            
            # Canvas boyutlarını al
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            # Eğer canvas henüz render edilmemişse varsayılan değerleri kullan
            if canvas_width <= 1:
                canvas_width = 800
            if canvas_height <= 1:
                canvas_height = 600
            
            # Sayfa boyutlarını al (döndürme dahil)
            if self.rotation % 180 == 90:
                page_width = page_rect.height
                page_height = page_rect.width
            else:
                page_width = page_rect.width
                page_height = page_rect.height
            
            # Zoom faktörünü hesapla (padding için %90 - daha fazla margin)
            zoom_x = (canvas_width * 0.90) / page_width
            zoom_y = (canvas_height * 0.90) / page_height
            
            # En küçük zoom faktörünü seç (tam sığması için)
            self.zoom_factor = min(zoom_x, zoom_y)
            self.auto_fit = True
            
            self.display_page()
            self.update_ui()
            
        except Exception as e:
            print(f"Fit to page error: {e}")
    
    def fit_to_width(self):
        """Sayfayı genişliğe sığdır"""
        if not self.pdf_document:
            return
        
        try:
            # Mevcut sayfayı al
            page = self.pdf_document[self.current_page]
            page_rect = page.rect
            
            # Canvas genişliğini al
            canvas_width = self.canvas.winfo_width()
            
            # Eğer canvas henüz render edilmemişse varsayılan değeri kullan
            if canvas_width <= 1:
                canvas_width = 800
            
            # Sayfa genişliğini al (döndürme dahil)
            if self.rotation % 180 == 90:
                page_width = page_rect.height
            else:
                page_width = page_rect.width
            
            # Zoom faktörünü hesapla (padding için %95)
            self.zoom_factor = (canvas_width * 0.95) / page_width
            self.auto_fit = False
            
            self.display_page()
            self.update_ui()
            
        except Exception as e:
            print(f"Fit to width error: {e}")
    
    def on_window_resize(self, event):
        """Pencere boyutu değiştiğinde otomatik sığdır"""
        # Sadece ana pencere resize olaylarını dinle
        if event.widget == self.root and self.auto_fit and self.pdf_document:
            # Kısa bir gecikme ile fit_to_page çağır (resize olayı çok sık tetiklenir)
            self.root.after(100, self.fit_to_page)
    
    def rotate_clockwise(self):
        """Saat yönünde döndür"""
        if self.pdf_document:
            self.rotation += 90
            if self.rotation >= 360:
                self.rotation = 0
            self.display_page()
    
    def rotate_counterclockwise(self):
        """Saat yönü tersine döndür"""
        if self.pdf_document:
            self.rotation -= 90
            if self.rotation < 0:
                self.rotation = 270
            self.display_page()
    
    def toggle_fullscreen(self):
        """Tam ekran açıp kapat"""
        current_state = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current_state)
    
    def canvas_click(self, event):
        """Canvas tıklama olayı"""
        self.canvas.focus_set()
    
    def mouse_wheel(self, event):
        """Mouse tekerleği ile scroll"""
        if event.state & 0x4:  # Ctrl tuşu basılı
            # Ctrl + Mouse wheel = Zoom
            if event.delta > 0:
                self.zoom_in()
            else:
                self.zoom_out()
        else:
            # Normal scroll - sadece içerik canvas'tan büyükse scroll yap
            if self.pdf_document:
                # Canvas ve görüntü boyutlarını kontrol et
                canvas_height = self.canvas.winfo_height()
                if hasattr(self, 'photo'):
                    img_height = self.photo.height()
                    if img_height > canvas_height:
                        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def update_ui(self):
        """Kullanıcı arayüzünü güncelle"""
        if self.pdf_document:
            # Sayfa bilgisi
            self.page_entry.delete(0, tk.END)
            self.page_entry.insert(0, str(self.current_page + 1))
            
            self.page_info_label.config(text=f"Sayfa {self.current_page + 1} / {self.total_pages}")
            
            # Zoom bilgisi
            zoom_percent = int(self.zoom_factor * 100)
            self.zoom_label.config(text=f"{zoom_percent}%")
    
    def show_shortcuts(self):
        """Klavye kısayollarını göster"""
        shortcuts = """
        Klavye Kısayolları:
        
        Dosya İşlemleri:
        • Ctrl+O : PDF dosyası aç
        
        Sayfa Navigasyonu:
        • ← Sol Ok : Önceki sayfa
        • → Sağ Ok : Sonraki sayfa
        
        Zoom İşlemleri:
        • Ctrl + + : Yakınlaştır
        • Ctrl + - : Uzaklaştır
        • Ctrl + Mouse Wheel : Zoom
        
        Görünüm:
        • F11 : Tam ekran açık/kapat
        
        Mouse İşlemleri:
        • Mouse Wheel : Dikey scroll
        • Ctrl + Mouse Wheel : Zoom
        """
        
        messagebox.showinfo("Klavye Kısayolları", shortcuts)
    
    def show_about(self):
        """Hakkında bilgisi"""
        about_text = """
        PDF Görüntüleyici v1.0
        
        Python Tkinter ile geliştirilmiş
        PDF görüntüleme uygulaması
        
        Özellikler:
        • PDF dosyalarını açma ve görüntüleme
        • Sayfa navigasyonu
        • Zoom in/out
        • Sayfa döndürme
        • Tam ekran modu
        • Klavye kısayolları
        
        Geliştirici: AI Assistant
        """
        
        messagebox.showinfo("Hakkında", about_text)

def main():
    # PyMuPDF kurulu mu kontrol et
    try:
        import fitz
    except ImportError:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Eksik Kütüphane", 
                           "Bu uygulama PyMuPDF kütüphanesine ihtiyaç duyar.\n\n"
                           "Lütfen şu komutu çalıştırın:\n"
                           "pip install PyMuPDF pillow")
        return
    
    root = tk.Tk()
    app = PDFViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
