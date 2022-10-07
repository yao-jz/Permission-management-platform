/*
    author: yaojianzhu
    date: 2021/5/7
    state: not finish
*/
import { mount, config, shallowMount } from '@vue/test-utils'
import inbox from '@/components/inbox.vue'
import axios from 'axios'
import flushPromises from "flush-promises"
import { createRouter, createWebHistory } from 'vue-router'

const wrapper = shallowMount(inbox)

test('test_method_back', async () => {
    await wrapper.componentVM.back()
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.selected_from).toBe("")
    expect(wrapper.vm.selected_to).toBe("")
    expect(wrapper.vm.selected_title).toBe("")
    expect(wrapper.vm.selected_created_time).toBe("")
    expect(wrapper.vm.selected_msg).toBe("")
    expect(wrapper.vm.show_read).toBe(false)
})