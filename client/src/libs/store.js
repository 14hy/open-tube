import createStore from './redux-zero.js'

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

export default store
