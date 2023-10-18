const mysql = require("mysql2");
const express = require('express');
const session = require('express-session');
const path = require('path');
const nodemailer = require('nodemailer');
const app = express();
const PORT = 3000;
const LocalStorage = require('node-localstorage').LocalStorage;
const localStorage = new LocalStorage('./scratch');

const connection = mysql.createConnection({
    host: 'aws-soybean-prod-mydbinstance-c51s1md1dk4d.cerbmnica18k.us-east-1.rds.amazonaws.com',
    user: 'soybean',
    password: 'urubu100',
    database: 'soybean'
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
    const { username, password, Empresa } = req.body;
    var access_type
    try {
        console.log(req.body)

        if(Empresa == 'true'){
            const [results] = await connection.promise().query('SELECT * FROM empresa WHERE email = ? AND password = ?', [username, password]);
            if(results.length > 0) {
                req.session.loggedin = true;
                req.session.username = username;
                req.session.password = password;
                return res.redirect('/empresa');
            } else {
                return res.send('Incorrect Username and/or Password!');
            }
        }
        
        const [results] = await connection.promise().query('SELECT * FROM usuario WHERE login = ? AND password = ?', [username, password]);
        if (results.length > 0) {
            const resultUpdate = await connection.promise().query('UPDATE usuario SET code = ?  where login = ? and password = ?', [code, username, password])
            req.session.loggedin = true;
            req.session.username = username;
            req.session.password = password;
            access_type = results[0].access_type;
            localStorage.setItem('email', username);
            localStorage.setItem('senha', password);
            localStorage.setItem('access_type', access_type)
            sendEmail();
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
        const { codeAuth } = req.body;
        console.log(req.body.codeAuth);
        var codigoVer = req.body.codeAuth;
        const email = localStorage.getItem('email');
        const senha = localStorage.getItem('senha');
        var access_type = localStorage.getItem('access_type');
        const [results] = await connection.promise().query('SELECT code FROM usuario WHERE login = ? AND password = ? and code = ?', [email, senha, parseInt(codigoVer)]);
        if (results.length > 0) {
            console.log(results)
            if (codigoVer == parseInt(results[0].code)) {
                console.log(req.session.codeAuth == parseInt(results[0].code))
                if (access_type == 1) {
                    return res.redirect('http://ec2-100-27-12-54.compute-1.amazonaws.com/');
                } else if (access_type == 2) {
                    return res.redirect('http://ec2-100-27-12-54.compute-1.amazonaws.com/');
                } else {
                    return res.redirect('/');
                }
            }
        } else {
            return res.redirect('/authentication');
        }
    } catch (error) {
        console.error(error);
        res.status(500).send('Server Error');
    }
});

async function sendEmail() { 
    const transporter = nodemailer.createTransport({
        host: 'smtp-mail.outlook.com',
        port: 587,
        secure: false, // use SSL
        auth: {
            user: 'contato.inview@outlook.com',
            pass: 'inview@2021'   
        }
        })
    
    const info= await transporter.sendMail({ 
        from: "contato.inview@outlook.com", 
        to: `${localStorage.getItem('email')}`, 
        subject: "Código de autenticação recebido", 
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

app.get('/empresa', (req, res) => {
    if (req.session.loggedin) {
        res.sendFile(path.join(__dirname, 'dashProprietario.html'));
    } else {
        res.send('Please login to view this page!');
    }
});

app.get('/usuario_financeiro', (req, res) => {
    if (req.session.loggedin) {
        res.sendFile(path.join(__dirname, 'dashFinanceiro.html'));
    } else {
        res.send('Please login to view this page!');
    }
});

app.get('/usuario_administrativo', (req, res) => {
    if (req.session.loggedin) {
        res.sendFile(path.join(__dirname, 'dashAdministrador.html'));
    } else {
        res.send('Please login to view this page!');
    }
});

app.get('/register_proprietario', (req, res) => {
    if (req.session.loggedin) {
        res.sendFile(path.join(__dirname, 'register_Proprietario.html'));
    } else {
        res.send('Please login to view this page!');
    }
});

app.get('/adm', (req, res) => {
    res.sendFile(path.join(__dirname, 'dashSoyBean.html'));
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