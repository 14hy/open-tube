import { html, render } from 'lit-html'
import i18next from 'i18next'

import { main } from '../main.js'
import { initLogin } from '../libs/actions.js'

export class FilterList extends HTMLElement {
	constructor() {
		super()
	}
    
	connectedCallback() {
		render(this.render(), this)
	}
    
	get clickRequestReport() {
		return {
			handleEvent() { 
				const modal = document.querySelector(`modal-request-report`)
				
				if (initLogin()) {
					modal.show()
					return
				}
				alert(`로그인이 필요합니다. 로그인 페이지로 이동`)
				main.connectLoginNoLoad(`login`)
				
			},
			capture: true,
		}
	}

	render() {
		return html`
        <h2 class="category-title">Reports</h2>
        <div class="category-desc">
            ${i18next.t(`FILTER_DESC`)}
        </div>
        <h3 class="category-filter-1">
            Filter List
        </h3>
        <ul class="filter-ul">
            <li><input type="checkbox" id="li1"/><label for="li1">감성 분석</label></li>
        </ul>
        <button class="btn-request-report" @click=${this.clickRequestReport}>${i18next.t(`BTN_REQUEST_REPORT`)}</button>
        `
	}
}

customElements.define(`filter-list`, FilterList)
