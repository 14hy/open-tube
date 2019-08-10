import { html, render } from 'lit-html'
import i18next from 'i18next'

export class FilterList extends HTMLElement {
	constructor() {
		super()

		render(this.render(), this)
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
        `
	}
}

customElements.define(`filter-list`, FilterList)
