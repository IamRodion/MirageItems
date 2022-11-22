import sqlite3 as sql 
import os

def createDB(): # Esta función crea una base de datos.
    conn = sql.connect("MirageItems.db") # Establece conexión con la base de datos, y en caso de no existir, la crea.
    conn.commit() # Se utiliza el método "commit()" del objeto creado para realizar cambios
    conn.close() # Se cierra la conexión a la base de datos

def createTable(): # Función que crea tablas en la base de datos creada
    conn = sql.connect("MirageItems.db") # Se establece conexión con la base de datos
    cursor = conn.cursor() # Se crea un objeto "cursor" el permite apuntar que ejecuciones se harán y donde en la base de datos.
    query = """CREATE TABLE IF NOT EXISTS Armaduras (
        Name varchar(100) NOT NULL,
        Type varchar(100) NOT NULL,
        Level int,
        Armour int,
        PrimaryStat varchar(100) NOT NULL,
        AmountPrimaryStat int NOT NULL,
        Stamina int NOT NULL,
        SecondaryStat varchar(100),
        AmountSecondaryStat int,
        BonusModifier1 varchar(100),
        BonusModifier2 varchar(100),
        Enchant varchar(100)
        )"""
    cursor.execute(query) # Ejecutar una solicitud con el cursor
    conn.commit()
    conn.close()

def insertRow(Name, Type, Level, Armour, PrimaryStat, AmountPrimaryStat, Stamina, SecondaryStat, AmountSecondaryStat, BonusModifier1, BonusModifier2, Enchant):
    conn = sql.connect("MirageItems.db")
    cursor = conn.cursor()
    query = f"INSERT INTO Armaduras VALUES ('{Name}', '{Type}', {Level}, {Armour}, '{PrimaryStat}', {AmountPrimaryStat}, {Stamina}, '{SecondaryStat}', {AmountSecondaryStat}, '{BonusModifier1}', '{BonusModifier2}', '{Enchant}')"
    cursor.execute(query)
    conn.commit()
    conn.close()

def saveItem():
    os.system("clear")
    Name = input("Nombre: ")
    Type = input("Tipo: ")
    Level = input("Nivel Requerido: ")
    Armour = int(input("Armadura: "))
    PrimaryStat = input("Nombre del Stat Primario: ")
    AmountPrimaryStat = int(input("Cantidad del Stat Primario: "))
    Stamina = int(input("Cantidad de Stamina: "))
    SecondaryStat = input("Nombre del Stat Secundario: ")
    AmountSecondaryStat = int(input("Cantidad del Stat Secundario: "))
    BonusModifier1 = input("Nombre del Primer Bonus: ")
    BonusModifier2 = input("Nombre del Segundo Bonus: ")
    Enchant = input("Encantamiento: ")
    insertRow(Name, Type, Level, Armour, PrimaryStat, AmountPrimaryStat, Stamina, SecondaryStat, AmountSecondaryStat, BonusModifier1, BonusModifier2, Enchant)

def showItem():
    conn = sql.connect("MirageItems.db")
    cursor = conn.cursor()
    query = "SELECT * FROM Armaduras"
    cursor.execute(query)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    os.system("clear")
    for i in datos:
        print("------------------------------------------")
        print(f"Nombre: {i[0]}")
        print(f"Tipo: {i[1]}")
        print(f"Nivel Requerido: {i[2]}")
        print(f"Armadura: {i[3]}")
        print(f"Nombre del Stat Primario: {i[4]}")
        print(f"Cantidad del Stat Primario: {i[5]}")
        print(f"Cantidad de Stamina: {i[6]}")
        print(f"Nombre del Stat Secundario: {i[7]}")
        print(f"Cantidad del Stat Secundario: {i[8]}")
        print(f"Nombre del Primer Bonus: {i[9]}")
        print(f"Nombre del Segundo Bonus: {i[10]}")
        print(f"Encantamiento: {i[11]}")


if __name__ == '__main__':
    #createDB()
    #createTable()
    #saveItem()
    #insertRow('Crystal Mask', 'Light', 80, 3, 'Magic', 27, 9, 'N/A', 0, 'Empowered', '3 HP Regen', 'N/A')
    #insertRow('Indigo Hat', 'Light', 60, 3, 'Magic', 21, 7, 'N/A', 0, 'Critic', 'OmniResist', 'N/A')
    #insertRow('Soldier Helmet', 'Medium', 40, 3, 'Distance', 10, 5, 'Defence', 10, '2% Thorns', '2 HP Regen', 'N/A')
    #insertRow('Arnisium Vest', 'Light', 70, 3, 'Magic', 24, 8, 'N/A', 0, 'Empowered', '2% Potions', 'N/A')
    showItem()





#from sqlite3 import Error

# def create_connection(db_file):
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#         print(sqlite3.version)
#     except Error as e:
#         print(e)
#     finally:
#         if conn:
#             conn.close()


# if __name__ == '__main__':
#     create_connection(r"C:\sqlite\db\pythonsqlite.db")