from datetime import datetime
import re
from tabulate import tabulate
import pandas as pd
from colorama import Fore, init, Back
from clearscreen import clearscreen
init(autoreset=True) 

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
        self.print_info()

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
                print(Fore.CYAN + "\t" + self.registro[i][1])     

    def select_user(self):
        try:
            self.user = input(Fore.YELLOW + "\nIngrese el nombre del usuario que desea ver el desplazamiento: " + Fore.GREEN)
            if self.user not in self.users:
                raise UserNotExist(Fore.RED + 'El usuario ingresado no existe, intente nuevamente')
            else:
                clearscreen()
                print(Fore.YELLOW +"\n El usuario ingresado es: " + Fore.GREEN + self.user)
                self.valid_user = False

        except UserNotExist as e:
            self.valid_user = True
            print(e)

    def date_validate(self, date):
        try:
            re_fecha = re.compile(r'^(0?[1-9]|[12][0-9]|30)/(0?[469]|11)/((19|20)\d\d)$|^(0?[1-9]|[12][0-9]|31)/(0?[13578]|1[02])/((19|20)\d\d)$|^(0?[1-9]|[12][0-8])/(0?2)/((19|20)\d\d)$')
            if re_fecha.search(date) is None:
                raise InvalidDate(Fore.RED + 'Formato de Fecha inv??lido' + Fore.GREEN)
            else:
                self.invalid_date = False

        except InvalidDate as e:
            self.invalid_date = True
            print(e)

    def input_date_start(self):
        self.invalid_date = True
        while self.invalid_date:
            self.date_start = input(Fore.YELLOW + "\nIngrese fecha inicial (formato dd/mm/aaaa): " + Fore.GREEN)
            self.date_validate(self.date_start)
        self.date_start = datetime.strptime(self.date_start, '%d/%m/%Y')
        print(Fore.GREEN + "La fecha ingresada es: " + str(self.date_start))

    def input_date_end(self):
        self.invalid_date = True
        while self.invalid_date:
            self.date_end= input(Fore.YELLOW +"\nIngrese fecha final (formato dd/mm/aaaa): " + Fore.GREEN)
            self.date_validate(self.date_end)
        self.date_end = datetime.strptime(self.date_end, '%d/%m/%Y')
        print(Fore.GREEN +"La fecha ingresada es: " + str(self.date_end))

    def show_activity(self):
        clearscreen()
        print(Fore.YELLOW +"El usuario es: " + Fore.GREEN + self.user)
        print(Fore.GREEN + "La fecha de inicio de b??squeda es: " + str(self.date_start))
        print(Fore.GREEN +"La fecha de fin de b??squeda es: " + str(self.date_end))
        DATEMAC = []
        MAC_AP = []
        INDEX_USER = []
        for i in range(1, self.cantreg):
            if(self.user == self.registro[i][1] and self.date_start <= datetime.strptime(self.registro[i][2][0:10], '%d/%m/%Y') 
            and self.date_end >= datetime.strptime(self.registro[i][2][0:10], '%d/%m/%Y')):
                INDEX_USER.append(i)
                if len(INDEX_USER) >= 2:
                    if self.registro[INDEX_USER[-2]][7] != self.registro[i][7]:
                        MAC_AP.append(self.registro[i][7])
                        DATEMAC.append(self.registro[i][2])
        myData={"User":self.user, "Date": DATEMAC, "MAC AP": MAC_AP}
        myDataFrame=pd.DataFrame(myData)
        input(Fore.YELLOW + "\n\n\t\tPresione enter para continuar" + Fore.CYAN)
        print(tabulate(myDataFrame, headers='keys', tablefmt='psql', stralign='center'))

    def export_activity(self):
        with open('activity_export.csv', 'w') as f:
            INDEX_USER = []
            f.write("User; Date; MAC AP\n")
            f.write(self.user + ";" + "Intervalo: " + str(self.date_start) + " - " + str(self.date_end) + "; \n")
            for i in range(1, self.cantreg):
                if(self.user == self.registro[i][1] and self.date_start <= datetime.strptime(self.registro[i][2][0:10], '%d/%m/%Y') and self.date_end >= datetime.strptime(self.registro[i][2][0:10], '%d/%m/%Y')):
                    INDEX_USER.append(i)
                    if len(INDEX_USER) >= 2:
                        if self.registro[INDEX_USER[-2]][7] != self.registro[i][7]:
                            f.write("\t;" + self.registro[i][2] + ";" + self.registro[i][7] + '\n')

    def print_info(self):
        print(Fore.GREEN + "\tFINAL AUTOMATAS Y GRAMATICAS")
        print(Fore.BLUE + "\nIntegrantes:" + Fore.CYAN + "\t-Ricciardi, Marcos \n\t\t-Taccetta, Nicolas \n\t\t-Tkaczek, Tob??as")
        print(Fore.BLUE + "\nConsigna:\t" + Fore.CYAN + "Seguimiento alg??n usuario, en un d??a establecido, para ver el desplazamiento")
        print(Fore.CYAN + "\t\tdel usuario en el edificio donde se encuentra la red, a trav??s de la MAC AP")
        print(Fore.CYAN + "\t\tDebe incluir una lista de usuarios y la posibilidad de ingresar un rango de fechas.")
        input(Fore.YELLOW + "\n\n\t\tPresione enter para continuar" + Fore.BLUE)
        clearscreen()