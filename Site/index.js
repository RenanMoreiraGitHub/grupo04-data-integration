const mysql = require("mysql2");
const express = require('express');
const session = require('express-session');
const path = require('path');

const app = express();
const PORT = 3000;

const connection = mysql.createConnection({
    host: 'aws-python-project-dev-mydbinstance-6ffzmbct02f9.clstgtmhjsoh.us-east-1.rds.amazonaws.com',
    user: 'soybean',
    password: 'urubu100',
    database: 'soybean'
});

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
            req.session.loggedin = true;
            req.session.username = username;
            res.redirect('/home');
        } else {
            res.send('Incorrect Username and/or Password!');
        }
    } catch (error) {
        console.error(error);
        res.status(500).send('Server Error');
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

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
