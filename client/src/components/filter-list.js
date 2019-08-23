import { html, render } from 'lit-html'
import i18next from 'i18next'

import { main } from '../main.js'
import store from '../libs/store.js'

export class FilterList extends HTMLElement {
	constructor() {
		super()
	}
    
	connectedCallback() {
		render(this.render(), this)
	}
    
	clickRequestReport() {
		return {
			handleEvent() {
				const modal = document.querySelector(`modal-request-report`)
				
				if(store.getState().isLogin) {
					modal.show()
					return
				}

				alert(`로그인이 필요합니다. 로그인 페이지로 이동`)
				main.connectLoginNoLoad(`login`)
			},
			capture: false,
		}
	}

	get clickWait() {
		const root = this
		return {
			handleEvent(event) { 
				const check = event.currentTarget.checked

				root.showOrHide(check, `대기 중`)
			},
			capture: false,
		}
	}

	get clickProcessing() {
		const root = this
		return {
			handleEvent(event) { 
				const check = event.currentTarget.checked

				root.showOrHide(check, `분석 중`)
			},
			capture: false,
		}
	}

	get clickComplete() {
		const root = this
		return {
			handleEvent(event) { 
				const check = event.currentTarget.checked

				root.showOrHide(check, `분석 완료`)
			},
			capture: false,
		}
	}

	showOrHide(check, text) {
		document.querySelectorAll(`report-list > ul > li`).forEach(li => {
			if (li.querySelector(`.report-status`).textContent === text) {
				if (check) {
					li.style.display = `list-item`
				} else {
					li.style.display = `none`
				}
			}
		})
	}

	render() {
		return html`
        <h2 class="category-title">Reports</h2>
        <div class="category-desc">
            ${i18next.t(`FILTER_DESC`)}
        </div>
        <h3 class="category-filter-1">
            Report Step
        </h3>
        <ul class="filter-ul">
            <li><input type="checkbox" id="li1" checked @click=${this.clickWait}/><label for="li1">대기 중</label></li>
			<li><input type="checkbox" id="li2" checked @click=${this.clickProcessing}/><label for="li2">분석 중</label></li>
			<li><input type="checkbox" id="li3" checked @click=${this.clickComplete}/><label for="li3">분석 완료</label></li>
        </ul>
        <button class="btn-request-report" @click=${this.clickRequestReport()}>${i18next.t(`BTN_REQUEST_REPORT`)}</button>
        `
	}
}

customElements.define(`filter-list`, FilterList)
