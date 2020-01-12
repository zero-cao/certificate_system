import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/certificate/parsing',
    name: 'crt_parse',
    component: () => import('../views/CertificateParsing.vue')
  },
  {
    path: '/certificate/signing',
    name: 'crt_sign',
    component: () => import('../views/CertificateSigning.vue')
  },
  {
    path: '/certificate/making',
    name: 'crt_make',
    component: () => import('../views/CertificateMaking.vue')
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
  },
  {
    path: '/certificate/ca',
    name: 'crt_ca',
    component: () => import('../views/CertificateCA.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
