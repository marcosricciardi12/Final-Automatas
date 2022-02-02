from datetime import datetime
import re


class UserNotExist(Exception):
    pass

class InvalidDate(Exception):
    pass

class Registro:

    def __init__(self):
        self.cantreg = 0
        self.entrada = 0
        self.total_lines = 0
        self.valid_user = True
        self.invalid_date = True
        self.date_start = ""
        self.date_end = ""
        self.registro = []
        self.users = []
        self.user = ""
        self.registro_vacio()
        self.registro_lleno()

    def registro_vacio(self):    

        with open("acts-user1.txt","r") as archivo:
            self.total_lines = sum(1 for line in archivo)
            self.registro = [[[] for x in range(9)] for y in range(self.total_lines)]

    def registro_lleno(self):

        with open("acts-user1.txt","r") as archivo:
            for linea in archivo:
                self.entrada = 0
                for letra in linea:
                    if letra == ';' :
                        self.registro[self.cantreg][self.entrada] = "".join(self.registro[self.cantreg][self.entrada])
                        self.entrada += 1
                    elif letra == '\n' :
                        self.registro[self.cantreg][self.entrada] = "".join(self.registro[self.cantreg][self.entrada])
                        self.cantreg += 1
                    else:
                        self.registro[self.cantreg][self.entrada] += letra

    def mostrar_users(self):
        print("Lista de users:\n")
        for i in range(1, self.cantreg):
            if self.registro[i][1] not in self.users:
                self.users.append(self.registro[i][1])
                print("\t" + self.registro[i][1])     

    def select_user(self):
        try:
            self.user = input("\nIngrese el nombre del usuario que desea ver el desplazamiento: ")
            if self.user not in self.users:
                raise UserNotExist('El usuario ingresado no existe, intente nuevamente')
            else:
                print("\n El usuario ingresado es: " + self.user)
                self.valid_user = False

        except UserNotExist as e:
            self.valid_user = True
            print(e)

    def date_validate(self, date):
        try:
            re_fecha = re.compile(r'^(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[012])/((19|20)\d\d)$')
            if re_fecha.search(date) is None:
                raise InvalidDate('Formato de Fecha inválido')
            else:
                self.invalid_date = False

        except InvalidDate as e:
            self.invalid_date = True
            print(e)

    def input_date_start(self):
        self.invalid_date = True
        while self.invalid_date:
            self.date_start = input("\nIngrese fecha inicial (formato dd/mm/aaaa): ")
            self.date_validate(self.date_start)
        self.date_start = datetime.strptime(self.date_start, '%d/%m/%Y')
        print("La fecha ingresada es: " + str(self.date_start))

    def input_date_end(self):
        self.invalid_date = True
        while self.invalid_date:
            self.date_end= input("\nIngrese fecha final (formato dd/mm/aaaa): ")
            self.date_validate(self.date_end)
        self.date_end = datetime.strptime(self.date_end, '%d/%m/%Y')
        print("La fecha ingresada es: " + str(self.date_end))

    def show_activity(self):
        MAC_AP = []
        for i in range(1, self.cantreg):
            if(self.user == self.registro[i][1] and self.date_start <= datetime.strptime(self.registro[i][2][0:10], '%d/%m/%Y') and self.date_end >= datetime.strptime(self.registro[i][2][0:10], '%d/%m/%Y')):
                if self.registro[i][7] not in MAC_AP:
                    MAC_AP.append(self.registro[i][7])
                    print(self.registro[i])

    def export_activity(self):
        with open('activity_export.csv', 'w') as f:
            MAC_AP = []
            f.write("User; Date; MAC AP\n")
            f.write(self.user + ";" + "Intervalo: " + str(self.date_start) + " - " + str(self.date_end) + "; \n")
            for i in range(1, self.cantreg):
                if(self.user == self.registro[i][1] and self.date_start <= datetime.strptime(self.registro[i][2][0:10], '%d/%m/%Y') and self.date_end >= datetime.strptime(self.registro[i][2][0:10], '%d/%m/%Y')):
                    if self.registro[i][7] not in MAC_AP:
                        MAC_AP.append(self.registro[i][7])
                        f.write("\t;" + self.registro[i][2] + ";" + self.registro[i][7] + '\n')            