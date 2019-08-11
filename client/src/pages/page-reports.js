import { html, render } from 'lit-html'

import '../components/nav-top.js'
import '../components/filter-list.js'
import '../components/report-list.js'
import '../components/app-footer.js'
import '../components/modal-request-report.js'

export class PageReports extends HTMLElement {
	constructor() {
		super()				
	}
	
	connectedCallback() {
		render(this.render(), this)		
	}

	render() {
		return html`
		<link rel="stylesheet" type="text/css" href="/src/css/style.css">
		<div id="pageReports">
			<nav-top></nav-top>

			<filter-list></filter-list>
			<report-list></report-list>
			
			<app-footer></footer>
		</div>
		<modal-request-report></modal-request-report>
        `
	}
}

customElements.define(`page-reports`, PageReports)
