import createStore from './redux-zero.js'
import { main } from '../main.js'

const initialState = {
	router: {
		login: {
			requireLogin: false,
		},
		reports: {
			requireLogin: false,
		},
		report: {
			requireLogin: true,
		},
	},
	userInfo: {}, 
	isLogin: false,
}
const store = createStore(initialState)

initLoginState()

function initLoginState() {
	const state = store.getState()
	firebase.auth().onAuthStateChanged(user => {
		const pathName = location.pathname.split(`/`)[1] || `login`

		if (user) {
			const displayName = user.displayName
			const email = user.email
			const emailVerified = user.emailVerified
			const photoURL = user.photoURL
			const uid = user.uid
			const phoneNumber = user.phoneNumber
			const providerData = user.providerData			

			user.getIdToken().then(accessToken => {
				state.isLogin = true
				state.userInfo = {
					displayName,
					email,
					emailVerified,
					phoneNumber,
					photoURL,
					uid,
					accessToken,
					providerData,
				}
				store.setState(state)
			})
		} else {
			state.isLogin = false
			state.userInfo = {}
			store.setState(state)
			routeLogin(false, pathName)
		}
	}, error => {
		console.error(error)
	})

	return state
}

function routeLogin(isLogin, pathName) {
	const isNeedLogin = () => isLogin || isLogin === store.getState().router[pathName][`requireLogin`]
	
	if (isNeedLogin()) {
		main.connectLoginNoLoad(pathName)
		return
	}
	isLogin ? main.connectLoginNoLoad(pathName) : main.connectLoginNoLoad(`login`)
}

export default store
