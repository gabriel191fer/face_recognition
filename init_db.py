import sqlite3

# Conecta ao banco de dados. Se não existir, ele será criado neste momento.
conn = sqlite3.connect('my_database.db')

# Crie um cursor. O cursor é usado para percorrer os registros do resultado.
c = conn.cursor()

# Crie uma tabela chamada 'people' com duas colunas: 'name' e 'photo'.
c.execute("""
CREATE TABLE people (
    name TEXT,
    photo BLOB
)
""")

# Salve (commit) as mudanças
conn.commit()

# Feche a conexão
conn.close()
