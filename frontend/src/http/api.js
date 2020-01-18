import {post, get, remove} from '../http/service'

export const http = {
	crt_parse: function(data, type) {
		return post('/certificate/parsing', data, type)
	},
	crt_sign: function(data, type) {
		return post('/certificate/signing', data, type)
	},
	crt_make: function(data, type) {
		return post('/certificate/making', data, type)
  },
  get_crt_files: function() {
    return get('/certificate/files')
  },
  get_crt_file: function(params) {
    return get('/certificate/file/', params)
  },
  remove_crt_file: function(params) {
    return remove('/certificate/file/', params)
  }  
}
