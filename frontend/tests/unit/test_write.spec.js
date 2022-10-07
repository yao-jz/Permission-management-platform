/*
    author: yhy2001
    date: 2021/5/4
    state: finished
*/
import { shallowMount, mount, config } from '@vue/test-utils'
import createLocalVue from '@vue/test-utils'
import write from '@/components/write.vue'
import axios from 'axios'
import flushPromises from "flush-promises"
import { createRouter, createWebHistory } from 'vue-router'
import { delete_token, get_app_detail } from "@/utils/communication.js";
import modify_token_dialog from "@/components/modify_token_dialog.vue";
import { fail_msg, succeed_msg } from "@/utils/msg.js";
import { parser, parse_to_string } from "@/utils/time_parser.js";

const wrapper = mount(write)

test('send', async () => {
    await wrapper.componentVM.send()
    await wrapper.vm.$nextTick()
    expect(wrapper.emitted()).toHaveProperty("send_msg")
    expect(wrapper.vm.to).toBe("")
    expect(wrapper.vm.msg).toBe("")
})