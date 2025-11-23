# TransFlow – Sistema de Corridas Assíncronas

Protótipo de backend para gerenciamento de corridas urbanas com:

- FastAPI (API HTTP)
- MongoDB (persistência das corridas)
- Redis (saldo de motoristas)
- RabbitMQ + FastStream (mensageria assíncrona)
- Docker Compose (orquestração)

## 1. Estrutura do projeto

```text
transflow/
├── src/
│   ├── main.py
│   ├── producer.py
│   ├── consumer.py
│   ├── database/
│   │   ├── mongo_client.py
│   │   └── redis_client.py
│   └── models/
│       └── corrida_model.py
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## 2. Requisitos

- Docker
- Docker Compose

## 3. Configuração

1. Copie o arquivo de exemplo de variáveis:

   ```bash
   cp .env.example .env
   ```

2. Se necessário, altere os valores de conexão para MongoDB, Redis e RabbitMQ.

## 4. Subindo o ambiente

Na raiz do projeto:

```bash
docker-compose up --build
```

Serviços principais:

- API FastAPI: http://localhost:8000/docs
- RabbitMQ Management: http://localhost:15672 (user: guest, pass: guest)
- MongoDB: localhost:27017
- Redis: localhost:6379

## 5. Endpoints

### POST /corridas

Cadastra uma nova corrida e dispara o processamento assíncrono.

Corpo de exemplo:

```json
{
  "passageiro": {"nome": "João", "telefone": "99999-1111"},
  "motorista": {"nome": "Carla", "nota": 4.8},
  "origem": "Centro",
  "destino": "Inoã",
  "valor_corrida": 35.50,
  "forma_pagamento": "DigitalCoin"
}
```

Resposta de exemplo:

```json
{
  "mensagem": "Corrida enviada para processamento.",
  "id_corrida": "uuid-gerado"
}
```

### GET /corridas

Lista todas as corridas registradas no MongoDB.

### GET /corridas/{forma_pagamento}

Lista corridas filtrando pela forma de pagamento.

### GET /saldo/{motorista}

Retorna o saldo atual do motorista no Redis.

Exemplo: `/saldo/Carla`

## 6. Fluxo assíncrono

1. O cliente chama `POST /corridas`.
2. A API publica um evento `corrida_finalizada` no RabbitMQ.
3. O serviço `consumer` (FastStream) consome a mensagem.
4. O consumer:
   - Atualiza o saldo do motorista no Redis de forma atômica.
   - Registra ou atualiza a corrida no MongoDB.

## 7. Testes rápidos

Após subir com Docker Compose:

- Acesse o Swagger em `http://localhost:8000/docs`.
- Crie uma corrida em `POST /corridas`.
- Verifique:
  - `GET /corridas`
  - `GET /corridas/DigitalCoin`
  - `GET /saldo/Carla` (ou o nome do motorista utilizado)

## 8. Captura de tela

<img width="1878" height="992" alt="image" src="https://github.com/user-attachments/assets/239ad4ac-0593-4ef6-9bfd-9a640241484c" />

