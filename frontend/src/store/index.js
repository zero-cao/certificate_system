import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    'certificate': '',
    'crt_visible': false,
    'crt_format': '',
  },
  mutations: {    
    'update_certificate' (state, payload) {   
      state.certificate = payload.data
    },
    'update_crt_visible' (state, payload) {
      state.crt_visible = payload.data
    },
    'update_crt_format' (state, payload) {
      state.crt_format = payload.data
    }             
  },
  actions: {
  },
  modules: {
  }
})
