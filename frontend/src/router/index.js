import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../components/login.vue';
import HomeView from '../components/home.vue';
import ForgotPassView from '../components/forgotpass.vue';
import RegisterView from '../components/register.vue';

const routes = [
  {
    path: '/',
    name: 'login',
    component: LoginView 
  },
  {
    path: '/home',
    name: 'home',
    component: HomeView
  },
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: ForgotPassView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;