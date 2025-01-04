import json
import hashlib
from cryptography.fernet import Fernet
import os
import psutil
import pickle
from colorama import Fore,Back,Style
import time

# Генерация ключа для шифрования
def generate_key():
    return Fernet.generate_key()

# Шифрование данных
def encrypt_data(key, data):
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data.encode())
    return encrypted

# Дешифрование данных
def decrypt_data(key, encrypted_data):
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_data).decode()
    return decrypted

# Хэширование данных
def hash_data(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Основной класс приложения
class DataManager:
    def __init__(self):
        start_time = time.time()
        self.data_store = {}
        self.key = generate_key()
        end_time = time.time()
        
        print(f"Затраченное процессорное время {(end_time - start_time):.6f} секунд")  # Генерация ключа для шифрования

    def add_data(self, identifier, data, confidential=False):

        start_time = time.time()

        if confidential:
            encrypted_data = encrypt_data(self.key, data)
            self.data_store[identifier] = {'type': 'confidential', 'data': encrypted_data}
        else:
            self.data_store[identifier] = {'type': 'non-confidential', 'data': data}

        end_time = time.time()
        
        print(f"Затраченное процессорное время {(end_time - start_time):.6f} секунд")  

    def update_data(self, identifier, data):
        if identifier in self.data_store:
            start_time = time.time()
            if self.data_store[identifier]['type'] == 'confidential':
                encrypted_data = encrypt_data(self.key, data)
                self.data_store[identifier]['data'] = encrypted_data
                end_time = time.time()
        
                print(f"Затраченное процессорное время {(end_time - start_time):.6f} секунд")      
            else:
                self.data_store[identifier]['data'] = data
                end_time = time.time()
        
                print(f"Затраченное процессорное время {(end_time - start_time):.6f} секунд")  

    def delete_data(self, identifier):
        if identifier in self.data_store:
            start_time = time.time()
            del self.data_store[identifier]
            end_time = time.time()
        
            print(f"Затраченное процессорное время {(end_time - start_time):.6f} секунд")  


    def display_data(self):
        start_time = time.time()
        for identifier, info in self.data_store.items():
            if info['type'] == 'confidential':
                decrypted_data = decrypt_data(self.key, info['data'])
                print(f"{identifier}: {decrypted_data} (Конфиденциальные данные)")
            else:
                print(f"{identifier}: {info['data']} (Неконфиденциальные данные)")

        end_time = time.time()
        
        print(f"Затраченное процессорное время {(end_time - start_time):.6f} секунд")  

    def dump_memory(self, filename):
        start_time = time.time()
        with open(filename, 'wb') as f:
            pickle.dump(self.data_store, f)
            end_time = time.time()
        
            print(f"Затраченное процессорное время {(end_time - start_time):.6f} секунд")  
    
    def print_memory_usage(self):
        start_time = time.time()
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()
        print(f"Использование памяти: {mem_info.rss / (1024 * 1024):.2f} МБ")  # RSS в МБ
        end_time = time.time()
        print(f"Затраченное процессорное время {(end_time - start_time):.6f} секунд")

def main():
    manager = DataManager()

    while True:
        print(Fore.WHITE + "\nВыберите действие:")
        print("1. Добавить данные")
        print("2. Обновить данные")
        print("3. Удалить данные")
        print("4. Отобразить данные")
        print("5. Вывести использование памяти")
        print("6. Создать дамп оперативной памяти (ввод данных)")
        print("7. Создать дамп оперативной памяти (обновление данных)")
        print("8. Создать дамп оперативной памяти (удаление данных)")
        print("9. Выход")

        action = input(Fore.GREEN + "Введите номер действия: ").strip()


        if action == '1':
            identifier = input(Fore.LIGHTBLUE_EX + "Введите идентификатор: ")
            data = input(Fore.WHITE + "Введите данные: ")
            confidential = input(Fore.LIGHTYELLOW_EX + "Данные конфиденциальные? (yes/no): ").strip().lower() == 'yes'
            manager.add_data(identifier, data, confidential)
        elif action == '2':
            identifier = input(Fore.LIGHTBLUE_EX + "Введите идентификатор для обновления: ")
            data = input(Fore.WHITE + "Введите новые данные: ")
            manager.update_data(identifier, data)
        elif action == '3':
            identifier = input(Fore.LIGHTBLUE_EX + "Введите идентификатор для удаления: ")
            manager.delete_data(identifier)
        elif action == '4':
            manager.display_data()
        elif action == '5':
            manager.print_memory_usage()
        elif action == '6':
            filename = "memory_dump_after_add.pkl"
            manager.dump_memory(filename)
            print(Fore.LIGHTMAGENTA_EX + f"Создан дамп оперативной памяти после добавления данных в файле: {filename}")
        elif action == '7':
            filename = "memory_dump_after_update.pkl"
            manager.dump_memory(filename)
            print(Fore.LIGHTMAGENTA_EX  + f"Создан дамп оперативной памяти после обновления данных в файле: {filename}")
        elif action == '8':
            filename = "memory_dump_after_delete.pkl"
            manager.dump_memory(filename)
            print(Fore.LIGHTMAGENTA_EX  + f"Создан дамп оперативной памяти после удаления данных в файле: {filename}")
        elif action == '9':
            break
        else:
            print("Неверное действие. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()