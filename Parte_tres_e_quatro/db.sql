CREATE TABLE IF NOT EXISTS contas (
    REG_ANS VARCHAR(20), 
    DATA DATE NOT NULL,
    CD_CONTA_CONTABIL VARCHAR(50) NOT NULL,
    DESCRICAO TEXT NOT NULL,
    VL_SALDO_INICIAL DECIMAL(15,2) NOT NULL,
    VL_SALDO_FINAL DECIMAL(15,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS registros_ans (
    Registro_ANS VARCHAR(20) PRIMARY KEY,
    CNPJ VARCHAR(20) NOT NULL,
    Razao_Social VARCHAR(255) NOT NULL,
    Nome_Fantasia VARCHAR(255),
    Modalidade VARCHAR(100),
    Logradouro VARCHAR(255),
    Numero VARCHAR(50),
    Complemento VARCHAR(100),
    Bairro VARCHAR(100),
    Cidade VARCHAR(100),
    UF CHAR(2),
    CEP VARCHAR(10),
    DDD VARCHAR(5),
    Telefone VARCHAR(255),
    Fax VARCHAR(20),
    Endereco_eletronico VARCHAR(255),
    Representante VARCHAR(255),
    Cargo_Representante VARCHAR(100),
    Regiao_de_Comercializacao VARCHAR(255),
    Data_Registro_ANS DATE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
