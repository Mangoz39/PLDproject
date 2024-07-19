import sys
import classdef


user_list = {}
current_user: classdef.User
current_user_name = ""


def login():
    global current_user_name
    if user_list:
        print("--------------------")
        print("User List:")
        for idx, u in enumerate(user_list):
            print(f"{idx+1}. {u}")
        user = input("\nLogin As: ")
        if user in user_list:
            current_user_name = user
            return user_list[user]
    else:
        print("User not found!")
        welcome()


def register():
    global current_user_name
    print("--------------------")
    print("Register a new Account:")
    name = input("Enter Your Name: ")
    user_list.update({f"{name}": classdef.User()})
    current_user_name = name
    return user_list[name]


def welcome():
    global current_user
    print("--------------------")
    print("1. Login\n2. Register\n3. Quit")
    print("--------------------")
    act = int(input("Action: "))
    match act:
        case 1:
            current_user = login()
            mainloop()
        case 2:
            current_user = register()
            mainloop()
        case 3:
            print("--------------------")
            print("See You Next Time ")
            print("--------------------")
            sys.exit(0)


def mainloop():
    global current_user
    print("--------------------")
    print(f"Hi, {current_user_name}! Choose an action!")
    print("1. Create a sheet\n2. Check a sheet\n3. Change a value in a sheet\n"
          "4. Change a sheet's access right\n5. Collaborate with other users\n"
          "6. List from friends\n7. Log out")
    print("--------------------")
    act = input("Action: ")
    match act:
        case '1':
            current_user.create_sheet()
            mainloop()
        case '2':
            current_user.print_sheet()
            mainloop()
        case '3':
            current_user.change_val()
            mainloop()
        case '4':
            current_user.change_right()
            mainloop()
        case '5':
            current_user.share_user()
            mainloop()
        case '6':
            current_user.can_access_sheet()
            mainloop()
        case '7':
            print(f"Thank you, {current_user_name}!")
            welcome()
    mainloop()
