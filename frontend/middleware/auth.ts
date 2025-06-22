onMounted(() => {
    const {$keycloak} = useNuxtApp()
    $keycloak.initKeycloak()
})