import store from './store.js'
import { main } from '../main.js'

function actionCreator(action) {
	return function() {
		let state = store.getState()
		state = action(state, ...arguments)
		store.setState(state)
	}
}

export const loadXhr = actionCreator((state, url, callback) => {
	const xhr = new XMLHttpRequest()

	if(!xhr) {
		throw new Error(`xhr 호출 불가`)
	}

	xhr.open(`GET`, url)
	xhr.setRequestHeader(`x-requested-with`, `XMLHttpRequest`)
	xhr.addEventListener(`readystatechange`, () => {
		if (xhr.readyState === xhr.DONE) {				
			if (xhr.status === 200 || xhr.status === 201) {
				callback(xhr.responseText)
			}
		}
	})
	xhr.send()
	return state
})

export const xhrFirebase = actionCreator((state, path, callback) => {
	const xhr = new XMLHttpRequest()

	if(!xhr) {
		throw new Error(`xhr 호출 불가`)
	}

	xhr.open(`GET`, `https://us-central1-open-tube-4c423.cloudfunctions.net/server${path}`)
	xhr.setRequestHeader(`x-requested-with`, `XMLHttpRequest`)
	xhr.addEventListener(`readystatechange`, () => {
		if (xhr.readyState === xhr.DONE) {				
			if (xhr.status === 200 || xhr.status === 201) {
				callback(xhr.responseText)
			}
		}
	})
	xhr.send()
	return state
})

export const logout = actionCreator(state => {
	firebase.auth().signOut().then(() => {
		state.isLogin = false
		store.setState(state)
		alert(`로그인이 필요합니다. 로그인 페이지로 이동`)
		main.renderPage(`page-login`, `/`)
	}).catch(error => {
		console.error(error)
	})

	return state
})
