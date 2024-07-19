import event


class Sheet:

    def __init__(self, name, myself):
        self.name = name
        self.master = myself
        self.sheet = [[0 for _ in range(3)] for _ in range(3)]
        self.right = 1  # 1 for RW(default), 0 for R only
        self.access = [f"{myself}"]

    def print_sheet(self):
        if event.current_user_name in self.access:
            for row in self.sheet:
                for element in row:
                    print(f"{element}, ", end="")
                print("\n", end="")
        else:
            print("You have no right to access this sheet")

    def change_value(self):
        if event.current_user_name in self.access:
            if self.right:
                x = int(input("Enter an x-axis location to change (0 to 2): "))
                y = int(input("Enter a y-axis location to change (0 to 2): "))
                val = input("Enter a value to change: ")
                if x < 3 and y < 3:
                    self.sheet[x][y] = eval(val)
                    print("Value changed!")
                else:
                    print("Invalid Position")

            else:
                print("The sheet is read-only!")
        else:
            print("You have no right to edit this sheet")

    def set_right(self, right: int):
        if event.current_user_name == self.master:
            match right:
                case 0:  # Read-only
                    self.right = 0
                case 1:  # Editable(default)
                    self.right = 1
        else:
            print("You have no right to edit this sheet")

    def share_user(self, user: str):
        if user in self.access:
            self.access.remove(user)
            event.user_list[user].can_access.remove(self)
            return
        else:
            self.access.append(user)
            event.user_list[user].can_access.append(self)


class User:
    def __init__(self):
        self.sheet_list = {}
        self.can_access = []

    def create_sheet(self):
        name = input("Enter a sheet name: ")
        if name in self.sheet_list:
            print("Sheet already exists!")
            return
        self.sheet_list[name] = Sheet(name, event.current_user_name)
        print(f"A new sheet {name} created!")

    def list_sheet(self):
        print("--------------------")
        print("Current Sheet:")
        for i, s in enumerate(self.sheet_list):
            print(f"{i + 1}. {self.sheet_list[s].name}")
        print("--------------------")

    def print_sheet(self):
        if not self.sheet_list:
            print("You have no sheet currently!")
            return
        self.list_sheet()
        sheet = input("Select a sheet: ")
        if sheet in self.sheet_list:
            self.sheet_list[f'{sheet}'].print_sheet()
            return
        else:
            print("Sheet not found!")

    def change_val(self):
        self.list_sheet()
        sheet = input("Enter a sheet to be changed: ")
        if self.sheet_list[f'{sheet}']:
            self.sheet_list[f'{sheet}'].change_value()
        else:
            print("Sheet doesn't exist!")

    def change_right(self):
        self.list_sheet()
        sheet = input("Enter a sheet to be changed: ")
        if sheet in self.sheet_list:
            right = int(input("Enter the right(0 for R only, 1 for RW): "))
            if not (right == 0 or right == 1):
                print("Invalid right code !")
                return
            self.sheet_list[sheet].set_right(right)

    def share_user(self):
        self.list_sheet()
        sheet = input("Enter a sheet to be shared: ")
        if sheet in self.sheet_list:
            print("Here's people who can access the sheet: ")
            for i, x in enumerate(self.sheet_list[sheet].access):
                print(f"{i+1}. {x}")
            print("--------------------")
            self.user_list()
            print("--------------------")
            user = input("Enter a new user to share or an existed user to unshare: ")
            if user == event.current_user_name:
                print("You cannot share a list with yourself !")
                return
            elif user not in event.user_list:
                print("User not found !")
                return
            if user in self.sheet_list[sheet].access:
                self.sheet_list[sheet].share_user(user)
                print(f"Sheet {sheet} is no longer sharing with {user}")
                return
            else:
                self.sheet_list[sheet].share_user(user)
                print(f"Sheet {sheet} is now sharing with {user}")
        else:
            print("Sheet doesn't exist!")
            return

    def user_list(self):
        print("User List: ")
        for x, i in enumerate(event.user_list):
            print(f"{x+1}. {i}")

    def can_access_sheet(self):
        print("Here is the sheet you can access: ")
        for x, i in enumerate(self.can_access):
            print(f"{x+1}. {i.name} by {i.master}")
        print("--------------------")
        sheet = input("Enter a sheet by Name Sheet or type Quit to leave:")
        act = int(input("Choose your action:\n1.Print\n2.Edit\nAction: "))
        print("--------------------")
        if sheet == "Quit" or sheet == "quit":
            return
        aut, sht = sheet.split(' ', 2)
        for s in self.can_access:
            if sht == s.name and aut == s.master:
                match act:
                    case 1:
                        s.print_sheet()
                        return
                    case 2:
                        s.change_value()
                        return
            else:
                print("Sheet not exists!")
                return

