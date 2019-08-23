import { html, render } from 'lit-html'

export class ModalMessage extends HTMLElement {
	constructor() {
		super()
	}

	connectedCallback() {
		render(this.render(), this)
        
		window.setTimeout(() => {
			this.remove()
		}, 3000)
	}

	render() {
		return html`
        <div id="modalMessage">
            ${this.message}
        </div>
        `
	}
}

customElements.define(`modal-message`, ModalMessage)
