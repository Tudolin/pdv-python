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
  peso = float(cod_bar[7:])  # Extrai o peso do produto
  item = produtos.get(item_cod)
  return item, peso


# Exemplo de uso
cod_bar = input("Insira o código de barras: ")
produto, valor = ler_cod(cod_bar)
if produto:
  peso = (valor / produto['Preço']) / 1000
  valor_t = valor / 1000
  print(
      f"Produto: {produto['Nome']}, Preço: R$ {valor_t:,.2f}, Peso: {peso:.3f}"
  )
else:
  print("Produto não encontrado")
