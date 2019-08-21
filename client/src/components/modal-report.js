import { html, render } from 'lit-html'
import i18next from 'i18next'
import randomcolor from 'randomcolor'

import { xhrCorsServer, postXhr } from '../libs/actions.js'
import store from '../libs/store.js'

export class ModalReport extends HTMLElement {
	constructor() {
		super()

		this.url = ``
		this.vid = ``
		this.title = ``
		this.desc = ``
		this.date = ``
		this.viewCount = ``
		this.likeCount = ``
	}

	connectedCallback() {
		render(this.render(), this)
	}
    
	show(url, vid) {
		this.url = url
		this.style.transform = `scale(1)`
		this.getYoutubeData(vid)
		render(this.render(), this)
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

	async getYoutubeData(vid) {		
		const text = await xhrCorsServer(`https://www.youtube.com/watch?v=${vid}`)

		this.vid = vid
		this.title = text.match(/videoPrimaryInfoRenderer":{"title":{"runs":\[{"text":"(.*?)"}\]}/)[1]
		this.viewCount = text.match(/"viewCountText":{"simpleText":"조회수 (.*?)"}/)[1]
		this.date = text.match(/"dateText":{"simpleText":"게시일: (.*?)"}/)[1]
		this.desc = text.match(/"description":{"runs":\[{"text":"(.*?)"}/)[1]
		this.likeCount = text.match(/"accessibilityData":{"label":"좋아요 (.*?)"}/)[1]
		this.getFaceData()
		render(this.render(), this)			
	}

	get videoBox() {
		return html `
		<span class="video-box">
			<h2 class="video-title"><i class="fi-play-video size-72"></i> Info Video</h2>
			<iframe width="300" height="250" .src=${this.url} frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
			<h2 class="video-desc">Information</h2>
			<div class="video-desc">
				<span class="desc-title">Title:</span>
				<span class="desc-content title">${this.title}</span>
			</div>
			<div class="video-desc">
				<span class="desc-title">Date:</span>
				<span class="desc-content">${this.date}</span>
			</div>
			<div class="video-desc">
				<span class="desc-title">Describe:</span>
				<span class="desc-content desc">${this.desc}</span>
			</div>
			<div class="video-desc">
				<span class="desc-title">View Count:</span>
				<span class="desc-content">${this.viewCount}</span>
			</div>
			<div class="video-desc">
				<span class="desc-title">Like Count:</span>
				<span class="desc-content">${this.likeCount}</span>
			</div>
		</span>
		`
	}

	async getFaceData() {
		const uid = store.getState().userInfo.uid
		const formData = new FormData()
		formData.append(`uid`, uid)
		formData.append(`vid`, this.vid)

		const res = await postXhr(`http://101.101.167.71:32666/download/`, formData)

		const status = JSON.parse(res)[`status`]				

		// data.forEach(img => {
		// 	img.forEach(time => {				
		// 		console.log(Object.entries(time)[0])				
		// 	})
		// })

		if (status === `wait`) {
			render(html `${i18next.t(`MODAL_REPORT_FACE_STATUS_WAIT`)}`, this.querySelector(`.face-content`))	
		} else if (status === `processing`)	 {
			render(html `${i18next.t(`MODAL_REPORT_FACE_STATUS_PROCESSING`)}`, this.querySelector(`.face-content`))	
		} else if (status === `complete`) {
			const data = Object.values(JSON.parse(JSON.parse(res)[`time_line`]))
			const imgCount = data.length

			render(html `
				${imgCount}개의 이미지가 검색됨
			`, this.querySelector(`.face-img-count`))
			
			render(html `
				${data.map((img, index) => html`<img class="face-img" style="border: 5px solid ${randomcolor({luminosity: `dark`})}" src="https://open-tube.kro.kr/img-face/${uid}/${this.vid}/${index}.jpg"/>`)}
			`, this.querySelector(`.face-content`))	
		}
	}

	get faceAnalysisBox() {		
		return html `
		<span class="face-analysis-box">
			<h2 class="title"><i class="fi-social-myspace size-72"></i> Face Analysis</h2>
			<h3 class="title"><i class="fi-photo size-72"></i> All People <span class="face-img-count"></span></h3>
			<div class="face-content"></div>
		</span>
		`
	}

	render() {
		return html`
        <div class="modal-report"> 
			<i class="fi-x size-72" @click=${this.clickX}></i>
			<div class="modal-header">					
				<h1 class="modal-title"><i class="fi-results size-72"></i> Reports</h1>
			</div>
            <div class="modal-body">								

				${this.videoBox}

				${this.faceAnalysisBox}				

			</div>
			<div class="modal-footer">© 2019 Open-Tube, Inc.</div>
        </div>
        `
	}
}

customElements.define(`modal-report`, ModalReport)
