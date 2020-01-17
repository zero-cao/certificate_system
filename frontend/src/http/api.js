import {post, get} from '../http/service'

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
  crt_files: function() {
    return get('/certificate/files')
  }
}
