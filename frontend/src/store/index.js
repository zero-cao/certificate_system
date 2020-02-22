import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    'component_name': '',    
    'pending_file': {},
    'selected_file': {
      'filename': '',
      'file_type': ''
    }
  },
  mutations: { 
    'update_component_name' (state, payload) {
      state.component_name = payload.data
    },          
    'update_pending_file' (state, payload) {
      state.pending_file = payload.data
    },         
    'update_selected_file' (state, payload) {
      state.selected_file = payload.data
    }      
  },
  actions: {
  },
  modules: {
  }
})
