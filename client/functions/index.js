const functions = require(`firebase-functions`)
const express = require(`express`)
const cors = require(`cors`)
const admin = require(`firebase-admin`)

admin.initializeApp(functions.config().firebase)

const app = express()

const whiteList = [`https://open-tube.web.app`, `localhost`]
app.use(cors({
	origin: (origin, callback) => {
		if (whiteList.indexOf(origin) === -1) {
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

exports.server = functions.https.onRequest(app)
