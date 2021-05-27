STUDENTS_CSV = "files/students.csv"
import pandas as pd
#Demana un integer dins del rang establert, l'string s'utilitza per permetre que sigui mes modular
def request_int(min, max, str):
    num = -1
    while num < min or num > max:
        try:
            num = int(input(str))
        except:
            print("Introdueix un numero vàlid! ")
    return num

def insert(data):
    #Llegeix el csv
    aux_df = pd.DataFrame(data, columns=['student_id','first_name','last_name','subject','grade'])
    try:
        #Fa un append al df del csv ja existent, si retorna una excepcio es degut a que el csv esta buit.
        df = pd.read_csv(STUDENTS_CSV, usecols=['student_id','first_name','last_name','subject','grade'])
        df = df.append(aux_df, ignore_index=True)
        df.to_csv(STUDENTS_CSV, mode='w', index=False)

    except:
        #Si es dona la excepcio de que esta buit, assigna el valor al csv
        print("CSV buit, inserint...")
        aux_df.to_csv(STUDENTS_CSV, mode='w', index=False)

def option():
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
