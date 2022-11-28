import sqlite3 as sql
import os, time
from sqlite3 import Error
from tabulate import tabulate

BANNER = """███╗   ███╗██╗   ██╗    ██╗████████╗███████╗███╗   ███╗███████╗
████╗ ████║╚██╗ ██╔╝    ██║╚══██╔══╝██╔════╝████╗ ████║██╔════╝
██╔████╔██║ ╚████╔╝     ██║   ██║   █████╗  ██╔████╔██║███████╗
██║╚██╔╝██║  ╚██╔╝      ██║   ██║   ██╔══╝  ██║╚██╔╝██║╚════██║
██║ ╚═╝ ██║   ██║       ██║   ██║   ███████╗██║ ╚═╝ ██║███████║
╚═╝     ╚═╝   ╚═╝       ╚═╝   ╚═╝   ╚══════╝╚═╝     ╚═╝╚══════╝"""

INFO = "\n[i] Programa que administra items de Mirage Realms en una base de datos SQLite.\n[i] Creado por Rodion (github.com/IamRodion)\n"
MENU1 = "[1] Registrar Item\n[2] Buscar Item\n[3] Modificar Item\n[4] Borrar Item\n[5] Modo Venta\n[6] Salir\n\n[?] Indique una opción: "

def logWrite(text): # Función que registra texto en el archivo de logs.
    with open('log.txt', 'a') as log: # Abre el archivo de log.
        fecha, hora = time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S") # Obteniendo fecha y hora.
        log.write(f'[{fecha} {hora}] '+text+'\n') # Escribe el texto en el archivo de log.

def clearScreen(): # Función que limpia la pantalla.
    if os.name == 'posix': # Sí es un OS unix se ejecutará el comando "clear".
        os.system("clear")
    else: # En otros casos (windows), se ejecutará "cls".
        os.system("cls")
    logWrite(f"Se ejecutó la función 'clearScreen()' correctamente.")

def createCursor(database): # Genera un objeto cursor a traves de una base de datos.
    conn = None
    try: # Intenta conectarse a la base de datos.
        conn = sql.connect(database) # Establece conexión con la base de datos, y en caso de no existir, la crea.
        logWrite("Se conectó correctamente a la base de datos.") # Registra en el archivo de logs la conexión.
    except Error as e: # En caso de no lograr conectar a la DB mostrará el error por pantalla.
        print(e)
        logWrite(f"Error al conectar a la base de datos: {e}") # Registra en el archivo de logs la conexión.
    finally: # En caso de lograr conectar, generará el objeto cursor y lo devolverá a traves de return.
        if conn:
            cursor = conn.cursor()
            logWrite("Se generó correctamente el cursor.")
            return cursor, conn # Devuelve el objeto cursor y el objeto conn para cerrar la conexión a la base de datos al final de la función.
    logWrite(f"Se ejecutó la función 'createCursor()' correctamente.")
    
def insertRow(Name, Type, Level, Armour, PrimaryStat, AmountPrimaryStat, Stamina, SecondaryStat, AmountSecondaryStat, BonusModifier1, BonusModifier2, Enchant, Sale): # Función que obtiene los valores de un item como argumentos y envía una solicitud SQL para registrarlo en la base de datos.
    cursor, conn = createCursor("MirageItems.db") # Obtiene el objeto cursor y conn de la base de datos.
    query = f"INSERT INTO Armaduras VALUES ('{Name}', '{Type}', {Level}, {Armour}, '{PrimaryStat}', {AmountPrimaryStat}, {Stamina}, '{SecondaryStat}', {AmountSecondaryStat}, '{BonusModifier1}', '{BonusModifier2}', '{Enchant}', '{Sale}')" # Crea una solicitud SQL con las variables una vez obtenidas.
    cursor.execute(query) # Ejecutar una solicitud con el cursor.
    input(f"\n[i] Se registró el item '{Name}' correctamente, presione Enter.")
    conn.commit() # Aplicar cambios.
    conn.close() # Cerrar conexión.
    logWrite(f"Se ejecutó la función 'insertRow()' correctamente.")

def createItem(): # Función que obtiene los datos para crear un item y lo envía a la base de datos.
    showHeader()
    print("\tREGISTRANDO ITEM\n")
    try:
        Name = input("[Name]: ")
        Type = input("[Type]: ")
        Level = input("[Level]: ")
        Armour = int(input("[Armour]: "))
        PrimaryStat = input("[Name of Primary Stat]: ")
        AmountPrimaryStat = int(input("[Amount of Primary Stat]: "))
        Stamina = int(input("[Amount of Stamina]: "))
        SecondaryStat = input("[Name of Secondary Stat]: ")
        AmountSecondaryStat = int(input("[Amount of Secondary Stat]: "))
        BonusModifier1 = input("[First Bonus Modifier]: ")
        BonusModifier2 = input("[Second Bonus Modifier]: ")
        Enchant = input("[Enchant]: ")
        Sale = input("[Sale]: ")
        insertRow(Name, Type, Level, Armour, PrimaryStat, AmountPrimaryStat, Stamina, SecondaryStat, AmountSecondaryStat, BonusModifier1, BonusModifier2, Enchant, Sale) # Registra los datos como un nuevo registro en la base de datos.
    except KeyboardInterrupt:
        pass
    except ValueError:
        input("\n[!] Se produjo un error, el dato ingresado no es del tipo requerido.")
    logWrite(f"Se ejecutó la función 'createItem()' correctamente.")

def showItem(query): # Muestra en una tabla los datos resultantes de una query.
    cursor, conn = createCursor("MirageItems.db") # Obtiene el objeto cursor y conn de la base de datos.
    cursor.execute(query) # Se ejecuta la solicitud pasada como argumento.
    data = cursor.fetchall() # Se vuelcan los datos en una variable.
    conn.commit() # Aplicar cambios
    conn.close() # Cerrar conexión
    print(tabulate(data, headers=["ID", "Name", "Type", "Level", "Armour", "Primary", "#", "Stamina", "Secondary", "#", "Bonus", "Bonus", "Enchant", "Sale"])) # Muestra los datos almacenados en la variable de forma ordenada en una tabla.
    logWrite(f"Se ejecutó la función 'showItem()' correctamente.")

def searchItem(): # Función que crea una query dependiendo de los filtros de búsqueda y la pasa a la función showItem().
    query = 'SELECT rowid, * FROM "Armaduras" ORDER BY rowid' # Consulta SQL a ser ejecutada.
    dataSearch = { # Diccionario con los datos por defecto de la búsqueda.
        "Nombre": "",
        "Tipo": "",
        "Nivel": ""
    }

    while True: # Loop infinito.
        try:
            showHeader() # Función que limpia la pantalla, muestra el banner y la información.
            print("\tFILTROS ACTUALES\n")
            print(f"[Nombre]: {dataSearch['Nombre']}\n[Tipo]: {dataSearch['Tipo']}\n[Level]: {dataSearch['Nivel']}\n") # Muestra los filtros actuales.
            showItem(query) # Mostrar los datos con la query actual.
            print("\n\tPARÁMETROS DE BÚSQUEDA\n[i] Enter para omitir filtro, 'Ctrl+C' para volver al menú anterior\n")

            for data in dataSearch.keys(): # Itera sobre los parámetros del filtro para que el usuario pueda elegir que datos buscar.
                dataSearch[data] = input(f'[{data}]: ') # Solicita al usuario el tipo de item que busca basado en sus datos.

            query = f'SELECT rowid, * FROM "Armaduras" WHERE Name LIKE "%{dataSearch["Nombre"]}%" AND Type LIKE "%{dataSearch["Tipo"]}%" AND Level LIKE "%{dataSearch["Nivel"]}%" ORDER BY rowid' # Query que toma los datos del filtro indicados por el usuario y los solicita a la base de datos.

        except KeyboardInterrupt: # Para salir del menú de búsqueda, se debe presionar Ctrl+C.
            break

    logWrite(f"Se ejecutó la función 'searchItem()' correctamente.")

def updateItem():
    id_item = ""
    while True:
        try:
            showHeader()
            print("\tREGISTRANDO ITEM\n")
            id_item = input("[?] Indique el ID del Item a modificar, 'Ctrl+C' para volver al menú anterior: ")
            if id_item.isnumeric():
                data = {
                    "Name" : "",
                    "Type" : "",
                    "Level" : "",
                    "Armour" : "",
                    "PrimaryStat" : "",
                    "AmountPrimaryStat" : "",
                    "Stamina" : "",
                    "SecondaryStat" : "",
                    "AmountSecondaryStat" : "",
                    "BonusModifier1" : "",
                    "BonusModifier2" : "",
                    "Enchant" : "",
                    "Sale" : ""
                }
                
                for key in data.keys():
                    data[key] = input(f'[{key}]: ')

                query = f'UPDATE "Armaduras" SET Name = "{data["Name"]}", Type = "{data["Type"]}", Level = {data["Level"]}, Armour = {data["Armour"]}, PrimaryStat = "{data["PrimaryStat"]}", AmountPrimaryStat = {data["AmountPrimaryStat"]}, Stamina = {data["Stamina"]}, SecondaryStat = "{data["SecondaryStat"]}", AmountSecondaryStat = {data["AmountSecondaryStat"]}, BonusModifier1 = "{data["BonusModifier1"]}", BonusModifier2 = "{data["BonusModifier2"]}", Enchant = "{data["Enchant"]}", Sale = "{data["Sale"]}" WHERE ROWID = {id_item}'

                cursor, conn = createCursor("MirageItems.db") # Obtiene el objeto cursor y conn de la base de datos.
                cursor.execute(query) # Se ejecuta la solicitud pasada como argumento.
                conn.commit() # Aplicar cambios
                conn.close() # Cerrar conexión

            else:
                input("[!] El ID indicado no es correcto, intente de nuevo")
                pass

        except KeyboardInterrupt: # Para salir del menú de modificación, se debe presionar Ctrl+C.
            break

    logWrite(f"Se ejecutó la función 'updateItem()' correctamente.")

def deleteItem(): # Función que elimina un item seleccionado.
    while True:
        try:
            showHeader()
            print("\tBORRANDO ITEM\n")
            id_item = input("[?] Indique el ID del Item a borrar, 'Ctrl+C' para volver al menú anterior: ")
            query = f'DELETE FROM "Armaduras" WHERE ROWID = {id_item}'

            cursor, conn = createCursor("MirageItems.db") # Obtiene el objeto cursor y conn de la base de datos.
            cursor.execute(query) # Se ejecuta la solicitud pasada como argumento.
            conn.commit() # Aplicar cambios
            conn.close() # Cerrar conexión
            input(f"[i] El item con ID {id_item} fue eliminado.")

        except KeyboardInterrupt: # Para salir del menú de eliminación, se debe presionar Ctrl+C.
            break
        except:
            input(f"[!] El ID indicado no es correcto, intente de nuevo.")
    logWrite(f"Se ejecutó la función 'deleteItem()' correctamente.")

def showHeader(): # Función que limpia la pantalla, muestra el banner y la información.
    clearScreen()
    print(BANNER)
    print(INFO)
    logWrite(f"Se ejecutó la función 'showHeader()' correctamente.")   

def mainMenu(): # Función que muestra el menú principal, y devuelve la opción que el usuario desea ejecutar.
    showHeader()
    option = input(MENU1)
    logWrite(f"Se ejecutó la función 'mainMenu()' correctamente.")
    return option

def main(): # Función principal.
    while True:
        option = mainMenu()
        if option == "1": # Registrar Item.
            createItem()
        elif option == "2": # Buscar Item.
            searchItem()
        elif option == "3": # Modificar Item
            updateItem()
        elif option == "4": # Borrar Item.
            deleteItem()
        elif option == "5": # Modo Venta
            pass
        elif option == "6": # Salir.
            print("\nCerrando programa...")
            break
        else:
            input("[!] La opción indicada es incorrecta.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt: # En caso que se detenga la ejecución a través del teclado (Ctrl+C) mostrará un mensaje y cerrará el programa
        print("\nCerrando programa...")