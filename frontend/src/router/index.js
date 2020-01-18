import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'crt_files',
    component: () => import('../views/CertificateFiles.vue')
  },  
  {
    path: '/certificate/publish',
    name: 'crt_pblh',
    component: () => import('../views/CertificatePublish.vue')
  },    
  {
    path: '/certificate/parsing',
    name: 'crt_parse',
    component: () => import('../views/CertificateParsing.vue')
  },  
  {
    path: '/certificate/data',
    name: 'crt_data',
    component: () => import('../views/CertificateData.vue')
  },
  {
    path: '/certificate/file',
    name: 'crt_file',
    component: () => import('../views/CertificateFile.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
