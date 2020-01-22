import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    'file_name': '',
    'file_obj': '',
    'certificate': '',
    'crt_visible': false,
    'crt_format': '',
    'upload_visible': false
  },
  mutations: { 
    'update_file_name' (state, payload) {
      state.file_name = payload.data
    },       
    'update_file_obj' (state, payload) {
      state.file_obj = payload.data
    },  
    'update_certificate' (state, payload) {   
      state.certificate = payload.data
    },
    'update_crt_visible' (state, payload) {
      state.crt_visible = payload.data
    },
    'update_crt_format' (state, payload) {
      state.crt_format = payload.data
    },  
    'update_upload_visible' (state, payload) {
      state.upload_visible = payload.data
    }
  },
  actions: {
  },
  modules: {
  }
})
