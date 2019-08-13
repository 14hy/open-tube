import './libs/i18n.js'
import store from './libs/store.js'

import './pages/page-reports.js'
import './pages/page-login.js'

export const main = new class {
	constructor() {
		this.path = location.pathname
		this.isContinue = true
	}

	init() {
		if (this.isIE()) {
			document.querySelector(`main`).innerHTML = `<div>THIS BROWSER NO SUPPORT</div>`
			return
		}

		this.loadingDOM()
		this.connectRoute()
	}

	// Init functions
	connectRoute(pathName = this.path.split(`/`)[1] || `login`) {
		this._onLoad(() => {
			if (store.getState().isLogin) {
				this.routeLogin(pathName)
			}			
		})
	}

	connectLoginNoLoad(pathName = this.path.split(`/`)[1] || `login`) {
		this.routeLogin(pathName)
	}

	routeLogin(pathName) {
		const isRoute = () => Object.keys(store.getState().router).includes(pathName)
		
		if (isRoute()) {
			this.renderPage(`page-${pathName}`, `/${pathName}`)
		}
	}

	// Functions

	_onLoad(callback) {
		window.addEventListener(`load`, () => {			
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
}()

main.init()
