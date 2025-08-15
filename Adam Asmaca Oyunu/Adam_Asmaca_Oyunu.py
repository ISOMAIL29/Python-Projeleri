import tkinter as tk
import random

# Kelime listesi
kelimeler = ("elma", "armut", "muz", "çilek", "kiraz", "üzüm", "erik", "kayısı", "şeftali", "portakal", "mandalina", "nar", "kavun", "karpuz", "incir", "hurma", "ayva", "limon", "vişne", "dut", "ananas", "avokado", "greyfurt", "kivi", "böğürtlen", "ahududu", "yabanmersini", "kızılcık", "hurma")

# Adam asmacanın çizimleri
hangman_drawings = {
    0: (" ", " ", " "),
    1: ("  o  ", "   ", "   "),
    2: ("  o  ", "  |  ", "   "),
    3: ("  o  ", " /|  ", "   "),
    4: ("  o  ", " /|\\ ", "   "),
    5: ("  o  ", " /|\\ ", " /   "),
    6: ("  o  ", " /|\\ ", " / \\ ")
}

# Global değişkenler
wrong_guesses_count = 0
guessed_letters = set()
target_word = ""
display_word = []

# Arayüz elemanları
drawing_label = None
word_label = None
message_label = None
guess_entry = None
guess_button = None
new_game_button = None

def update_drawing():
    global drawing_label
    drawing = "\n".join(hangman_drawings[wrong_guesses_count])
    drawing_label.config(text=drawing)

def update_word_display():
    global word_label
    word_label.config(text=" ".join(display_word))

def check_game_state():
    global message_label, guess_entry, guess_button, new_game_button
    
    if "_" not in display_word:
        message_label.config(text="TEBRİKLER! KAZANDINIZ!", fg="#2ecc71")
        guess_entry.config(state="disabled")
        guess_button.config(state="disabled")
        new_game_button.pack()
    elif wrong_guesses_count >= len(hangman_drawings) - 1:
        message_label.config(text=f"KAYBETTİNİZ! Doğru cevap '{target_word}' idi.", fg="#e74c3c")
        guess_entry.config(state="disabled")
        guess_button.config(state="disabled")
        new_game_button.pack()

def make_guess(event=None):
    global wrong_guesses_count, guessed_letters, display_word, target_word
    
    guess = guess_entry.get().lower()
    guess_entry.delete(0, tk.END)

    if len(guess) != 1 or not guess.isalpha():
        message_label.config(text="Geçersiz giriş! Lütfen tek bir harf girin.")
        return
    
    if guess in guessed_letters:
        message_label.config(text=f"'{guess}' harfini zaten tahmin ettiniz.")
        return

    guessed_letters.add(guess)

    if guess in target_word:
        message_label.config(text="Doğru tahmin!")
        for i in range(len(target_word)):
            if target_word[i] == guess:
                display_word[i] = guess
    else:
        message_label.config(text="Yanlış tahmin!")
        wrong_guesses_count += 1
    
    update_word_display()
    update_drawing()
    check_game_state()

def start_new_game():
    global wrong_guesses_count, guessed_letters, target_word, display_word
    
    wrong_guesses_count = 0
    guessed_letters = set()
    target_word = random.choice(kelimeler)
    display_word = ["_"] * len(target_word)
    
    update_drawing()
    update_word_display()
    message_label.config(text="Oyun Başladı!", fg="#ecf0f1")
    
    guess_entry.config(state="normal")
    guess_button.config(state="normal")
    new_game_button.pack_forget()
    guess_entry.focus_set()

if __name__ == "__main__":
    pencere = tk.Tk()
    pencere.title("Adam Asmaca")
    pencere.geometry("500x500")
    pencere.resizable(False, False)
    pencere.configure(bg="#2c3e50")

    main_frame = tk.Frame(pencere, bg="#2c3e50")
    main_frame.pack(expand=True, padx=20, pady=20)
    
    drawing_label = tk.Label(main_frame, text="", font=("Courier", 20), bg="#2c3e50", fg="#ecf0f1")
    drawing_label.pack(pady=(0, 20))
    
    word_label = tk.Label(main_frame, text="", font=("Arial", 24, "bold"), bg="#2c3e50", fg="#ecf0f1")
    word_label.pack(pady=10)
    
    message_label = tk.Label(main_frame, text="", font=("Arial", 14), bg="#2c3e50", fg="#ecf0f1")
    message_label.pack(pady=10)
    
    input_frame = tk.Frame(main_frame, bg="#2c3e50")
    input_frame.pack(pady=10)
    
    letter_label = tk.Label(input_frame, text="Bir harf gir:", font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1")
    letter_label.pack(side=tk.LEFT)
    
    guess_entry = tk.Entry(input_frame, width=5, font=("Arial", 12))
    guess_entry.pack(side=tk.LEFT, padx=5)
    guess_entry.bind("<Return>", make_guess)
    
    guess_button = tk.Button(input_frame, text="Tahmin Et", font=("Arial", 12), command=make_guess)
    guess_button.pack(side=tk.LEFT)
    
    new_game_button = tk.Button(main_frame, text="Yeni Oyun", font=("Arial", 12), command=start_new_game)
    new_game_button.pack(pady=20)
    new_game_button.pack_forget()

    start_new_game()
    pencere.mainloop()
