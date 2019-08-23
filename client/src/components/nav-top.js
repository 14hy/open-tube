import { html, render } from 'lit-html'
import i18next from 'i18next'

import store from '../libs/store.js'
import { logout } from '../libs/actions.js'
import { main } from '../main.js'
import { xhrFirebase } from '../libs/actions.js'

export class NavTop extends HTMLElement {
	constructor() {
		super()

		this._handlers = {}
	}

	connectedCallback() {
		render(this.render(), this)
		
		const handlers = this._handlers

		handlers.onClick = this._onClick.bind(this)
		
		this.addEventListener(`click`, handlers.onClick)
	}

	disconnectedCallback() {
		this.removeEventListener(`click`, this._handlers.onClick)
	}

	get btnLogout() {
		const info = store.getState().userInfo

		if (!info) {
			return html``
		}
		
		xhrFirebase(`/isAdmin/${info.uid}`, isAdmin => {
			const _isAdmin = JSON.parse(isAdmin)
			if (_isAdmin) {
				this.querySelector(`.user-name`).textContent = `관리자`
				return
			}
			this.querySelector(`.user-name`).textContent = info.displayName
		})
	
		return html`
		<span class="user-name"></span>
		<span class="login-btn-logout">Logout</span>
		`
	}

	get signIn() {
		return html`<span class="nav-sign-in">SIGN IN</span>`	
	}

	_onClick(event) {
		this.clickLogout(event)
		this.clickSignIn(event)
	}

	clickSignIn(event) {
		if (event.target.classList.contains(`nav-sign-in`)) {
			main.connectLoginNoLoad(`login`)
		}
	}

	clickLogout(event) {
		if (event.target.classList.contains(`login-btn-logout`)) {			
			logout()
		}
	}

	

	render() {
		const isLogin = store.getState().isLogin
		return html` 
        <h1 class="nav-title">${i18next.t(`APP_NAME`)}</h1>
        ${isLogin ? this.btnLogout : this.signIn}
        `
	}
}

customElements.define(`nav-top`, NavTop)
