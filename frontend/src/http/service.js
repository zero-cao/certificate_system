import axios from 'axios'

axios.defaults.timeout = 3000
// axios.defaults.baseURL = 'http://10.74.133.124:8000'
axios.defaults.baseURL = 'http://127.0.0.1:8000'

// request interceptors
axios.interceptors.request.use(
	config => { 
		return config
	}, 
	error => { 
		return Promise.reject(error)
	} 
)

// response interceptors
axios.interceptors.response.use(
	response => {
		if (response.headers['content-type'] === 'text/plain; charset=utf-8') { return(response.data) }
		else if (response.headers['content-type'] ==='application/json') { return response.data }
	},
	error => {
		var content = null
		var title = null

		if (error.response == undefined) {
			content = error.message
			if (error.code) { title = error.code }
			else { title = 'No response' }
		}
		else {
			content = error.response.data 
			title = error.response.status + ': ' + error.response.statusText
		}
		error.message = {
			content: content,
			title: title
		}

		return Promise.reject(error)
	}
)

// for get 
export function get(url, params={}) {
	return new Promise(
		(resolve, reject) => {
			axios.get(url, {params: params})
					.then(response => {
						resolve(response.data)
					})
					.catch(error => {reject(error)})
		}
	)
}

// for post
// type: 'multipart/form-data' or 'application/json'
export function post(url, data={}, type='application/json') {
	let config_form = { headers: { 'Content-Type': type } }	
	return new Promise(
		(resolve, reject) => {
			axios.post(url, data, config_form)
					.then(response => { resolve(response) })
					.catch(error => { reject(error) })
		}
	)
}
