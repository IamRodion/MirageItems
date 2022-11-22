import sqlite3 as sql
import os, time
from sqlite3 import Error
from tabulate import tabulate



def clearScreen(): # Función que limpia la pantalla.
    if os.name == 'posix': # Sí es un OS unix se ejecutará el comando "clear".
        os.system("clear")
    else: # En otros casos (windows), se ejecutará "cls".
        os.system("cls")

def logWrite(text): # Función que registra texto en el archivo de logs.
    with open('log.txt', 'a') as log: # Abre el archivo de log.
        fecha, hora = time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S") # Obteniendo fecha y hora.
        log.write(f'[{fecha} {hora}] '+text+'\n') # Escribe el texto en el archivo de log.

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
    
def insertRow(Name, Type, Level, Armour, PrimaryStat, AmountPrimaryStat, Stamina, SecondaryStat, AmountSecondaryStat, BonusModifier1, BonusModifier2, Enchant): # Función que obtiene los valores de un item como argumentos y envía una solicitud SQL para registrarlo en la base de datos.
    cursor, conn = createCursor("MirageItems.db") # Obtiene el objeto cursor y conn de la base de datos.
    query = f"INSERT INTO Armaduras VALUES ('{Name}', '{Type}', {Level}, {Armour}, '{PrimaryStat}', {AmountPrimaryStat}, {Stamina}, '{SecondaryStat}', {AmountSecondaryStat}, '{BonusModifier1}', '{BonusModifier2}', '{Enchant}')" # Crea una solicitud SQL con las variables una vez obtenidas.
    cursor.execute(query) # Ejecutar una solicitud con el cursor.
    conn.commit() # Aplicar cambios.
    conn.close() # Cerrar conexión.

def createItem(): # Función que obtiene los datos para crear un item y lo envía a la base de datos.
    Name = input("Name: ")
    Type = input("Type: ")
    Level = input("Level: ")
    Armour = int(input("Armour: "))
    PrimaryStat = input("Name of Primary Stat: ")
    AmountPrimaryStat = int(input("Amount of Primary Stat: "))
    Stamina = int(input("Amount of Stamina: "))
    SecondaryStat = input("Name of Secondary Stat: ")
    AmountSecondaryStat = int(input("Amount of Secondary Stat: "))
    BonusModifier1 = input("First Bonus Modifier: ")
    BonusModifier2 = input("Second Bonus Modifier: ")
    Enchant = input("Enchant: ")
    insertRow(Name, Type, Level, Armour, PrimaryStat, AmountPrimaryStat, Stamina, SecondaryStat, AmountSecondaryStat, BonusModifier1, BonusModifier2, Enchant) # Registra los datos como un nuevo registro en la base de datos.

def showItem(query): # Muestra los datos resultantes de una query en una tabla.
    cursor, conn = createCursor("MirageItems.db") # Obtiene el objeto cursor y conn de la base de datos.
    cursor.execute(query)
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    print(tabulate(data, headers=["Name", "Type", "Level", "Armour", "Primary", "Amount", "Stamina", "Secondary", "Amount", "Bonus 1", "Bonus 2", "Enchant"]))

def main():
    pass

if __name__ == '__main__':
    main()
    showItem("SELECT * FROM 'Armaduras'" )







# ------------------- Código Reciclado -------------------

#insertRow('Crystal Mask', 'Light', 80, 3, 'Magic', 27, 9, 'N/A', 0, 'Empowered', '3 HP Regen', 'N/A')
#insertRow('Indigo Hat', 'Light', 60, 3, 'Magic', 21, 7, 'N/A', 0, 'Critic', 'OmniResist', 'N/A')
#insertRow('Soldier Helmet', 'Medium', 40, 3, 'Distance', 10, 5, 'Defence', 10, '2% Thorns', '2 HP Regen', 'N/A')
#insertRow('Arnisium Vest', 'Light', 70, 3, 'Magic', 24, 8, 'N/A', 0, 'Empowered', '2% Potions', 'N/A')

# if __name__ == '__main__':
#     create_connection(r"C:\sqlite\db\pythonsqlite.db")

#for i in data:
    #print(tabulate(data))
    # print("------------------------------------------")
    # print(f"Nombre: {i[0]}")
    # print(f"Tipo: {i[1]}")
    # print(f"Nivel Requerido: {i[2]}")
    # print(f"Armadura: {i[3]}")
    # print(f"Nombre del Stat Primario: {i[4]}")
    # print(f"Cantidad del Stat Primario: {i[5]}")
    # print(f"Cantidad de Stamina: {i[6]}")
    # print(f"Nombre del Stat Secundario: {i[7]}")
    # print(f"Cantidad del Stat Secundario: {i[8]}")
    # print(f"Nombre del Primer Bonus: {i[9]}")
    # print(f"Nombre del Segundo Bonus: {i[10]}")
    # print(f"Encantamiento: {i[11]}")

# def createDB(): # Esta función crea una base de datos.
#     conn = sql.connect("MirageItems.db") # Establece conexión con la base de datos, y en caso de no existir, la crea.
#     conn.commit() # Se utiliza el método "commit()" del objeto creado para realizar cambios.
#     conn.close() # Se cierra la conexión a la base de datos.

# def createTable(): # Función que crea tablas en la base de datos creada.
#     cursor, conn = createCursor("MirageItems.db") # Obtiene el objeto cursor y conn de la base de datos.
#     query = """CREATE TABLE IF NOT EXISTS Armaduras (
#         Name varchar(100) NOT NULL,
#         Type varchar(100) NOT NULL,
#         Level int,
#         Armour int,
#         PrimaryStat varchar(100) NOT NULL,
#         AmountPrimaryStat int NOT NULL,
#         Stamina int NOT NULL,
#         SecondaryStat varchar(100),
#         AmountSecondaryStat int,
#         BonusModifier1 varchar(100),
#         BonusModifier2 varchar(100),
#         Enchant varchar(100)
#         )""" # Solicitud SQL.
#     cursor.execute(query) # Ejecutar una solicitud con el cursor.
#     conn.commit() # Aplicar cambios.
#     conn.close() # Cerrar conexión.