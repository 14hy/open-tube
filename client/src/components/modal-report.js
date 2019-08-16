import { html, render } from 'lit-html'

export class ModalReport extends HTMLElement {
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

	render() {
		return html`
        <div class="modal-report"> 
			<i class="fi-x size-72" @click=${this.clickX}></i>          			
            <div class="modal-body">				
				<div class="modal-header">
					<span class="modal-title">Reports</span>					
				</div>
				
				<div class="modal-footer">© 2019 Open-Tube, Inc.</div>
			</div>            
        </div>
        `
	}
}

customElements.define(`modal-report`, ModalReport)
