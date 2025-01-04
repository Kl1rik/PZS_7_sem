import json
import hashlib
from cryptography.fernet import Fernet



def generate_key():
    return Fernet.generate_key()

def encrypt_data(key, data):
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data.encode())
    return encrypted

def decrypt_data(key, encrypted_data):
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_data).decode()
    return decrypted

def hash_data(data):
    return hashlib.sha256(data.encode()).hexdigest()

class DataManager:
    def __init__(self):
        self.data_store = {}
        self.key = generate_key()  # Генерация ключа

    def add_data(self, identifier, data, confidential=False):
        st
        if confidential:
            encrypted_data = encrypt_data(self.key, data)
            self.data_store[identifier] = {'type': 'confidential', 'data': encrypted_data}
        else:
            self.data_store[identifier] = {'type': 'non-confidential', 'data': data}

    def update_data(self, identifier, data):
        if identifier in self.data_store:
            self.data_store[identifier]['data'] = data

    def delete_data(self, identifier):
        if identifier in self.data_store:
            del self.data_store[identifier]

    def display_data(self):
        for identifier, info in self.data_store.items():
            if info['type'] == 'confidential':
                decrypted_data = decrypt_data(self.key, info['data'])
                print(f"{identifier}: {decrypted_data} (Конфиденциальные данные)")
            else:
                print(f"{identifier}: {info['data']} (Неконфиденциальные данные)")

def main():
    manager = DataManager()
    
    while True:
        print("\nВыберите действие:")
        print(Fore.LIGHTBLUE_EX  + "1 -- Добавить данные")
        print(Fore.WHITE  + "2 -- Обновить данные")
        print("3 -- Удалить данные")
        print("4 -- Показать данные")
        print("5 -- Выход")

        action = input("Введите номер действия: ").strip()

        if action == '1':
            identifier = input(Fore.WHITE  + "Введите идентификатор: ")
            data = input("Введите данные: ")
            confidential = input(Fore.GREEN + "Данные конфиденциальные? (yes/no): ").strip().lower() == 'yes'
            manager.add_data(identifier, data, confidential)
        elif action == '2':
            identifier = input(Fore.WHITE  + "Введите идентификатор для обновления: ")
            data = input("Введите новые данные: ")
            manager.update_data(identifier, data)
        elif action == '3':
            identifier = input(Fore.WHITE  + "Введите идентификатор для удаления: ")
            manager.delete_data(identifier)
        elif action == '4':
            manager.display_data()
        elif action == '5':
            break
        else:
            print("Неверный номер действия. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()
