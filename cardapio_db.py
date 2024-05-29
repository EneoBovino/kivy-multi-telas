import sqlite3

# Create or connect to a database
conn = sqlite3.connect('cardapio.db')

# Create a cursor object
cursor = conn.cursor()

# Check if table 'cardapio' exists
cursor.execute('''
    SELECT count(name) FROM sqlite_master WHERE type='table' AND name='cardapio'
''')

# If the table does not exist, create it
if cursor.fetchone()[0] == 0:
    cursor.execute('''
        CREATE TABLE cardapio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            descricao TEXT,
            disponivel INTEGER DEFAULT 1,
            pedido TEXT
        )
    ''')

    conn.commit()


while True:
    nome = input("Nome do item (digite 'sair' para sair): ")
    if nome == "sair":
        break
    preco = float(input("Preço do item: "))
    descricao = input("Descrição do item: ")
    pedido = input("Pedido (1 - Cozinha, 2 - Bar): ")
    pedido = "Cozinha" if pedido == "1" else "Bar"

    cursor.execute(f'''
        INSERT INTO cardapio (nome, preco, descricao, pedido)
        VALUES ('{nome}', {preco}, '{descricao}', '{pedido}')
    ''')

    conn.commit()

conn.close()

# Insert data into the table
# cursor.execute('''
#     INSERT INTO cardapio (nome, preco, descricao)
#     VALUES ('Café', 5.0, 'Café preto quente')
# ''')

# cursor.execute('''
#     INSERT INTO cardapio (nome, preco, descricao)
#     VALUES ('Pão de queijo', 3.0, 'Pão de queijo quentinho')
# ''')

# cursor.execute('''
#     INSERT INTO cardapio (nome, preco, descricao)
#     VALUES ('Bolo', 7.0, 'Bolo de chocolate')
# ''')

# # Commit changes and close connection
# conn.commit()
# conn.close()

