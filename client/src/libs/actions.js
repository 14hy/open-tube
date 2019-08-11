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
		throw new Error(`XHR 호출 불가`)
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
		throw new Error(`XHR 호출 불가`)
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

export const initLogin = actionCreator((state, callback) => {
	firebase.auth().onAuthStateChanged(user => {
		if (user) {
			user.getIdToken().then(() => {
				state.isLogin = true
				store.setState(state)
				callback(true)
			})
		} else {
			state.isLogin = false
			store.setState(state)
			callback(false)
		}
	}, error => {
		console.error(error)
	})
	return state
})

export const getUserInfo = actionCreator((state, callback) => {
	firebase.auth().onAuthStateChanged(user => {
		if (user) {
			const displayName = user.displayName
			const email = user.email
			const emailVerified = user.emailVerified
			const photoURL = user.photoURL
			const uid = user.uid
			const phoneNumber = user.phoneNumber
			const providerData = user.providerData

			user.getIdToken().then(accessToken => {
				callback({
					displayName,
					email,
					emailVerified,
					phoneNumber,
					photoURL,
					uid,
					accessToken,
					providerData,
				})
			})
		} else {
			callback(null)
		}
	}, error => {
		console.error(error)
	})
	return state
})

export const logout = actionCreator(state => {
	firebase.auth().signOut().then(() => {
		main.renderPage(`page-login`, `/`)
	}).catch(error => {
		console.error(error)
	})

	return state
})
