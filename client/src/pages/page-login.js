import { html, render } from 'lit-html'
import store from '../libs/store.js'
import { logout } from '../libs/actions.js'
import { main } from '../main.js'

export class PageLogin extends HTMLElement {
	constructor() {
		super()		

		this._handlers = {}		
	}

	connectedCallback() {
		render(this.render(), this)

		const handlers = this._handlers

		handlers.onClick = this._onClick.bind(this)
		
		this.addEventListener(`click`, handlers.onClick)				

		this.createLogin()
	}

	disconnectedCallback() {
		this.removeEventListener(`click`, this._handlers.onClick)
	}

	_onClick(event) {
		this.clickLogout(event)
		this.clickLookAround(event)
	}

	clickLogout(event) {
		if (event.target.classList.contains(`login-btn-logout`)) {
			logout()
		}			
	}

	clickLookAround() {
		if (event.target.classList.contains(`login-btn-sightsee`)) {			
			main.connectLoginNoLoad(`reports`)
		}
	}

	createLogin() {		
		const uiConfig = {
			signInSuccessUrl: `/reports`,
			signInOptions: [
				{
					provider: firebase.auth.GoogleAuthProvider.PROVIDER_ID,
					customParameters: {
						prompt: `select_account`,
					},
				},
				firebase.auth.FacebookAuthProvider.PROVIDER_ID,
				firebase.auth.GithubAuthProvider.PROVIDER_ID,
			],
			tosUrl: `/`,
			signInFlow: `popup`,
			privacyPolicyUrl: () => {
				window.location.assign(`/`)
			},
		}	
		const ui = firebaseui.auth.AuthUI.getInstance() || new firebaseui.auth.AuthUI(firebase.auth())
		const loginBox = this.querySelector(`.login-box`)
		if (!store.getState().isLogin) {
			ui.start(loginBox, uiConfig)
			return
		}
		loginBox.insertAdjacentHTML(`beforeend`, `<span class="login-btn-logout">Logout</span>`)
	}

	render() {
		return html`
		<div id="pageLogin">
			<div class="div-info">
				<span>그림으로 된 설명</span>
			</div>
			<div class="div-login">
				<span class="login-box">
					<button class="login-btn-sightsee">LOOK AROUND Page</button>
				</span>
			</div>
		</div>
		`
	}
}

customElements.define(`page-login`, PageLogin)
