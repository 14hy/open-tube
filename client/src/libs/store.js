import createStore from './redux-zero.js'

const initialState = {
	info: [] , 
	isLogin: false,
}
const store = createStore(initialState)

export default store
