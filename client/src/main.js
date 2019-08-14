import './libs/i18n.js'
import store from './libs/store.js'

import './pages/page-reports.js'
import './pages/page-login.js'

export const main = new class {
	constructor() {
		this.path = location.pathname
		this.isContinue = true
	}

	async init() {
		if (this.isIE()) {
			document.querySelector(`main`).innerHTML = `<div>THIS BROWSER NO SUPPORT</div>`
			return
		}

		firebase.initializeApp({
			apiKey: `AIzaSyBfd5CP6NWbLOUGMiZ5Z0Kh-n0ciVaAWsQ`,
			authDomain: `open-tube.web.app`,
			databaseURL: `https://open-tube-4c423.firebaseio.com`,
			projectId: `open-tube-4c423`,
			storageBucket: ``,
			messagingSenderId: `23035864360`,
			appId: `1:23035864360:web:66704a6d558311a0`,
		})

		await this.initLoginState()
		
		this.connectRoute()
	}

	// Init functions
	connectRoute(pathName = this.path.split(`/`)[1] || `login`) {
		this._onLoad(() => {
			this.routeLogin(pathName)
		})

		if (document.readyState === `complete`) {
			this.routeLogin(pathName)
		}
	}

	connectLoginNoLoad(pathName = this.path.split(`/`)[1] || `login`) {
		this.routeLogin(pathName)
	}

	routeLogin(pathName) {
		const isLogin = store.getState().isLogin
		const isRoute = () => Object.keys(store.getState().router).includes(pathName)
		const canMove = () => isLogin || isLogin === store.getState().router[pathName][`requireLogin`]
		const moveBasedLogin = (loginUrl, noLoginUrl) => {
			isLogin ? this.renderPage(`page-${loginUrl}`, `/${loginUrl}`) : this.renderPage(`page-${noLoginUrl}`, `/${noLoginUrl}`)
		}
		
		if (!isRoute()) {
			moveBasedLogin(`reports`, `login`)
			return
		}

		if (canMove()) {
			this.renderPage(`page-${pathName}`)			
			return
		}
		moveBasedLogin(`reports`, `login`)
	}

	// Functions

	_onLoad(callback) {
		window.addEventListener(`DOMContentLoaded`, () => {
			callback()
		})
	}

	isIE() {		
		return navigator.userAgent.includes(`Trident`) || navigator.userAgent.includes(`MSIE`)
	}

	loadingDOM() {
		const root = document.querySelector(`main`)
		const loading = document.createElement(`div`)
				
		this.emptyDOM()
		loading.classList.add(`loading`)
		for (let i=0; i < 5; i++) {
			loading.appendChild(document.createElement(`span`))
		}
		root.appendChild(loading)
	}

	renderPage(pageName, path) {		
		this.emptyDOM()
		const pageElement = document.createElement(pageName)
		document.querySelector(`main`).appendChild(pageElement)
		history.pushState({}, pageName, path)
	}	

	emptyDOM() {
		document.querySelector(`main`).innerHTML = ``	
	}

	initLoginState() {
		return new Promise((resolve, reject) => {
			const state = store.getState()
			firebase.auth().onAuthStateChanged(user => {
				if (user) {
					const displayName = user.displayName
					const email = user.email
					const emailVerified = user.emailVerified
					const photoURL = user.photoURL
					const uid = user.uid
					const phoneNumber = user.phoneNumber
					const providerData = user.providerData			
		
					user.getIdToken().then(accessToken => {
						state.isLogin = true
						state.userInfo = {
							displayName,
							email,
							emailVerified,
							phoneNumber,
							photoURL,
							uid,
							accessToken,
							providerData,
						}
						store.setState(state)
						resolve()
					})
				} else {
					state.isLogin = false
					state.userInfo = {}
					store.setState(state)
					resolve()
				}
			}, error => {
				reject(error)
			})
		})	
	}
}()

main.init()
