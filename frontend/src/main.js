import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import {http} from '../src/http/api'
import {blob} from '../src/blob/index'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

Vue.use(ElementUI)
Vue.prototype.$http = http
Vue.prototype.blob = blob
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
