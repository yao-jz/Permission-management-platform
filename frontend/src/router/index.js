import { createRouter, createWebHistory } from "vue-router";

const routes = [
    {
        path: "/",
        name: "Login",
        component: () =>
            import(/* webpackChunkName: "about" */ "../views/login/login.vue"),
        meta: {
            title: "企业通用权限平台-登录",
        },
    },
    {
        path: "/userlist",
        name: "Userlist",
        component: () => import("../views/user-list.vue"),
        meta: {
            title: "企业通用权限平台",
        },
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

/**
 * 在这里做 路由拦截
 */
router.beforeEach((to, from, next) => {
  
  console.log('to', to)
  next()
})

export default router
