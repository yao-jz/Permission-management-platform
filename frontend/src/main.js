/*
 * @Description: 文件及简介
 * @Author: Cary
 * @Date: 2021-03-15 15:20:08
 * @FilePath: \excel-to-jsone:\work\vue-project\frontend\src\main.js
 */
import { createApp } from "vue";
import ElementPlus from "element-plus";
import "element-plus/lib/theme-chalk/index.css";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import axios from "axios";
axios.defaults.withCredentials = true;
router.beforeEach((to, from, next) => {
    /* 路由发生变化修改页面title */
    if (to.meta.title) {
        document.title = to.meta.title;
    }
    next();
});

const app = createApp(App);
app.use(ElementPlus, { size: "small", zIndex: 3000 }); //size改变组件的默认尺寸，zIndex设置弹框初始值
app.use(store).use(router).mount("#app");
