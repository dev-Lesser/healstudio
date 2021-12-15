import Vue from "vue";
import VueRouter from "vue-router";
import Home from "@/views/Home";
import Login from "@/views/Login";
import Review from "@/views/Review"
Vue.use(VueRouter);

const routes = [
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/review/:id",
    name: "Review",
    component: Review,
  },

]

const router = new VueRouter({
    routes,
  });
export default router;