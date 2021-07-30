import funcs
import datetime
import bcrypt

rol_user = ["admin", "agent"]

user = True

server_token = "12345"
user_token = None

while user != False:
    funcs.menu()
    user = input("Opcion: ")

    if user.upper() == "Q": # Exit
        user = False

    elif user == "1":   #Create user
        print("-----------------------")
        print("MENU CREAR USUARIO")
        user_name = input("User name: ")
        users = funcs.read_json("users.json")
        users_names = [user["name"] for user in users["data"]]
        try:
            users_names.index(user_name)
            print("El usuario ya existe")
        except ValueError:
            user_pwd = input("Password: ")
            funcs.rol_options(rol_user)
            option = int(input("Opcion: ")) -1
            user_rol = rol_user[option]
            users = funcs.read_json("users.json")
            new_user = {"name": user_name, "pwd": bcrypt.hashpw(user_pwd.encode(), bcrypt.gensalt()).decode(), "rol": user_rol, "user_since": datetime.date.today().isoformat()}
            users["data"].append(new_user)
            funcs.create_user(users, "users.json")
            print("Usuario creado")

    elif user == "2":   # Log in
        print("-----------------------")
        print("MENU LOG IN")
        user_name = input("Name: ")
        user_pwd = input("Password: ")
        users = funcs.read_json("users.json")

        encontrado = False
        user_token = None
        for user in users["data"]:
            if user["name"] == user_name:
                encontrado = True
                if bcrypt.checkpw(user_pwd.encode(), user["pwd"].encode()):
                    if user["rol"] == "admin":
                        user_token = server_token
                    print("Log in...")
                else:
                    print("Password incorrecto")
        if encontrado == False:
            print("Usuario no encontrado")

    elif user == "3": # comprobar token
        if server_token == user_token:
            print("-----------------------")
            print("ZONA RESTRINGIDA")
            print("Acceso permitido...")
            user = input("")