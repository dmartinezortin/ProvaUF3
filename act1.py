import functions as f

def main():
    adding = True

    #Per entrar a un bucle fins que l'usuari vulgui sortir
    while adding == True:
        #Es defineix el valor dels camps
        student_id, first_name, last_name, subject, grade = \
            f.request_int(1, 999, "Introdueix l'id dessitjat: "), \
            input("Nom de l'alumne: "), \
            input("Cognom de l'alumne: "), \
            input("Materia: "), \
            f.request_int(1, 999, "Nota: ")
        #Es converteix a un diccionari
        data = {'student_id':[student_id],
                'first_name':[first_name],
                'last_name':[last_name],
                'subject':[subject],
                'grade':[grade]
                }
        #Funcio per inserir al fitxer CSV
        f.insert(data)

        #Funcio per sortir del bucle
        adding = f.option()

    #Funcio per mostrar els calculs
    f.median()
if __name__ == '__main__':
    main()
