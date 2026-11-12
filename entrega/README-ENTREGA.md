# Entrega — Desafio Onfly

## 1. Defeitos identificados e corrigidos

Os defeitos foram identificados com auxílio do GitHub Copilot, integrado ao VS Code, por meio do prompt registrado em `uso-de-ia/sessao.json`.

Foram identificados e corrigidos cinco problemas:

| Arquivo                                      | Defeito                                              | Causa raiz                                                                                                                                                            |
| -------------------------------------------- | ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `services/status_policy.py`                  | Reservas `NO_SHOW` eram consideradas faturáveis.     | A função `is_billable()` considerava faturável qualquer status diferente de `CANCELLED`.                                                                              |
| `services/currency_converter.py`             | Conversão cambial incorreta e perda de precisão.     | A implementação dividia o valor pela taxa e convertia `Decimal` para `float`, de forma desnecessária e em desacordo com a regra de negócio estabelecida no README.md. |
| `services/stay_calculator.py`                | Cálculo incorreto de noites na virada de mês ou ano. | O cálculo com `.day` estava utilizando apenas o dia do mês, ignorando a diferença real entre as datas.                                                                |
| `services/report_builder.py`                 | Ranking de hotéis em ordem incorreta.                | A ordenação utilizava o faturamento crescente, contrariando a especificação.                                                                                          |
| `repositories/csv_reservation_repository.py` | Leitura limitada a 200 reservas.                     | A leitura do CSV era interrompida por uma condição que limitava a quantidade de registros.                                                                            |

## 2. Investigação e abordagem

A investigação começou com a leitura do README e dos testes fornecidos, seguida pela execução de `pytest -q` para identificar as falhas iniciais.

Com auxílio do GitHub Copilot, foram analisados os arquivos envolvidos no processamento, comparando suas implementações com as regras de negócio especificadas.

Também foi executada a amostra de validação para verificar as divergências nos valores consolidados.

Após a identificação dos defeitos, foram aplicadas as seguintes correções:

- Considerar somente reservas `CONFIRMED` como faturáveis.
- Realizar a conversão cambial por multiplicação, removendo a conversão desnecessária para `float`.
- Calcular as noites utilizando a diferença entre os objetos `date` com o atributo `.days` da diferença entre a data final e inicial, ao invés do atributo `.day` em cada data.
- Ordenar os hotéis pelo faturamento decrescente e, em caso de empate, pelo identificador crescente.
- Remover o limite de 200 registros na leitura do CSV.

Os testes originais foram mantidos inalterados.

## 3. Testes adicionais

Foram adicionados dois testes para verificar cenários não cobertos diretamente pelos testes originais:

- `test_repository_limit.py`: verifica se todas as reservas de um CSV com mais de 200 registros são processadas.
- `test_top_hotels_tiebreak.py`: verifica se hotéis com o mesmo faturamento são ordenados pelo `hotel_id` em ordem crescente.

## 4. Como validar

Instalar as dependências:

```bash
pip install -r requirements-dev.txt
```

Executar todos os testes:

```bash
pytest -q
```

Executar o CLI:

```bash
PYTHONPATH=src python -m onfly_report \
  --input data/reservas_hoteis.csv \
  --rates data/taxas_cambio.csv \
  --output output/report.json
```

## 5. Resultado dos testes

Após as correções e a inclusão dos dois testes adicionais, a suíte completa foi executada com sucesso.

```text
txaif@LAPTOP-7GP8DC2I UCRT64 ~/OneDrive/Área de Trabalho/onfly/onfly-desafio-20261111T194048Z-1-001/onfly-desafio
$ python -m pytest -q
.......                                                                                      [100%]
7 passed in 0.84s
(.venv)
```

Todos os cinco testes originais e os dois testes adicionais foram aprovados.
