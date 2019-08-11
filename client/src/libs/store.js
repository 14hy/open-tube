import createStore from './redux-zero.js'

const initialState = {
	userInfo: [] , 
	isLogin: false,
}
const store = createStore(initialState)

export default store
