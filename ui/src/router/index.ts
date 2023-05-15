import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import { inject } from 'vue';
import {Settings} from '../types/Settings.interface'
import { routes } from "../constants/routes";

const populateRoutes:RouteRecordRaw[] = []

routes.forEach((route) => {
  populateRoutes.push({
    path: `/${route.name}`,
    name: `${route.name}`,
    component: () => import(`../components/${route.name.charAt(0).toUpperCase()}${route.name.slice(1)}/${route.name.charAt(0).toUpperCase()}${route.name.slice(1)}.vue`)
  })
})

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      redirect: () => {
        return { name: (inject("settingsStore") as Settings).home };
      },
    },
    ...populateRoutes
  ],
});

export default router;
