import { html, render } from 'lit-html'

export class AppFooter extends HTMLElement {
	constructor() {
		super()

		render(this.render(), this)
	}

	render() {
		return html`
        © 2019 Open-Tube, Inc.
        `
	}
}

customElements.define(`app-footer`, AppFooter)
