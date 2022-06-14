# House Rocket 

Esse é um projeto ficticio. A empresa e os problemas de negócio. As instruções para realização do projeto, foram recomendações do blog [Seja um Data Scientist](https://medium.com/@meigarom/os-5-projetos-de-data-science-que-fará-o-recrutador-olhar-para-você-c32c67c17cc9).

# 1. Descrição
A House Rocket é uma empresa que trabalha com compra e venda de imóveis. A empresa está em busca de maximizar sua receita, encontrando as melhores oportunidades de negócio, dessa forma o Cientista de Dados precisa identificar as melhores opções de compra de imóveis, assim como a melhor hora para vende-los.
Os imóveis apresentam diferentes características que fazem os preços variarem de acordo com seus atributos. As questões a serem respondidas são:

**1**. Quais casas o CEO da House Rocket deveria comprar e por qual preço de compra?

**2.** Uma vez a casa em posse da empresa, qual o melhor momento para vendê-las e qual seria o preço da venda?

# 2. Atributos 

|    Atributos    |                         Significado                          |
| :-------------: | :----------------------------------------------------------: |
|       id        |       Numeração única de identificação de cada imóvel        |
|      date       |                    Data da venda da casa                     |
|      price      |    Preço que a casa está sendo vendida pelo proprietário     |
|    bedrooms     |                      Número de quartos                       |
|    bathrooms    | Número de banheiros (0.5 = banheiro em um quarto, mas sem chuveiro) |
|   sqft_living   | Medida (em pés quadrado) do espaço interior dos apartamentos |
|    sqft_lot     |     Medida (em pés quadrado)quadrada do espaço terrestre     |
|     floors      |                 Número de andares do imóvel                  |
|   waterfront    | Variável que indica a presença ou não de vista para água (0 = não e 1 = sim) |
|      view       | Um índice de 0 a 4 que indica a qualidade da vista da propriedade. Varia de 0 a 4, onde: 0 = baixa  4 = alta |
|    condition    | Um índice de 1 a 5 que indica a condição da casa. Varia de 1 a 5, onde: 1 = baixo \|-\| 5 = alta |
|      grade      | Um índice de 1 a 13 que indica a construção e o design do edifício. Varia de 1 a 13, onde: 1-3 = baixo, 7 = médio e 11-13 = alta |
|  sqft_basement  | A metragem quadrada do espaço habitacional interior acima do nível do solo |
|    yr_built     |               Ano de construção de cada imóvel               |
|  yr_renovated   |                Ano de reforma de cada imóvel                 |
|     zipcode     |                         CEP da casa                          |
|       lat       |                           Latitude                           |
|      long       |                          Longitude                           |
| sqft_livining15 | Medida (em pés quadrado) do espaço interno de habitação para os 15 vizinhos mais próximo |
|   sqft_lot15    | Medida (em pés quadrado) dos lotes de terra dos 15 vizinhos mais próximo |

# 3. Premissas de Negócio 

Quais premissas foram adotadas para este projeto:

- As seguintes premissas foram consideradas para esse projeto:
- Os valores iguais a zero em **yr_renovated** são casas que nunca foram reformadas.
- O valor igual a 33 na coluna **bathroom** foi considerada um erro e por isso foi delatada das análises
- A coluna **price** significa o preço que a casa foi / será comprada pela empresa House Rocket
- Valores duplicados em ID foram removidos e considerados somente a compra mais recente
- A localidade e a condição do imóvel foram características decisivas na compra ou não do imóvel
- A estação do ano foi a característica decisiva para a época da venda do imóvel

# 4. Estratégia de Solução

Quais foram as etapas para solucionar o problema de negócio:

1. Coleta de dados via Kaggle

2. Entendimento de negócio

3. Tratamento de dados 

3.1. ​	Tranformação de variaveis 

3.2. ​	Limpeza 

3.3. ​	Entendimento

4. Exploração de dados

5. Responder problemas do negócio

6. Resultados para o negócio

7. Conclusão

# 5. Top Insights

Insights mais relevantes para o projeto:

Imóveis renovados recentemente são 35% mais caros

**Falso**: Imóveis antigos e atuais possuem uma faixa de preço equivalente.

Imóveis em más condições, mas com uma boa vista são 10% mais caros.

**Falso**: Imóveis em más condições e com vista ruim são mais caros.

Crescimento do preço mês após mês em 2014 é de 10%.

**Falso**: O preço dos imóveis são mais caros entre o mês 3 e 6.
