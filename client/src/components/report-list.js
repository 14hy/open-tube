import { html, render } from 'lit-html'

export class ReportList extends HTMLElement {
	constructor() {
		super()		
	}
    
	connectedCallback() {
		render(this.render(), this)		
	}

	render() {
		return html`
        <ul class="ul-reports">
            ${li}
        </ul>
        `
	}
}

const li = html`
<li class="li-report">
    <div class="report-title">유튜브 영상 제목</div>
    <div class="report-desc">유튜브 영상 URL</div>
</li>
`

customElements.define(`report-list`, ReportList)
