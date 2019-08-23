import { storiesOf } from '@storybook/polymer'
// import { document } from 'global'
import '../main.js'
import '../../public/src/css/style.css'

storiesOf(`Page`, module)
	.add(`page-login`, () => `<page-login></page-login>`)
	.add(`page-reports`, () => `<page-reports></page-reports>`)

// storiesOf(`Demo`, module)
// 	.add(`heading`, () => `<h1>Hello World</h1>`)
// 	.add(`button`, () => {
// 		const button = document.createElement(`button`)
// 		button.type = `button`
// 		button.innerText = `Hello Button`
// 		button.addEventListener(`click`, e => console.log(e))
// 		return button
// 	})
