/*
    author: yhy2001
    date: 2021/4/7
    state: finished
*/
import { shallowMount, mount, config } from '@vue/test-utils'
import user_edit from '@/components/user_edit.vue'
import axios from 'axios'
import flushPromises from "flush-promises"
import { createRouter, createWebHistory } from 'vue-router'
import * as router from '@/router/index.js'

test('router', async () => {
    let rs = router.routes
    let rr = router.router
})