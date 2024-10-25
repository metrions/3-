import tkinter as tk
import re
from tkinter import filedialog, messagebox
import string

# Генерация алфавита с символом '_'
ALPHABET = 'abcdefghijklmnopqrstuvwxyz_'
ALPHABET_SIZE = len(ALPHABET)

# Преобразование символа в индекс
def char_to_index(char):
    return ALPHABET.index(char)

# Преобразование индекса в символ
def index_to_char(index):
    return ALPHABET[index % ALPHABET_SIZE]

# Функция шифрования
def beaufort_encrypt(plaintext, key):
    # Подгоняем длину ключа
    k = (key * (len(plaintext)) + key)[:len(plaintext)] 
    c = ''.join([index_to_char((char_to_index(k[i]) - char_to_index(plaintext[i])) % ALPHABET_SIZE) for i in range(len(plaintext))])

    return c

# Функция дешифрования по алгоритму Бофора (та же, что и для шифрования)
def beaufort_decrypt(ciphertext, key):
    return beaufort_encrypt(ciphertext, key)

# Функция чтения данных из файла
def read_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().strip().lower()

# Функция записи данных в файл
def write_to_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(data)

# Интерфейс tkinter
class BoforApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Шифрование Бофора")
        self.geometry("900x600")

        # Поля для ввода ключа и последовательности
        self.key_label = tk.Label(self, text="Ключ для шифрования")
        self.key_label.place(x=20, y=30)

        self.key_entry = tk.Entry(self, width=50)
        self.key_entry.place(x=20, y=60)

        self.sequence_label = tk.Label(self, text="Последовательность для шифрования")
        self.sequence_label.place(x=20, y=100)

        self.sequence_entry = tk.Entry(self, width=50)
        self.sequence_entry.place(x=20, y=130)

        # Поля для отображения кодов и результатов
        self.code_label = tk.Label(self, text="Зашифрованная последовательность")
        self.code_label.place(x=20, y=180)

        self.code_text = tk.Entry(self, width=50)
        self.code_text.place(x=20, y=210)

        self.decode_label = tk.Label(self, text="Расшифрованная последовательность")
        self.decode_label.place(x=20, y=260)

        self.decode_text = tk.Entry(self, width=50)
        self.decode_text.place(x=20, y=290)

        # Кнопки для действий
        y_shift = 60
        y_step = 40
        self.encode_button = tk.Button(self, text="Загрузить Ключ для шифрования", command=self.load_key)
        self.encode_button.place(x=520, y=y_shift)

        self.key_button = tk.Button(self, text="Загрузить последовательность", command=self.load_sequence)
        self.key_button.place(x=520, y=y_shift+y_step)

        self.encrypt_button = tk.Button(self, text="Зашифровать", command=self.encrypt_sequence)
        self.encrypt_button.place(x=520, y=y_shift+y_step*2)

        self.save_encoded_button = tk.Button(self, text="Сохранить в файл зашифрованную последовательность", command=self.save_encoded)
        self.save_encoded_button.place(x=520, y=y_shift+y_step*3)

        self.load_encoded_button = tk.Button(self, text="Загрузить зашифрованную последовательность", command=self.load_encoded)
        self.load_encoded_button.place(x=520, y=y_shift+y_step*4)

        self.decrypt_button = tk.Button(self, text="Расшифровать", command=self.decrypt_sequence)
        self.decrypt_button.place(x=520, y=y_shift+y_step*5)

        self.save_decoded_button = tk.Button(self, text="Сохранить в файл расшифрованную последовательность", command=self.save_decoded)
        self.save_decoded_button.place(x=520, y=y_shift+y_step*6)

    # Функция для шифрования введенной последовательности
    def encrypt_sequence(self):
        sequence = self.sequence_entry.get().strip()
        key = self.key_entry.get().strip()
        if not sequence or not key:
            messagebox.showerror("Error", "Введите последовательность и ключ")
            return

        encrypted_sequence = beaufort_encrypt(sequence, key)
        self.code_text.delete(0, tk.END)
        self.code_text.insert(0, encrypted_sequence)

    # Функция для расшифровки введенной последовательности
    def decrypt_sequence(self):
        encrypted_sequence = self.code_text.get().strip()
        key = self.key_entry.get().strip()
        if not encrypted_sequence or not key:
            messagebox.showerror("Error", "Введите зашифрованную последовательность и ключ")
            return

        decrypted_sequence = beaufort_decrypt(encrypted_sequence, key)
        self.decode_text.delete(0, tk.END)
        self.decode_text.insert(0, decrypted_sequence)

    # Сохранить зашифрованную последовательность
    def save_encoded(self):
        encrypted_sequence = self.code_text.get().strip()
        if not encrypted_sequence:
            messagebox.showerror("Error", "Нет последовательности для сохранения")
            return

        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not filepath:
            return

        write_to_file(filepath, encrypted_sequence)
        messagebox.showinfo("Success", "Закодированная последовательность сохранена успешно")

    # Сохранить расшифрованную последовательность
    def save_decoded(self):
        decoded_sequence = self.decode_text.get().strip()
        if not decoded_sequence:
            messagebox.showerror("Error", "Нет последовательности для сохранения")
            return

        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not filepath:
            return

        write_to_file(filepath, decoded_sequence)
        messagebox.showinfo("Success", "Расшифрованная последовательность сохранена успешно")

    # Загрузить зашифрованную последовательность из файла
    def load_encoded(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not filepath:
            return

        encoded_sequence = read_from_file(filepath)
        self.code_text.delete(0, tk.END)
        self.code_text.insert(0, encoded_sequence)

    # Загрузить Последовательность
    def load_sequence(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not filepath:
            return

        with open(filepath, 'r') as file:
            encoded_sequence = file.read().strip()

            # Проверка, что последовательность содержит только символы a-z и _
            if not re.fullmatch(r'[a-z_]+', encoded_sequence):
                messagebox.showerror("Error", "Последовательность должна содержать только символы a-z и _")
                return
            
            self.sequence_entry.delete(0, tk.END)
            self.sequence_entry.insert(0, encoded_sequence)
    
    # Загрузить Ключ
    def load_key(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not filepath:
            return

        with open(filepath, 'r') as file:
            key_entry = file.read().strip()
            # Проверка, что ключ содержит только символы a-z и _
            if not re.fullmatch(r'[a-z_]+', key_entry):
                messagebox.showerror("Error", "Ключ должен содержать только символы a-z и _")
                return
            self.key_entry.delete(0, tk.END)
            self.key_entry.insert(0, key_entry)


if __name__ == "__main__":
    app = BoforApp()
    app.mainloop()
