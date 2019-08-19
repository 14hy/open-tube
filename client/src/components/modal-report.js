import { html, render } from 'lit-html'

export class ModalReport extends HTMLElement {
	constructor() {
		super()

		this.url = ``
	}

	connectedCallback() {
		render(this.render(), this)
	}
    
	show(url) {
		this.url = url
		this.style.transform = `scale(1)`
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

	render() {
		return html`
        <div class="modal-report"> 
			<i class="fi-x size-72" @click=${this.clickX}></i>
            <div class="modal-body">				
				<div class="modal-header">					
					<h1 class="modal-title"><i class="fi-results size-72"></i> Reports</h1>
				</div>

				<div class="video-box">
					<h2 class="video-title"><i class="fi-play-video size-72"></i> Play Video</h2>
					<iframe width="300" height="250" .src=${this.url} frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
				</div>				
				
				<div class="modal-footer">© 2019 Open-Tube, Inc.</div>
			</div>            
        </div>
        `
	}
}

customElements.define(`modal-report`, ModalReport)
