import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import View from '@/components/View'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/test',
      name: 'View',
      component: View
    },
    {
      path: '/view',
      name: 'HelloWorld',
      component: HelloWorld
    }
  ]
})
