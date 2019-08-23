import { html, render } from 'lit-html'

import { main } from '../main.js'
import store from '../libs/store.js'

export class ReportList extends HTMLElement {
	constructor() {
		super()		
	}
    
	connectedCallback() {
		render(this.render(), this)		
	}

	clickReport() {
		return {
			handleEvent(event) {
				const modal = document.querySelector(`modal-report`)
				const target = event.currentTarget
				const vid = new URL(target.querySelector(`.report-desc a`).textContent).searchParams.get(`v`)
				if(store.getState().isLogin) {
					// autoplay=0&rel=0&controls=0&showinfo=0&cc_load_policy=0&iv_load_policy=3&
					modal.show(`https://www.youtube.com/embed/${vid}?autoplay=0&rel=0&showinfo=0&cc_load_policy=0&iv_load_policy=3&modestbranding=1`, vid)
					return
				}

				alert(`로그인이 필요합니다. 로그인 페이지로 이동`)
				main.connectLoginNoLoad(`login`)				
			},
			capture: false,
		}
	}

	clickLink(vid) {
		return {
			handleEvent(event) { 
				event.stopImmediatePropagation()
				event.preventDefault()
				window.open(`https://www.youtube.com/watch?v=${vid}`, `_blank`)
			},
			capture: false,
		}
	}

	get li() {
		const info = store.getState().userInfo
		const db = firebase.firestore()

		if (!info) {
			return html``
		}		

		db.collection(`userId`).doc(`1InVr0t4PdTWHcomCZlcuJ0ZZB03`).get().then(doc => {
			if (doc.exists) {
				this.renderLi(doc.data())
			} else {
				console.error(`No SEACH DB`)
			}
		}).catch(err => {
			console.error(`NO ACCESS DB ${err}`)
		})

		return html``
	}

	renderLi(db) {
		const ul = this.querySelector(`.ul-reports`)
		const li = item => {			
			const date = new Date(item.time.seconds * 1000).toLocaleDateString()
			const statusName = [`요청 전`, `대기 중`, `분석 중`, `분석 완료`]
			const status = statusName[item.status]
			return html`
			<li class="li-report" @click=${this.clickReport()}>						
				<div class="report-wrap"><span class="report-status">${status}</span><span class="report-title">${item.title}</span></div>
				<div class="report-desc"><a @click=${this.clickLink(item.vid)}>https://www.youtube.com/watch?v=${item.vid}</a></div>
				<div class="report-time">${date}</div>						
				<img src="https://i1.ytimg.com/vi/${item.vid}/hqdefault.jpg" width="132" height="80"/>
			</li>
			`
		}

		ul.innerHTML = ``
		render(html`
			${Object.values(db).map(i => li(i))}
		`, ul)
	}

	render() {
		return html`
		<ul class="ul-reports">
			${this.li}			
		</ul>
		`
	}
}

customElements.define(`report-list`, ReportList)
