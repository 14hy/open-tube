import { html, render } from 'lit-html'
import i18next from 'i18next'

import { xhrCorsServer, postXhr, messageShow } from '../libs/actions.js'
import store from '../libs/store.js'

export class ModalRequestReport extends HTMLElement {
	constructor() {
		super()
	}

	connectedCallback() {
		render(this.render(), this)		
	}
    
	show() {
		this.style.transform = `scale(1)`
	}

	hide() {
		this.style.transform = `scale(0)`
	}
    
	get clickX() {
		const root = this
		return {
			handleEvent() {
				root.hide()
			},
			capture: true,
		}
	}

	get requestList() {
		return html`
		<div class="analysis-box">
			<label class="label-analysis-list">${i18next.t(`MODAL_REQUEST_LABEL_ANALYSIS`)}</label>
			<ul>
				<li><input id="itemFace" type="checkbox" checked disabled/><label for="itemFace"></label>영상 인물 인식</li>
				<li><input id="itemComment" type="checkbox" checked disabled/><label for="itemComment"></label>댓글 감성 분석</li>
				<li><input id="itemKeyword" type="checkbox" checked disabled/><label for="itemKeyword"></label>키워드 분석</li>
			</ul>
		</div>
		`
	}

	get clickSend() {
		const root = this
		return {
			handleEvent() {				
				const url = root.querySelector(`#inputYoutubeURL`).value				
				
				const formData = new FormData()
				formData.append(`userId`, `1InVr0t4PdTWHcomCZlcuJ0ZZB03`)
				formData.append(`keyword`, root.querySelector(`#itemKeyword`).checked)
				formData.append(`sentiment`, root.querySelector(`#itemComment`).checked)
				formData.append(`slang`, root.querySelector(`#itemComment`).checked)
				formData.append(`url`, url)

				if (!root.regUrlType(url)) {
					messageShow(`URL 형식이 잘못되었습니다.`)
					
				}

				const vid = new URL(url).searchParams.get(`v`)
				
				postXhr(`/history/`, formData).then(res => {
					if (JSON.parse(res).status === `success`) {						
						root.hide()						
						try {
							root.getYoutubeData(vid).then(youtubeInfo => {
								root.setDb(youtubeInfo)
								document.querySelector(`#inputYoutubeURL`).value = ``
							})
						} catch(err) {
							messageShow(`레포트 요청 접수 실패`)
						}					
					}
				})
			},
			capture: true,
		}
	}

	regUrlType(data) {
		const regex = /^(((http(s?)):\/\/)?)([0-9a-zA-Z-]+\.)+[a-zA-Z]{2,6}(:[0-9]+)?(\/\S*)?/
	
		return regex.test(data)
	
	}

	
	// eslint-disable-next-line max-lines-per-function
	setDb(youtubeInfo) {
		const uid = store.getState().userInfo.uid
		const db = firebase.firestore()
		db.collection(`userId`).doc(uid).get().then(doc => {
			if (doc.exists) {
				const data = doc.data()
				const length = Number(Object.keys(data)[Object.keys(data).length - 1]) + 1
				const obj = {}
				const formData = new FormData()
				let isDuplicate = false
				
				obj[length] = {
					status: 1,
					time: firebase.firestore.Timestamp.fromDate(new Date()),
					title: youtubeInfo.title,
					vid: youtubeInfo.vid,
					viewCount: youtubeInfo.viewCount,
					writeDate: youtubeInfo.date,
					desc: youtubeInfo.desc,
					likeCount: youtubeInfo.likeCount,
				}

				Object.values(data).forEach(each => {
					if (youtubeInfo.vid === each.vid) {
						isDuplicate = true
					}
				})
				
				if (isDuplicate) {
					messageShow(`실패: 중복된 레포트 요청`)
					return
				}
				
				db.collection(`userId`).doc(uid).update(obj).catch(err => {
					console.error(`NO ACCESS DB ${err}`)
				})
				messageShow(`레포트 요청이 접수되었습니다.`)
				document.querySelector(`report-list`).render()
				
				formData.append(`uid`, uid)
				formData.append(`vid`, youtubeInfo.vid)
				postXhr(`/download/`, formData)
			} else {
				messageShow(`인증되지 않은 사용자 입니다.`)
				console.error(`No SEACH DB`)
			}
		}).catch(err => {
			console.error(`NO ACCESS DB ${err}`)
		})
	}

	async getYoutubeData(vid) {		
		const text = await xhrCorsServer(`https://www.youtube.com/watch?v=${vid}`)
		return {
			vid,
			title: text.match(/videoPrimaryInfoRenderer":{"title":{"runs":\[{"text":"(.*?)"}\]}/)[1],
			viewCount: text.match(/"viewCountText":{"simpleText":"조회수 (.*?)"}/)[1],
			date: text.match(/"dateText":{"simpleText":"게시일: (.*?)"}/)[1],
			desc: text.match(/"description":{"runs":\[{"text":"(.*?)"}/)[1],
			likeCount: text.match(/"accessibilityData":{"label":"좋아요 (.*?)"}/)[1],
		}
	}

	render() {
		return html`
        <div class="modal-report">
            <div class="modal-header">
                <span class="modal-title">${i18next.t(`MODAL_REQUEST_REPORT_TITLE`)}</span>
                <i class="fi-x size-72" @click=${this.clickX}></i>
			</div>
			
            <div class="modal-body">
				<div class="url-box">
					<label class="url-label" for="inputYoutubeURL">${i18next.t(`MODAL_REQUEST_LABEL_URL`)}</label>
					<input type="text" id="inputYoutubeURL" placeholder="https://www.youtube.com/watch?v=vid..."/>
				</div>
				${this.requestList}
			</div>

            <div class="modal-footer">
                <button class="submit-request" @click=${this.clickSend}>${i18next.t(`MODAL_REQUEST_REPORT_SUBMIT`)}</button>
            </div>
        </div>
        `
	}
}

customElements.define(`modal-request-report`, ModalRequestReport)
