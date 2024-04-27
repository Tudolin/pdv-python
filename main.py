import csv

data = {}
with open("instance\produtos_export.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data[row['codigo_barras']] = row

def ler_cod(cod_bar):
    # Obter o código do item e o valor do código de barras
    item_cod = cod_bar[:7]
    valor = cod_bar[7:]
    valor = int(valor)

    # Tentar buscar o item por código de barras (usando o dicionário)
    try:
        item = data[item_cod]
        nome = item['nome']  # Obter o nome do produto
        preco = float(item[' preco '].replace('R$ ', ''))  # Obter e converter o preço

        # Calcular o peso **dentro do bloco return**
        peso = (valor / preco) / 1000

        return nome, peso, preco
    except KeyError:
        # Retornar None caso o código de barras não seja encontrado
        return None, None

    return nome, peso

def carrinho():
  carrinho = []
  while True:
    cod_bar = input(
        "Digite o código de barras do produto (ou 'P' para encerrar): ")
    if cod_bar.lower() == 'p':
      break
    item, valor, preco = ler_cod(cod_bar)
    if item is None:
      print("Código de barras inválido. Tente novamente.")
      continue
    carrinho.append((item, valor, preco))

  return carrinho


def calcular_total(carrinho):
    total = 0
    for item, valor, preco in carrinho:
        total += valor * preco
    return total



def imprimir_recibo(carrinho, total):
    print("===== Recibo =====")
    for item, _ , peso in carrinho:
        valor_item = _ * peso
        print(f"R$ {valor_item:.2f} - {item}:  VALOR - {peso:.2f} kg")
    print(f"Total: R$ {total:.2f}")
    print("==================")



carrinho_compras = carrinho()

if carrinho_compras:
  total_compra = calcular_total(carrinho_compras)
  imprimir_recibo(carrinho_compras, total_compra)

input("Pressione Enter para finalizar a compra...")
