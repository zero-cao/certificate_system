import {post, get, remove} from '../http/service'

export const http = {
	crt_parse: function(data, type) {
		return post('/certificate/parsing', data, type)
  },
  
  upload_crt_files: function(data, type) {
    return post('/certificate/files', data, type)
  },
  get_crt_files: function() {
    return get('/certificate/files')
  },

  get_crt_file: function(params, resType) {
    return get('/certificate/file/', params, resType)
  },
  remove_crt_file: function(params) {
    return remove('/certificate/file/', params)
  },
	sign_crt_file: function(data, params) {
		return post('/certificate/file/', data, params, 'multipart/form-data', 'blob')
	},
	make_crt_file: function(data, params) {
		return post('/certificate/file/', data, params, 'application/json', 'blob')
  }    
}
