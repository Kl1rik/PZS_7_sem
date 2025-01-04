from flask import Flask, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from colorama import Fore,Back,Style


app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/kl1rik/PZS_7_sem/lab_2/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

# Модель пользователя
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Модель конфиденциальных и неконфиденциальных данных
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    is_confidential = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Запросы в функции
def add_user(username, password):
    with app.app_context():
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        print(Fore.GREEN + f"Пользователь '{username}' создан.")

def login(username, password):
    with app.app_context():
        user = User.query.filter_by(username=username, password=password).first()
    if user:
        print(Fore.GREEN + f"Пользователь '{username}' вошел в систему.")
    else:
        print("Неправильные данные пользователя.")

def logout():
    with app.app_context():
        logout_user()
        print("Пользователь вышел из системы.")

def add_data(content, is_confidential):
    with app.app_context():
        new_data = Data(content=content, is_confidential=is_confidential)
        db.session.add(new_data)
        db.session.commit()
        print(Fore.GREEN + f"Добавлены данные: {content}")

def edit_data(data_id, content, is_confidential):
    with app.app_context():
        existing_data = Data.query.get(data_id)
        if existing_data:
            existing_data.content = content
            existing_data.is_confidential = is_confidential
            db.session.commit()
            print("Данные обновлены.")
        else:
            print("Данные не найдены.")

def delete_data(data_id):
    with app.app_context():
        existing_data = Data.query.get(data_id)
        if existing_data:
            db.session.delete(existing_data)
            db.session.commit()
            print("Данные удалены.")
        else:
            print("Данные не найдены.")

def search_data(query):
    with app.app_context():
        results = Data.query.filter(Data.content.contains(query)).all()
        if results:
            print("Результаты поиска:")
            for d in results:
                print(f"ID: {d.id}, Content: {d.content}, Confidential: {d.is_confidential}")
        else:
            print("Резулаты поиска не найдены.")

def view_users(username):
    with app.app_context():
        users = User.query.all()
        if users and username == "admin":
            print("Пользователи в БД:")
            for user in users:
                print(f"ID: {user.id}, Username: {user.username}")
        elif users and username != "admin":
            print("Пользователи в БД:")
            for user in users:
                print(f" Username: {user.username}")
        else:
            print("No users found.")

def view_data(username):
    with app.app_context():
        data_entries = Data.query.all()
        if data_entries and username == "admin":
            print("Данные в БД:")
            for d in data_entries:
                print(f"ID: {d.id}, Content: {d.content}, Confidential: {d.is_confidential}")

        if data_entries and username != "admin":
            print("Данные в БД:")
            for d in data_entries:
                if d.is_confidential == False :
                    print(f"ID: {d.id}, Content: {d.content}, Confidential: {d.is_confidential}")        
        else:
            print("Данные не найдены.")

# Создание базы данных
with app.app_context():
    db.create_all()  # Создание всех таблиц в базе данных

if __name__ == '__main__':
    print("ПЗС 2.1")

    username = input("Имя пользователя: ")
    password = input("Пароль: ")
    login(username, password)

    while True:
        print(Fore.LIGHTBLUE_EX + "\nВыберите опцию:")
        print(Fore.WHITE + "1. Добавить пользователя")
        print("2. Добавить данные")
        print("3. Изменить данные ")
        print("4. Удалить данные")
        print("5. Поиск данных")
        print("6. Просмотр пользователей")
        print("7. Просмотр данных")
        print("8. Выход")

        option = input("Enter option (1-8): ")

        if option == "1":
            username = input("Имя пользователя: ")
            password = input("Пароль: ")
            add_user(username, password)
        elif option == "2":
            content = input("Введите данные: ")
            is_confidential = input("Это закрытые данные? (да/нет): ").strip().lower() == 'да'
            add_data(content, is_confidential)
        elif option == "3":
            data_id = int(input("Введите id записи для изменения: "))
            content = input("Введите новые данные: ")
            is_confidential = input("Это закрытые данные? (да/нет): ").strip().lower() == 'да'
            edit_data(data_id, content, is_confidential)
        elif option == "4":
            data_id = int(input("Введите id записи для удаления: "))
            delete_data(data_id)
        elif option == "5":
            query = input("Введите SQL запрос: ")
            search_data(query)
        elif option == "6":
            view_users(username)
        elif option == "7":
            view_data(username)
        elif option == "8":
            print(Fore.BLUE + "Выход...")
            break
        else:
            print("Некорректный ввод.попробуйте еще.")