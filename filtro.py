import os
import pandas as pd

# Obtém a lista de todos os arquivos CSV na pasta atual
csv_files = [file for file in os.listdir() if file.endswith(".CSV")]

# DataFrame vazio para armazenar os dados combinados
combined_df = pd.DataFrame()

# Itera sobre os arquivos CSV e realiza o processo para cada um
for csv_file in csv_files:
    # Etapa 1: Ler o arquivo e extrair data e hora das 2 primeiras linhas
    with open(csv_file, "r") as f:
        lines = f.readlines()
        data_hora = lines[0].strip() + " " + lines[1].strip()

    # Etapa 2: Remover as 3 primeiras linhas do arquivo
    lines = lines[3:]

    # Etapa 3: Separar a nova 1ª linha em colunas (estão separadas por ",")
    header = lines[0].strip().split(",")

    # Etapa 4: Criar um DataFrame com os dados restantes do arquivo
    data = [line.strip().split(",") for line in lines[1:]]
    df = pd.DataFrame(data, columns=header)

    # Etapa 6: Trocar "." por "," em todas as colunas
    df = df.apply(lambda x: x.str.replace(".", ","))

    # Etapa 7: Adicionar colunas com os valores de data e hora
    df["Data e Hora"] = data_hora

    # Etapa 8: Adicionar uma coluna "ciclo" com valor 1 em cada linha
    df["Ciclo"] = 1

    # Etapa 9: Adicionar uma coluna de índice
    df.insert(10, "Índice", range(1, len(df) + 1))

    # Etapa 10: Encontrar linhas onde as 2ª a 4ª colunas são iguais a "-1" e fazer as modificações
    # Encontre as linhas com valor -1 em qualquer coluna
    mask = df.apply(lambda row: "-1" in row.values, axis=1)

    # Obtenha os índices das linhas com valor -1
    indices_menos_um = mask.index[mask].tolist()

    # Exclua as linhas com valor -1
    df = df.drop(index=indices_menos_um)

    # Adicione 1 ao valor da coluna "Ciclo" a partir de cada linha que tinha -1
    for indice in indices_menos_um:
        df.loc[indice:, 'Ciclo'] += 1

    # Etapa 11: Manter apenas as linhas com Latitude entre 0 e -45 e Longitude entre -30 e -60
    df["Latitude"] = df["Latitude"].str.replace(",", ".").astype(float)
    df["Longitude"] = df["Longitude"].str.replace(",", ".").astype(float)
    
    df = df[(df["Latitude"] <= 0) & (df["Latitude"] >= -45) & (df["Longitude"] <= -30) & (df["Longitude"] >= -60)]
    
    # Etapa 12: Trocar ponto por vírgula novamente nas colunas Latitude e Longitude
    df["Latitude"] = df["Latitude"].apply(lambda x: str(x).replace(".", ","))
    df["Longitude"] = df["Longitude"].apply(lambda x: str(x).replace(".", ","))

    # Etapa 13: Reindexar o DataFrame
    df.reset_index(drop=True, inplace=True)

    # Etapa 14: Adicionar uma coluna "Nome" com o nome do arquivo
    df["Nome"] = os.path.splitext(csv_file)[0]

    # Verificar se o arquivo de resultado já existe
    if os.path.isfile("resultado.csv"):
        existing_df = pd.read_csv("resultado.csv")
        df = existing_df.append(df, ignore_index=True)

    # Salvar os dados atualizados no arquivo CSV
    df.to_csv("resultado.csv", index=False)

    print(f"Processo concluído para '{csv_file}'.")

print("Todos os processos concluídos. Os dados foram adicionados a 'resultado.csv'.")