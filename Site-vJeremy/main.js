function generateCode(){
    return Math.floor(Math.random() * (1000 - 1 + 1)) + 1;
}

'INSERT INTO Usuario(code) where login = ? and senha = ?' [login, senha]

'SELECT code from Usuario where login = ? and senha = ?' [login, senha]


// --------------------------


// npm install nodemailer

const nodemailer = require('nodemailer');

async function notifyAdmin() { 
    const transporter = nodemailer.createTransport({
        host: 'smtp.office365.com',
        port: 567,
        secure: true, // use SSL
        auth: {
            user: 'cultura.soja@sptech.school',
            pass: '*******'   
        }
        })
    
    const info= await transporter.sendMail({ 
        from: "cultura.soja@sptech.school", 
        to: `${usuario}`, 
        subject: "Código de auntenticação recebido", 
        text: `Insira o código ${code} para validar o seu acesso na plataforma SoyBean`,
    })

    console.log("Message sent: %s", info.messageId)
}

async function main() { 
    await notifyAdmin()
}