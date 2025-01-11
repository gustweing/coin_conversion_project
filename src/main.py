from crud import init_db, imports

if __name__ == '__main__':
    init_db()
    print("Banco criado com sucesso.")
    imports()