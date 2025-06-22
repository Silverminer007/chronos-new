// plugins/keycloak.client.ts
import Keycloak from 'keycloak-js'

export default defineNuxtPlugin(() => {
    const config = useRuntimeConfig()

    const keycloak = new Keycloak({
        url: 'https://auth.chronos-live.de/',
        realm: 'chronos',
        clientId: config.public.keycloakClientId,
    })

    const token = useState<string | null>('token', () => null)
    const authenticated = ref(false)

    async function initKeycloak() {
        try {
            await keycloak.init({
                onLoad: 'check-sso',
                pkceMethod: 'S256',
                enableLogging: false,
                checkLoginIframe: true,
            })

            if (keycloak.authenticated) {
                token.value = keycloak.token || null
                authenticated.value = true
                startTokenRefresh()
            }
        } catch (err) {
            console.error('Keycloak init error:', err)
        }
    }

    function login() {
        return keycloak.login({
            scope: 'openid profile email offline_access', // offline_access = long-lived refresh
        })
    }

    function logout() {
        stopTokenRefresh()
        return keycloak.logout()
    }

    function getToken() {
        return keycloak.token || null
    }

    function isAuthenticated() {
        return authenticated.value
    }

    // Auto-refresh Token
    let refreshInterval: NodeJS.Timer

    function startTokenRefresh() {
        stopTokenRefresh()
        refreshInterval = setInterval(() => {
            if (!keycloak.token) return

            keycloak.updateToken(30).then((refreshed) => {
                if (refreshed) {
                    token.value = keycloak.token || null
                    console.debug('🔁 Token refreshed')
                }
            }).catch((err) => {
                console.warn('❌ Token refresh failed, logging out', err)
                logout()
            })
        }, 10_000)
    }

    function stopTokenRefresh() {
        if (refreshInterval) {
            clearInterval(refreshInterval)
        }
    }

    return {
        provide: {
            keycloak: {
                initKeycloak,
                login,
                logout,
                getToken,
                isAuthenticated,
            },
        },
    }
})
