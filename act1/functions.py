import pandas as pd
from act2.creds import creds
import mysql.connector
from mysql.connector import errorcode

STUDENTS_CSV = "files/students.csv"
ACT2_CSV = "files/prospects.csv"


#Demana un integer dins del rang establert, l'string s'utilitza per permetre que sigui mes modular
def request_int(min, max, str):
    num = -1
    while num < min or num > max:
        try:
            num = int(input(str))
        except:
            print("Introdueix un numero vàlid! ")
    return num

def insert(CSV, cols, data):
    #Llegeix el csv
    aux_df = pd.DataFrame(data, columns=cols)
    try:
        #Fa un append al df del csv ja existent, si retorna una excepcio es degut a que el csv esta buit.
        df = pd.read_csv(CSV, usecols=cols)
        df = df.append(aux_df, ignore_index=True)
        df.to_csv(CSV, mode='w', index=False)

    except:
        #Si es dona la excepcio de que esta buit, assigna el valor al csv
        print("CSV buit, inserint...")
        aux_df.to_csv(STUDENTS_CSV, mode='w', index=False)

def sn_option():
    n = str()
    #Fa un bucle fins que l'usuari posi "S" o "N"
    while n.lower() != "n" and n.lower() != "s":
        n = input("Vols afegir mes registres? S/N ")
    #Retorna False si es N i si es S retorna True
    return False if n.lower() == "n" else True

def median():
    #Llegeix el CSV
    df = pd.read_csv(STUDENTS_CSV, usecols=['student_id','first_name','last_name','subject','grade'])
    #Calcula quants estudiants son al CSV
    total_students = len(df.index)
    #Calcula la media dels estudiants
    students_median = df['grade'].sum()/total_students
    #Obte el valor minim de totes les notes al dataframe
    min_value = df['grade'].min()
    #Obte el valor maxim de totes les notes al dataframe
    max_value = df['grade'].max()
    #Es crea una llista canviant l'ordre de les columnes
    cols = ['subject','student_id','first_name','last_name','grade']
    #Es canvia el dataframe amb l'ordre canviat
    df = df[cols]
    #Printa el dataframe i els calculs realitzats.
    print(df)
    print("La media dels estudiants es de", students_median, "Nota minima", min_value, "Nota Maxima", max_value)

def main_menu():
    #Demana un valor inicial
    selected_val = input("Qué vols fer?"
                         "\na. carregar CSV a la bbdd: "
                         "\nb. inserir nous registres a la bbdd: "
                         "\nc. modificar les dades inserides (demanant l’identificador del registre)"
                         "\nd. consultar les dades actuals a la bbdd:"
                         "\ne. sortir")
    #Llista de les opcions permitides
    available_options = ['a', 'b','c','d','e']
    #Bucle fins que l'usuari fiqui una opcio permitida
    while selected_val.lower() not in available_options:
        selected_val = input("Qué vols fer?"
                         "\na. carregar CSV a la bbdd: "
                         "\nb. inserir nous registres a la bbdd: "
                         "\nc. modificar les dades inserides (demanant l’identificador del registre)"
                         "\nd. consultar les dades actuals a la bbdd:"
                         "\ne. sortir\n")
    return selected_val

def df_to_list():
    try:
        df = pd.read_csv(ACT2_CSV)
        return df.values.tolist()
    except:
        return list()

def insert_csv_to_db():
    try:
        cnx = mysql.connector.connect(user=creds['user'],
                                      password=creds['pass'],
                                      host=creds['host'],
                                      database=creds['database'])
        crs = cnx.cursor()
        to_add = tuple(df_to_list())
        if len(to_add) < 1:
            print("Fitxer buit.")
        else:
            print("Carregant dades...")
            for item in to_add:
                try:
                    crs.execute("INSERT INTO prospects "
                                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                (item))

                    cnx.commit()
                except mysql.connector.IntegrityError:
                    print(f"Valor amb ID ja existent, passant al seguent id... (ID duplicat: {item[0]})")
            print(f"Base de dades actualitzada, total de registres afegits: {crs.rowcount}")
            crs.close()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

def tuple_to_db(data):
    try:
        cnx = mysql.connector.connect(user=creds['user'],
                                      password=creds['pass'],
                                      host=creds['host'],
                                      database=creds['database'])
        crs = cnx.cursor()
        print("Carregant dades...")
        try:
            crs.execute("INSERT INTO prospects "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        data)

            cnx.commit()
        except mysql.connector.IntegrityError:
            print(f"Valor amb ID ja existent, passant al seguent id... (ID duplicat: {data[0]})")
        print(f"Base de dades actualitzada, total de registres afegits: {crs.rowcount}")
        crs.close()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


def insert_data():
    prospect_id, first_name, last_name, interview_date, telephone, grade, interviewer, valid = \
        request_int(1, 999, "Introdueix l'id dessitjat: "), \
        input("El nom: "), \
        input("El cognom: "), \
        input("Data de entrevista: "),\
        input("Telefon"), \
        request_int(1, 10, "Grade: "), \
        input("Entrevistador: "), \
        request_int(0, 1, "Valid: "), \
    # Es converteix a un diccionari
    data = (prospect_id, first_name,last_name,interview_date,telephone,grade,interviewer,valid)
    tuple_to_db(data)