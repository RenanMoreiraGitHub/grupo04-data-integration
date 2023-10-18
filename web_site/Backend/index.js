const express = require('express');
const mysql = require('mysql');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

app.use(bodyParser.json());

const db = mysql.createConnection({
    host: 'localhost',
    user: 'seu_usuario_mysql',
    password: 'sua_senha_mysql',
    database: 'nome_do_banco_de_dados'
});

db.connect(err => {
    if (err) {
        console.error('Erro ao conectar ao banco de dados:', err);
        return;
    }
    console.log('Conexão ao banco de dados estabelecida');
});

app.listen(port, () => {
    console.log(`Servidor rodando na porta ${port}`);
});
