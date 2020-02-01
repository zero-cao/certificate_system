import {post, get, remove} from '../http/service'

export const http = {
	crt_parse: function(data) {
		return post('/certificate/parsing', data, {}, 'multipart/form-data', 'json')
  },
  
  upload_crt_files: function(data) {
    return post('/certificate/files', data, {}, 'multipart/form-data', '')
  },
  get_crt_files: function() {
    return get('/certificate/files')
  },


  download_crt_file: function(filename) {
    return get('/certificate/file/', {'filename': filename, 'operation': 'download'}, 'blob')
  },
  parse_crt_file: function(filename) {
    return get('/certificate/file/', {'filename': filename, 'operation': 'parse'}, 'json')
  },  
  remove_crt_file: function(filename) {
    return remove('/certificate/file/', {'filename': filename})
  },

	sign_crt_file: function(data) {
		return post('/certificate/file/', data, {'operation': 'sign'}, 'multipart/form-data', 'json')
	},
	make_crt_file: function(data) {
		return post('/certificate/file/', data, {'operation': 'make'}, 'application/json', 'json')
  }    
}
