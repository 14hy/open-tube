import { html, render } from 'lit-html'
import i18next from 'i18next'

import store from '../libs/store.js'
import { logout } from '../libs/actions.js'
import { main } from '../main.js'

export class NavTop extends HTMLElement {
	constructor() {
		super()

		this._handlers = {}

		render(this.render(), this)
	}

	connectedCallback() {
		const handlers = this._handlers

		handlers.onClick = this._onClick.bind(this)
		
		this.addEventListener(`click`, handlers.onClick)
	}

	disconnectedCallback() {
		this.removeEventListener(`click`, this._handlers.onClick)
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
        ${isLogin ? btnLogout : signIn}
        `
	}
}

const btnLogout = html`<span class="login-btn-logout">Logout</span>`
const signIn = html`<span class="nav-sign-in">SIGN IN</span>`

customElements.define(`nav-top`, NavTop)
