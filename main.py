# CONDICIONES PARA PRESENTAR EL PROYECTO PARA EL EXAMEN FINAL DE LA MATERIA AUTÓMATAS Y GRAMÁTICAS

# Para aprobar el examen final de la materia deberán presentar un proyecto. 
# Dicho proyecto consistirá en desarrollar una aplicación, que permita, 
# sobre un archivo que incluye registros de tráfico de conexiones de wifi de varios usuarios 
# y con distintos dispositivos a una red wifi, encontrar información útil.

# El trabajo deberá cumplir con las siguientes pautas

#     • Ser realizado en grupo de hasta 4 alumnos como máximo.
#     • Incluir el nombre de los integrantes del grupo.
#     • Incluir explicación del proyecto: cuál es la información que se obtiene y su utilidad. 
#     • Explicación individual de la aplicación desarrollada.
#     • Ser implementado mediante Python y utilizando las herramientas y conocimientos visto en la materia.
#         ◦ Utilizar expresiones regulares y el modulo re de Python.
#         ◦ Identificar los campos relevantes a mostrar según la aplicación a realizar.
#         ◦ Mostrar la información en la interfaz desarrollada y exportar a Excel.
#         ◦ Trabajo para cada grupo:
#             1. Seguimiento algún usuario, en un día establecido, para ver el desplazamiento del usuario en el edificio donde se encuentra la red, 
#             a través de la MAC AP. Debe incluir una lista de usuarios y la posibilidad de ingresar un rango de fechas. 
#             Ricciardi Marcos - Taccetta, Nicolas -Tkaczek Tobías.

from registro import Registro

def main():

    registro = Registro()
    registro.mostrar_users() #Mostar lista de usuarios
    while registro.valid_user: #Elegir un usuario
         registro.select_user()
    registro.input_date_start() #Ingresar un rango de fechas
    registro.input_date_end()
    registro.show_activity() #Ver desplazamiento del usuario por MAC AP en el rango de fechas
    registro.export_activity() #Exportar informacion a excel


if __name__ == '__main__':
    main()