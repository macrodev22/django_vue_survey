import { createRouter, createWebHistory } from "vue-router";
import Signin from "../views/Signin.vue";
import Dashboard from "../views/Dashboard.vue";
import Register from "../views/Register.vue";
import SurveyView from "../views/SurveyView.vue";
import NotFound from "../views/NotFound.vue";
import UserProfile from "../views/UserProfile.vue";

import { useStore } from "../store"

const routes = [
    {
        path: '/',
        redirect: '/dashboard',
        // component: Dashboard,
    },
    {
        path: '/dashboard',
        component: Dashboard,
        name: 'Dashboard',
        meta: {
            requiresAuth: true,
        },
        children: [
            { path: '/surveys', name: 'Surveys', component: SurveyView},
            { path: '/surveys/:id', name: 'SurveysView', component: SurveyView },
            { path: '/surveys/create', name: 'SurveysCreate', component: SurveyView },
            { path: '/profile', name: 'UserProfile', component: UserProfile },
        ]
    },
    {
        path: '/auth',
        redirect: '/login',
        name: 'Auth',
        meta: {
            isGuest: true,
        },
        children: [
            {
                path: '/register',
                component: Register,
                name: 'Register'
            },
            {
                path: '/login',
                component: Signin,
                name: 'Login'
            },
        ]
    },
    {
        path: '/view/survey/:slug',

    },
    {
        path: '/404',
        component: NotFound,
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})


router.beforeEach((to, from, next) => {
    const store = useStore()
    // If to route requires auth and user not auth, redirect login
    // && !useStore.auth.user.token
    if (to.meta.requiresAuth && !store.auth.user.token)
        next({ name: 'Login' })
    else if (store.auth.user.token && to.meta.isGuest)
        next({ name: 'Dashboard' })
    else
        next()
})

export default router;