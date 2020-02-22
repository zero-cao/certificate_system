import {post, get, remove} from '../http/service'

export const http = {
  upload_crt_files: function(data) {
    return post('/certificate/files', data, {}, 'multipart/form-data', '')
  },
  get_crt_files: function() {
    return get('/certificate/files')
  },

  parse_crt_file: function(filename) {
    return get('/certificate/file/', {'filename': filename, 'operation': 'parse'}, 'json')
  },  
  download_crt_file: function(filename) {
    return get('/certificate/file/', {'filename': filename, 'operation': 'download'}, 'blob')
  },
  remove_crt_file: function(filename) {
    return remove('/certificate/file/', {'filename': filename})
  },
  convert_crt_file: function(filename, data) {
    return post('/certificate/file/', data, {'filename': filename, 'operation': 'convert'}, 'application/json', 'blob')
  },

	sign_crt_file: function(data) {
		return post('/certificate/file/', data, {'operation': 'sign'}, 'multipart/form-data', 'json')
	},
	make_crt_file: function(data) {
		return post('/certificate/file/', data, {'operation': 'make'}, 'application/json', 'json')
  }    
}
