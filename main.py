produtos = {
    '2000500': {
        'Nome': 'Capeleti',
        'Preço': 62.00,
        'Codigo': 5
    },
    '2002000': {
        'Nome': 'Nhoque',
        'Preço': 35.90,
        'Codigo': 20
    },
    '2001400': {
        'Nome': 'Lasanha 4 Queijos',
        'Preço': 56.90,
        'Codigo': 14
    }
}


def ler_cod(cod_bar):
  item_cod = cod_bar[:7]  # Extrai o código do item
  valor = float(cod_bar[7:])  # Extrai o valor
  item = produtos.get(item_cod)
  if item is None:
    return None, None  # Retorna None se o código de barras for inválido
  peso = (valor / item['Preço']) / 1000
  return item, peso


def carrinho():
  carrinho = []
  while True:
    cod_bar = input(
        "Digite o código de barras do produto (ou 'sair' para encerrar): ")
    if cod_bar.lower() == 'sair':
      break
    item, valor = ler_cod(cod_bar)
    if item is None:
      print("Código de barras inválido. Tente novamente.")
      continue
    carrinho.append((item, valor))

  return carrinho


def calcular_total(carrinho):
  total = 0
  for item, peso in carrinho:
    total += peso * item['Preço']
  return total


def imprimir_recibo(carrinho, total):
  print("===== Recibo =====")
  for item, peso in carrinho:
    valor_item = item['Preço'] * peso  # Calcula o valor do item individual
    print(f"R$ {valor_item:.2f} - {item['Nome']}: {peso:.3f} kg")
  print(f"Total: R$ {total:.2f}")
  print("==================")


carrinho_compras = carrinho()

if carrinho_compras:
  total_compra = calcular_total(carrinho_compras)
  imprimir_recibo(carrinho_compras, total_compra)

input("Pressione Enter para finalizar a compra...")
