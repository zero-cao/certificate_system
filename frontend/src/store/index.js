import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    'file_name': '',
    'file_obj': '',
    'byte_crt': '',
    'parse_visible': false,
    'upload_visible': false,
    'make_visible': false
  },
  mutations: { 
    'update_file_name' (state, payload) {
      state.file_name = payload.data
    },       
    'update_file_obj' (state, payload) {
      state.file_obj = payload.data
    },  
    'update_byte_crt' (state, payload) {   
      state.byte_crt = payload.data
    },
    'update_parse_visible' (state, payload) {
      state.parse_visible = payload.data
    },     
    'update_upload_visible' (state, payload) {
      state.upload_visible = payload.data
    },
    'update_make_visible' (state, payload) {
      state.make_visible = payload.data
    }
  },
  actions: {
  },
  modules: {
  }
})
