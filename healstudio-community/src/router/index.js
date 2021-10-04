import Vue from "vue";
import VueRouter from "vue-router";
import Home from "@/views/Home";
import Login from "@/views/Login";
import SignUp from "@/views/SignUp"
import UserPage from "@/views/UserPage"
import Review from "@/views/Review"
import Trainer from "@/views/Trainer"
Vue.use(VueRouter);

const routes = [
  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: { transition: 'zoom' },
  },
  {
    path: "/signup",
    name: "SignUp",
    component: SignUp,
    meta: { transition: 'zoom' },
  },
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: { transition: 'fade' },
  },
  {
    path: "/review/:id",
    name: "Review",
    component: Review,

  },
  {
    path: "/trainer/:id",
    name: "Trainer",
    component: Trainer,
  },
  {
    path: "/user/:id",
    name: "UserPage",
    component: UserPage,

  },

]

const router = new VueRouter({
    routes,
  });
export default router;