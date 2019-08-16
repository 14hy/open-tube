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
					<span class="modal-title">Reports</span>
				</div>

				<iframe width="1195" height="600" .src=${this.url} frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
				
				<div class="modal-footer">© 2019 Open-Tube, Inc.</div>
			</div>            
        </div>
        `
	}
}

customElements.define(`modal-report`, ModalReport)
