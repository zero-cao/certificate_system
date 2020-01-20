import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    'certificate': '',
    'crt_visible': false,
    'crt_parsed': false
  },
  mutations: {    
    'update_certificate' (state, payload) {   
      state.certificate = payload.data
    },
    'update_crt_visible' (state, payload) {
      state.crt_visible = payload.data
    },
    'update_crt_parsed' (state, payload) {
      state.crt_parsed = payload.data
    }              
  },
  actions: {
  },
  modules: {
  }
})
