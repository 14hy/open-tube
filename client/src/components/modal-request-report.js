import { html, render } from 'lit-html'
import i18next from 'i18next'

import { postXhr, messageShow } from '../libs/actions.js'
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
				<li><input id="itemFace" type="checkbox" checked/><label for="itemFace"></label>영상 얼굴 인식</li>
				<li><input id="itemComment" type="checkbox" checked/><label for="itemComment"></label>댓글 감성 분석</li>
				<li><input id="itemKeyword" type="checkbox" checked/><label for="itemKeyword"></label>키워드 분석</li>
			</ul>
		</div>
		`
	}

	get clickSend() {
		const root = this
		return {
			handleEvent() {
				const uid = store.getState().userInfo.uid
				const url = root.querySelector(`#inputYoutubeURL`).value
				
				const formData = new FormData()
				formData.append(`userId`, uid)
				formData.append(`keyword`, root.querySelector(`#itemKeyword`).checked)
				formData.append(`sentiment`, root.querySelector(`#itemComment`).checked)
				formData.append(`slang`, root.querySelector(`#itemComment`).checked)
				formData.append(`url`, url)

				if (!root.regUrlType(url)) {
					messageShow(`URL 형식이 잘못되었습니다.`)
				}
				
				postXhr(`/history/`, formData).then(res => {
					if (JSON.parse(res).status === `success`) {
						messageShow(`레포트 요청이 접수되었습니다.`)
						root.hide()
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
