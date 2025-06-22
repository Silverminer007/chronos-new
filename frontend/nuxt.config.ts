// https://nuxt.com/docs/api/configuration/nuxt-config

import tailwindcss from "@tailwindcss/vite";
import Aura from '@primeuix/themes/aura';

export default defineNuxtConfig({
    compatibilityDate: '2025-05-15',
    devtools: {enabled: true},
    css: ['~/assets/css/main.css'],
    vite: {plugins: [tailwindcss()]},
    runtimeConfig: {
        public: {
            keycloakClientId: process.env.NUXT_PUBLIC_KEYCLOAK_CLIENT_ID,
        },
    },
    modules: ['@nuxt/icon', '@primevue/nuxt-module', '@vueuse/nuxt'],
    primevue: {
        options: {
            theme: {
                preset: Aura
            }
        }
    }
})