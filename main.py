import funcs
import datetime
import bcrypt

rol_user = ["admin", "agent"]

user = True

# contraseñas usadas "1234"

server_token = None
user_token = {"expired_date": datetime.datetime.today(), "token": "invite"}

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
        user_token = {"expired_date": datetime.datetime.today(), "token": "invite"}
        server_token = None

        for user in users["data"]:
            if user["name"] == user_name:
                encontrado = True
                if bcrypt.checkpw(user_pwd.encode(), user["pwd"].encode()):
                    print("Log in...")
                    user_token = {"expired_date": datetime.datetime.today(), "token": bcrypt.hashpw(user_pwd.encode(), bcrypt.gensalt())}
                    if user["rol"] == "admin":
                        server_token = user_token["token"] # Asignamos server_token para que tenga acceso a la zona restringida
                else:
                    print("Password incorrecto")
        if encontrado == False:
            print("Usuario no encontrado")

    elif user == "3": # comprobar token
        if user_token:
            if (user_token["expired_date"] + datetime.timedelta(seconds=10)) > datetime.datetime.today():
                #if bcrypt.checkpw(server_token.encode(), user_token["token"]):
                if user_token["token"] == server_token:
                    print("-----------------------")
                    print("ZONA RESTRINGIDA")
                    print("Acceso permitido...")
                    user = input("")