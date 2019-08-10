import { html, render } from 'lit-html'

export class ReportList extends HTMLElement {
	constructor() {
		super()		

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
    <div class="report-title">유튜브 레포트 1</div>
    <div class="report-desc">레포트 설명레포트 설명</div>
</li>
`

customElements.define(`report-list`, ReportList)
