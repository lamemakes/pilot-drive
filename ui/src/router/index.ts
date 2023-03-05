import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import { routes } from "../constants/routes";

const populateRoutes:RouteRecordRaw[] = []

routes.forEach((route) => {
  populateRoutes.push({
    path: `/${route.name}`,
    name: `${route.name}`,
    component: () => import(`../views/${route.name.charAt(0).toUpperCase()}${route.name.slice(1)}.vue`)
  })
})

console.log(populateRoutes);

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      redirect: () => {
        return { name: "media" };
      },
    },
    ...populateRoutes
  ],
});

export default router;
