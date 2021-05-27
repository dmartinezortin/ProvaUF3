import functions as f
def main():
    #Demana a l'usuari que vol fer
    option = f.main_menu()

    #Cas que vulgui la opció a
    if option.lower() == "a":
        f.insert_csv_to_db()
    elif option.lower() == "b":
        f.insert_data()
    elif option.lower() == "c":
        f.update_data

if __name__ == '__main__':
        main()
