/*
    author: yhy2001
    date: 2021/5/4
    state: finished
*/
import { shallowMount, mount, config } from '@vue/test-utils'
import createLocalVue from '@vue/test-utils'
import set_time from '@/components/set_time.vue'
import axios from 'axios'
import flushPromises from "flush-promises"
import { createRouter, createWebHistory } from 'vue-router'
import { delete_token, get_app_detail } from "@/utils/communication.js";
import modify_token_dialog from "@/components/modify_token_dialog.vue";
import { fail_msg, succeed_msg } from "@/utils/msg.js";
import { parser, parse_to_string } from "@/utils/time_parser.js";

const test_fail = 'test_fail'
const test_succeed = 'test_succeed'
const token_content = 'THUiLoveYou!!!'

jest.mock('@/utils/communication.js', () => {
    return {
        __esModule: true,
        set_role_time: jest.fn(
            (token, key, user_keys, role_keys) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: token == 'test_fail' ? "fail" : "succeed",
                        msg: "",
                        message: "",
                    } });
                }),
        ),
    };
});

const wrapper = mount(set_time)

test('infinite', async () => {
    await wrapper.setProps({
        app_token: test_fail
    })
    await wrapper.vm.$nextTick()
    await wrapper.componentVM.infinite()
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty("close")
    let emit_close = wrapper.emitted("close")
    expect(emit_close).toHaveLength(1)

    await wrapper.setProps({
        app_token: test_succeed
    })
    await wrapper.vm.$nextTick()
    await wrapper.componentVM.infinite()
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty("close")
    emit_close = wrapper.emitted("close")
    expect(emit_close).toHaveLength(2)
})

test('close', async () => {
    await wrapper.componentVM.close()
    await wrapper.vm.$nextTick()

    expect(wrapper.emitted()).toHaveProperty("close")
    let emit_close = wrapper.emitted("close")
    expect(emit_close).toHaveLength(3)
})

test('confirm', async () => {
    await wrapper.setProps({
        app_token: test_fail
    })
    await wrapper.vm.$nextTick()
    await wrapper.componentVM.confirm()
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty("close")
    let emit_close = wrapper.emitted("close")
    expect(emit_close).toHaveLength(4)

    await wrapper.setProps({
        app_token: test_succeed
    })
    await wrapper.vm.$nextTick()
    await wrapper.componentVM.confirm()
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty("close")
    emit_close = wrapper.emitted("close")
    expect(emit_close).toHaveLength(5)
})

test('change_visible', async () => {
    await wrapper.setProps({
        visible: true
    })
    await wrapper.vm.$nextTick()

    await wrapper.setProps({
        visible: false
    })
    await wrapper.vm.$nextTick()

    await wrapper.setProps({
        visible: true
    })
    await wrapper.vm.$nextTick()
})
