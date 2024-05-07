# Ponto de Venda (PDV) em Flask

![Badge em Desenvolvimento](http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge)

* [Introdução](#introdução)
* [Instalação de Dependencias](#instalação-de-dependencias)
* [Estrutura do Código](#estrutura-do-código)
* [Importações](#importações)
* [Etiquetas para teste](#etiquetas-para-teste)
* [Variáveis](#variáveis)
* [Funções](#funções)
* [Rotas da aplicação](#rotas-da-aplicação)
* [Execução da Aplicação](#execução-da-aplicação)
* [Conclusão](#conclusão)

  
# Introdução

Este documento serve como guia para o aplicativo PDV desenvolvido em Flask. O objetivo principal do PDV é gerenciar vendas de produtos, incluindo a leitura de códigos de barras, cálculo de totais, impressão de recibos e geração de notas fiscais em PDF.

Inicialmente, o projeto surgiu como uma necessidade real de negócio, onde no comercio da minha família, não encontravamos nenhum sistema de pdv que pudesse atender somente a nossa necessidade real que era a frente de caixa.
Muito disso porque nós vendemos os alimentos por KG, fazendo com que cada etiqueta de código de barras fosse única, assim, nenhum programa que inicialmente foi desenvolvido para mercados que utilizam etiquetas "estáticas" funcionava.

Assim, analisando a etiqueta, percebi um padrão, que era, os 7 primeiros digitos eram utilizados para identificação do item no nosso sistema de balança, exemplo, Nhoque, Código 20, então o código de barras dele ficaria "2002000039025" sendo os primeiros 7 utilizados para identificação e os 6 ultimos o valor da etiqueta, nesse caso, "R$ 39,02".

Seguindo essa lógica, o código foi desenvolvido para quebrar e fazer o calculo pensando nessa lógica, tendo como exceções itens vendidos por kg e itens que não fazem parte do nosso sistema, como refrigerantes, doces e água por exemplo.

# Instalação de Dependencias

> pip install -r requirements.txt

# Etiquetas para teste

![etiquetas](https://github.com/Tudolin/pdv-python/assets/108036444/b4b8101f-a9c5-45b4-952e-ab2983667a99)


# Estrutura do Código

O código Python do PDV está organizado da seguinte maneira:

## Importações:

csv: Para manipulação de arquivos CSV.

json: Para leitura e escrita de arquivos JSON.

os: Para interação com o sistema operacional.

datetime: Para manipulação de datas e horários.

Flask: Biblioteca principal do Flask para criação de aplicações web.

url_for: Função para gerar URLs dinâmicas.

reportlab.lib.pagesizes: Módulo para definição de tamanhos de página em PDF.

reportlab.pdfgen.canvas: Classe para criação de documentos PDF.

## Variáveis:

metodo_pagamento: Armazena o método de pagamento selecionado pelo cliente.
data: Dicionário contendo os dados dos produtos carregados do arquivo produtos_export.csv.
carrinho: Lista que armazena os itens do carrinho de compras.

## Funções:

ler_cod(cod_bar): Lê um código de barras e retorna o nome, peso e preço do produto correspondente.

adicionar_venda(carrinho, total, cpf): Adiciona uma nova venda à lista de vendas e salva em um arquivo JSON.

print_pdf(filename): Envia um arquivo PDF para a impressora especificada.
pdv(): Função principal do PDV que gerencia a interface do usuário e as operações de venda.

exibir_recibo(): Exibe um recibo HTML com os itens do carrinho e o total da venda.

calcular_total(carrinho): Calcula o total da venda com base nos itens do carrinho.

imprimir_recibo(carrinho, total): Gera um recibo em formato de lista contendo os itens do carrinho e o total da venda.

delete_item(item): Remove um item específico do carrinho de compras.

checkout(): Processa o pagamento da venda, calcula o troco (se houver) e exibe a página de finalização da compra.

finalizar_compra(): Zera o carrinho de compras e redireciona o usuário para a página inicial.

imprimir_nf(): Gera uma nota fiscal em PDF com os dados da venda e salva o arquivo no computador do cliente.

generate_receipt(): Gera um recibo em PDF com os dados da venda e envia o arquivo para a impressora.

## Rotas da Aplicação:

'/': Rota principal do PDV que exibe a interface do usuário para leitura de códigos de barras.
![pdv](https://github.com/Tudolin/pdv-python/assets/108036444/b3cf8c90-8d0f-44a7-8ea5-4c3f82dd2ae7)


'/recibo': Rota que exibe o carrinho da venda.
![carrinho](https://github.com/Tudolin/pdv-python/assets/108036444/398d8c2a-e4a9-4861-891e-ceae8f712b54)



'/delete/<item>': Rota que remove um item específico do carrinho de compras.

'/finalizar': Rota que processa o pagamento da venda e exibe a página de finalização da compra.
![recibo](https://github.com/Tudolin/pdv-python/assets/108036444/db7f8a45-65a9-4841-a1a2-3e88c6aed0f1)


'/zerar_carrinho': Rota que zera o carrinho de compras e redireciona o usuário para a página inicial.

'/recibo': Rota que gera a nota fiscal em PDF e a salva no computador do cliente.
![nota](https://github.com/Tudolin/pdv-python/assets/108036444/4b62607a-4ffe-4afd-a9d7-677b08d5fa1d)

'/gerar_recibo': Rota que gera o recibo em PDF e envia o arquivo para a impressora.

# Execução da Aplicação:

Para executar o PDV, utilize o seguinte comando no terminal:

> python main.py

# Observações:

O código assume que o arquivo produtos_export.csv contendo os dados dos produtos está localizado no diretório instance.
As configurações de impressão devem ser ajustadas de acordo com a impressora utilizada.

O aplicativo PDV está em constante desenvolvimento e novas funcionalidades podem ser adicionadas no futuro.
Recursos Adicionais:

Documentação do [Flask](https://palletsprojects.com/p/flask/)

# Conclusão

O Ponto de Venda (PDV) em Flask oferece uma solução completa para gerenciamento de vendas em lojas de varejo. O código é bem estruturado, com funções e variáveis ​​claramente definidas, facilitando sua compreensão e modificação. A aplicação possui diversas funcionalidades, desde a leitura de códigos de barras até a geração de notas fiscais em PDF, atendendo às necessidades básicas de um PDV.

## Pontos fortes do PDV:

Facilidade de uso: A interface do usuário é intuitiva e simples de usar, permitindo que operadores iniciantes aprendam rapidamente a utilizar o sistema.
Flexibilidade: O código é modular e pode ser facilmente adaptado para atender às necessidades específicas de cada negócio.

Recursos completos: O PDV oferece diversas funcionalidades essenciais para gerenciamento de vendas, como leitura de códigos de barras, cálculo de totais, impressão de recibos e geração de notas fiscais.

Tecnologia robusta: O Flask é uma biblioteca Python popular e confiável, garantindo a estabilidade e o desempenho do PDV.

# Considerações finais:

O PDV em Flask é uma ferramenta valiosa para lojas de varejo que buscam otimizar seus processos de venda e melhorar a experiência do cliente. A aplicação oferece uma base sólida para o desenvolvimento de um sistema completo de gestão de vendas, atendendo às necessidades de diversos tipos de negócios.

## Recomendações para aprimoramento:


Relatórios de vendas: O PDV poderia gerar relatórios de vendas detalhados para auxiliar na análise de dados e na tomada de decisões estratégicas.

Acredito que o PDV em Flask tem grande potencial para se tornar uma ferramenta essencial para o gerenciamento de vendas em lojas de varejo. Com aprimoramentos contínuos, a aplicação pode se adaptar às necessidades dinâmicas do mercado e oferecer soluções inovadoras para o setor.
