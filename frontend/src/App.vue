<template>
    <router-view />
</template>

<style lang="scss">
html
{
    padding: 0;
    margin: 0;
    height: 100%;
}
body {
    font-family: "Open Sans", sans-serif;
    font-size: 14px;
    color: #373a3c;
    font-weight: 400;
    background: #4680ff;
    position: relative;
}
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: left;
    color: #2c3e50;
    margin-top: 0px;
    height: 100%;
}
#nav {
    padding: 30px;

    a {
        font-weight: bold;
        color: #2c3e50;

        &.router-link-exact-active {
            color: #42b983;
        }
    }
}
</style>
