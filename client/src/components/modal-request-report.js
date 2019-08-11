import { html, render } from 'lit-html'
import i18next from 'i18next'

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
				<li><input id="item1" type="checkbox" checked/><label for="item1"></label>댓글 감성 분석</li>
				<li><input id="item2" type="checkbox" checked/><label for="item2"></label>영상 객체 분석</li>
				<li><input id="item3" type="checkbox" checked/><label for="item3"></label>Item 3</li>
				<li><input id="item4" type="checkbox" checked/><label for="item4"></label>Item 4</li>
			</ul>
		</div>
		`
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
                <button class="submit-request">${i18next.t(`MODAL_REQUEST_REPORT_SUBMIT`)}</button>
            </div>
        </div>
        `
	}
}

customElements.define(`modal-request-report`, ModalRequestReport)
