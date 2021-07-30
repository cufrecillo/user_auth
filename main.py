import funcs
import datetime

user = True

while user != False:
    funcs.menu()
    user = input("Choose: ")
    if user.upper() == "Q":
        user = False
    elif user == "1":
        user_name = input("User name: ")
        users = funcs.read_json("users.json")
        users_names = [user["name"] for user in users["data"]]
        try:
            users_names.index(user_name)
            print("El usuario ya existe")
        except ValueError:
            user_pwd = input("Password: ")
            new_user = {"name": user_name, "pwd": user_pwd, "user_since": datetime.date.today().isoformat()}
            users["data"].append(new_user)
            funcs.create_user(users, "users.json")
            print("Usuario creado")