import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    'crt_file': '',
    'crt_data': '',
    'crt_ca': ''
  },
  mutations: {    
    'update_crt_file' (state, payload) {  
      state.crt_file = payload.data
    },
    'update_crt_data' (state, payload) {   
      state.crt_data = payload.data
    },
    'update_crt_ca' (state, payload) {   
      state.crt_ca = payload.data
    }    
  },
  actions: {
  },
  modules: {
  }
})
