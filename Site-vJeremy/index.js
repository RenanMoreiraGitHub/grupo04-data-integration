const mysql = require("mysql2");
const express = require('express');
const session = require('express-session');
const path = require('path');
const nodemailer = require('nodemailer');
const app = express();
const PORT = 3000;
const storage = require('node-sessionstorage')

const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '*********',
    database: 'testeBack'
});

var code = generateCode();

app.use(session({
    secret: 'secret',
    resave: true,
    saveUninitialized: true
}));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'static')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'login.html'));
});

app.post('/auth', async (req, res) => {
    const { username, password } = req.body;

    try {
        const [results] = await connection.promise().query('SELECT * FROM accounts WHERE username = ? AND password = ?', [username, password]);

        if (results.length > 0) {
            const resultUpdate = await connection.promise().query('UPDATE accounts SET code = ?  where username = ? and password = ?', [code, username, password])
            sendEmail();
            req.session.loggedin = true;
            req.session.username = username;
            req.session.password = password;
            res.redirect('/authentication');
        } else {
            res.send('Incorrect Username and/or Password!');
        }
    } catch (error) {
        console.error(error);
        res.status(500).send('Server Error');
    }
});

app.post('/update', async (req, res) => {
    try {
        const [results] = await connection.promise().query('SELECT code FROM accounts WHERE username = ? AND password = ?', [email, senha]);
        
        if (results.length > 0) {
            res.redirect('/home');
        } else {
            res.send('Incorrect Username and/or Password!');
        }
    } catch (error) {
        console.error(error);
        res.status(500).send('Server Error');
    }
});

async function sendEmail() { 
    const transporter = nodemailer.createTransport({
        host: 'smtp.office365.com',
        port: 587,
        secure: false, // use SSL
        auth: {
            user: 'renan.lima@bandtec.com.br',
            pass: '**************'   
        }
        })
    
    const info= await transporter.sendMail({ 
        from: "renan.lima@bandtec.com.br", 
        to: `teste@gmail.com`, 
        subject: "Código de auntenticação recebido", 
        text: `Insira o código ${code} para validar o seu acesso na plataforma SoyBean`,
    })

    console.log("Message sent: %s", info.messageId)
}

app.get('/authentication', (req, res) => {
    if (req.session.loggedin) {
        res.sendFile(path.join(__dirname, 'authentication.html'));
    } else {
        res.send('Please login to view this page!');
    }
});

app.get('/home', (req, res) => {
    if (req.session.loggedin) {
        res.send('Welcome back, ' + req.session.username + '!');
    } else {
        res.send('Please login to view this page!');
    }
});

app.get('/register', (req, res) => {
    res.sendFile(path.join(__dirname, 'register.html'));
});

app.post('/register', async (req, res) => {
    const { username, password, email } = req.body;

    try {
        if (username && password) {
            await connection.promise().query('INSERT INTO accounts (username, password, email) VALUES (?, ?, ?)', [username, password, email]);
            res.redirect('/login');
        } else {
            res.send('Please enter Username and Password!');
        }
    } catch (error) {
        console.error(error);
        res.status(500).send('Server Error');
    }
});

function generateCode(){
    return Math.floor(Math.random() * (1000 - 1 + 1)) + 1;
}



app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
