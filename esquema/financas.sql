CREATE TABLE IF NOT EXISTS usuario 
(
    id_usuario SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(256) NOT NULL UNIQUE,
    telefone VARCHAR(15) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    foto BYTEA,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categoria
(
    id_categoria SERIAL PRIMARY KEY,
    descricao VARCHAR(500) NOT NULL,
    natureza VARCHAR(10) CHECK (natureza IN ('receita', 'despesa')),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS receita
(
    id_receita SERIAL PRIMARY KEY,
    descricao VARCHAR(500) NOT NULL,
    valor NUMERIC(10, 2) NOT NULL,
    recebida BOOLEAN NOT NULL,
    data_recebimento DATE,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER REFERENCES usuario(id_usuario) ON DELETE CASCADE,
    id_categoria INTEGER REFERENCES categoria(id_categoria) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS despesa
(
    id_despesa SERIAL PRIMARY KEY,
    descricao VARCHAR(500) NOT NULL,
    valor NUMERIC(10, 2) NOT NULL,
    paga BOOLEAN NOT NULL,
    data_pagamento DATE,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER REFERENCES usuario(id_usuario) ON DELETE CASCADE,
    id_categoria INTEGER REFERENCES categoria(id_categoria) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cliente
(
    id_cliente SERIAL PRIMARY KEY,
    nome_cliente VARCHAR(100) NOT NULL,
    cep VARCHAR(500),
    rua VARCHAR(500),
    cidade VARCHAR(500),
    bairro VARCHAR(500),
    uf VARCHAR(2),
    contato VARCHAR(250) NOT NULL,
    descricao VARCHAR(5000) NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS projetos
(
    id_projeto SERIAL PRIMARY KEY,
    nome_projeto VARCHAR (100) NOT NULL,
    observacao VARCHAR(5000) NOT NULL,
    valor_cobrado NUMERIC(10, 2) NOT NULL,
    valor_gasto NUMERIC(10, 2),
    data_inicio DATE NOT NULL,
    data_fim DATE,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_cliente INTEGER REFERENCES cliente(id_cliente) ON DELETE CASCADE,
    id_usuario INTEGER REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS daytrade
(
    id_daytrade SERIAL PRIMARY KEY,
    contratos INTEGER NOT NULL,
    caixa_atual NUMERIC(10, 2) NOT NULL,
    gastos NUMERIC(10, 2) NOT NULL,
    lucro_liquido NUMERIC(10, 2) NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS obs_daytrade
(
    id_obs SERIAL PRIMARY KEY,
    detalhe VARCHAR(5000) NOT NULL,
    status VARCHAR(10) CHECK (status IN ('gain', 'loss')),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ativos
(
    id_ativo SERIAL PRIMARY KEY,
    descricao VARCHAR(500) NOT NULL,
    valor_investido NUMERIC(10, 2) NOT NULL,
    data_investimento DATE,
    valor_retorno NUMERIC(10, 2),
    data_retorno DATE,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS metas
(
    id_meta SERIAL PRIMARY KEY,
    descricao VARCHAR(5000) NOT NULL,
    status BOOLEAN,
    observacao VARCHAR(5000),
    data_conclusao DATE,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS notas
(
    id_nota SERIAL PRIMARY KEY,
    nota BYTEA NOT NULL,
    descricao VARCHAR(700) NOT NULL,
    tipo VARCHAR(255) NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER REFERENCES usuario(id_usuario) ON DELETE CASCADE
);