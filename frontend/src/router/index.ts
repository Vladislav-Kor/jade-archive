import { createRouter, createWebHistory } from 'vue-router'
import ProfileView from '@/views/ProfileView.vue'

const routes = [
    {
        path: '/',
        name: 'home',
        component: () => import('@/views/ProfileView.vue')
    },
    {
        path: '/person/:id',
        name: 'person',
        component: () => import('@/views/ProfileView.vue'),
        props: true
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
