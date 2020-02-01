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
    return response.data 
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
export function get(url, params={}, resType='') {
  let config_form = {params: params, responseType: resType}
	return new Promise(
		(resolve, reject) => {
			axios.get(url, config_form)
          .then(response => { resolve(response) })
          .catch(error => { reject(error) })
		}
	)
}

// for delete
export function remove(url, params={}) {
	return new Promise(
		(resolve, reject) => {
			axios.delete(url, {params: params})
          .then(response => { resolve(response) })
          .catch(error => { reject(error) })
		}
	)
}

// for post
// type: 'multipart/form-data' or 'application/json'
export function post(url, data={}, params={}, type='application/json', resType='') {
	let config_form = { headers: { 'Content-Type': type }, params: params, responseType: resType }	
	return new Promise(
		(resolve, reject) => {
			axios.post(url, data, config_form)
					.then(response => { resolve(response) })
					.catch(error => { reject(error) })
		}
	)
}
