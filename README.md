# FIAP Exploring Database Options

## Grupo

* Bernardo Couto
* Raphael Freixo
* Ronaldo Nolasco

## Dataset

* **URL**: https://www.kaggle.com/elemento/nyc-yellow-taxi-trip-data
* **Tamanho**: 7 GB

## Arquitetura

![Arquitetura](./documentation/image/architecture.png)

## Deploy

Toda a infra-estrutura foi construída utilizando o conceito de IaC através do Serverless Framework.

Além disso, o workflow de CI/CD foi construído com o GitHub Actions conforme descrito no arquivo [deploy.yaml](./.github/workflows/deploy.yaml).

## Matadados

Nome de campo |	Descrição
--------------|----------
VendorID | Um código indicando o provedor TPEP que forneceu o registro. (1 - Creative Mobile Technologies, 2 - VeriFone Inc.)
tpep_pickup_datetime | A data e a hora em que o medidor estava ligado.
tpep_dropoff_datetime | A data e a hora em que o medidor foi desligado.
passenger_count | O número de passageiros no veículo. Este é um valor inserido pelo motorista.
trip_distance | A distância de viagem decorrido em milhas relatadas pelo taxímetro.
pickup_longitude | Longitude onde o medidor estava ligado.
pickup_latitude | Latitude onde o medidor estava ligado.
RateCodeID | O código de taxa final em vigor no final da viagem. (1- Taxa padrão, 2 -JFK, 3 - Newark, 4 - Nassau ou Westchester, 6 - Tarifa negociada, 7 - Passeio em grupo)
store_and_fwd_flag | Esta bandeira indica se o registro da viagem foi mantido na memória do veículo antes de enviar para o fornecedor, também conhecido como "loja e frente", porque o veículo não tinha conexão com o servidor. (Y - Loja e viagem para a frente, N - Não uma viagem de loja e para a frente)
dropoff_longitude | Longitude onde o medidor foi desligado.
dropoff_latitude | Latitude onde o medidor foi desligado.
payment_type | Um código numérico que significa como o passageiro pagou pela viagem. (1 - Cartão de crédito, 2 - Dinheiro, 3 - Sem custo, 4 - Disputa, 5 - Desconhecido, 6 - Viagem anulada)
fare_amount | A tarifa de tempo e distância calculada pelo medidor.
extra | Extras e sobretaxas diversos. Atualmente, isso inclui apenas. os $0,50 e $1 hora do rush e taxas de noite.
mta_tax | 0,50 Imposto MTA que é automaticamente acionado com base na taxa medida em uso.
tip_amount | Valor da gorjeta – Este campo é preenchido automaticamente para gorjeta de cartão de crédito. As gorjetas em dinheiro não estão incluídas.
tolls_amount | Total de todos os pedágios pagos na viagem.
improvement_surcharge | 0,30 sobretaxa de melhoria avaliada viagens na queda da bandeira. a taxa de melhoria começou a ser cobrada em 2015.
total_amount | O valor total cobrado aos passageiros. Não inclui gorjetas em dinheiro.

## Athena

### Faturamento médio por hora

```sql
select
    split_part(split_part(tpep_pickup_datetime, ' ', 2), ':', 1) as hora,
    avg(total_amount) as media_da_corrida
from "fiap"."parquet"
group by
    split_part(split_part(tpep_pickup_datetime, ' ', 2), ':', 1)
order by
    2 desc,
    1 desc
```

### Faturamento por hora por dia

````sql
select
    split_part(split_part(tpep_pickup_datetime, '-', 3), ' ', 1) as dia,
    split_part(split_part(tpep_pickup_datetime, ' ', 2), ':', 1) as hora,
    avg(total_amount) as media_da_corrida
from "fiap"."parquet"
group by
    split_part(split_part(tpep_pickup_datetime, '-', 3), ' ', 1),
    split_part(split_part(tpep_pickup_datetime, ' ', 2), ':', 1)
order by
    3 desc,
    2 desc
````

### Faturamento por dia por vendedor
```sql
select
    vendor_id,
    split_part(split_part(tpep_pickup_datetime, '-', 3), ' ', 1) as dia,
    sum(total_amount)
from
    "fiap"."parquet"
group by
    vendor_id,
    split_part(split_part(tpep_pickup_datetime, '-', 3), ' ', 1)
order by
    3 desc;
```
