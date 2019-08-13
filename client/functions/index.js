const functions = require(`firebase-functions`)
const express = require(`express`)
const cors = require(`cors`)
const admin = require(`firebase-admin`)

admin.initializeApp(functions.config().firebase)

const app = express()
const db = admin.firestore()

const whiteList = [`https://open-tube.web.app`, `https://open-tube.kro.kr`, `localhost`]
app.use(cors({
	origin: (origin, callback) => {
		if (whiteList.includes(origin)) {
			callback(null, true)
		} else {
			callback(new Error(`Not allowed by CORS`))
		}
	},
}))

app.get(`/isAdmin/:uid`, (req, res) => {
	if (!req.xhr) {
		res.send(`ONLY REQUEST AJAX`)
	}
    
	res.send(req.params.uid === functions.config().admin.uid)
})

app.get(`/:uid/reportList`, (req, res) => {
	if (!req.xhr) {
		res.send(`ONLY REQUEST AJAX`)
	}

	db.doc(`userId/${req.params.uid}`).get()
		.then(q => {			
			res.send(q.data())
		})
		.catch(err => {
			console.error(`Error getting documents`, err)
			res.send(`Error getting documents: ${err}`)
		})
})

exports.server = functions.https.onRequest(app)
