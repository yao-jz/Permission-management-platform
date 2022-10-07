/*
    author: yhy2001
    date: 2021/5/5
    state: finished
*/
import { shallowMount, mount, config } from '@vue/test-utils'
import createLocalVue from '@vue/test-utils'
import access_dialog from '@/components/access_dialog.vue'
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
        change_token_access: jest.fn(
            (list, user_name, pass_word) =>
                new Promise((resolve, reject) => {
                    console.log(list)
                    resolve({ data: {
                        status: list[0].app_token == 'test_fail' ? "fail" : "succeed",
                        msg: "",
                        message: "",
                    } });
                }),
        ),
    };
});

const wrapper = mount(access_dialog)

test('close', async () => {
    await wrapper.componentVM.close()
    await wrapper.vm.$nextTick()

    expect(wrapper.emitted()).toHaveProperty("close")
    let emit_close = wrapper.emitted("close")
    expect(emit_close).toHaveLength(1)
})

test('confirm', async () => {
    // 权限不够
    await wrapper.setData({
        access_int: 0
    })
    await wrapper.setProps({
        self: 1
    })
    await wrapper.vm.$nextTick()
    await wrapper.componentVM.confirm()
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty("close")
    let emit_close = wrapper.emitted("close")
    expect(emit_close).toHaveLength(2)

    // 权限够

    await wrapper.setData({
        access_int: 1
    })
    await wrapper.setProps({
        token: test_fail
    })
    await wrapper.vm.$nextTick()
    await wrapper.componentVM.confirm()
    await flushPromises()

    await wrapper.setProps({
        token: test_succeed
    })
    await wrapper.vm.$nextTick()
    await wrapper.componentVM.confirm()
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty("close")
    emit_close = wrapper.emitted("close")
    expect(emit_close).toHaveLength(3)
})

test('change_value', async () => {
    await wrapper.componentVM.change_value("all")
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.access_int).toBe(0)

    await wrapper.componentVM.change_value("admin")
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.access_int).toBe(1)

    await wrapper.componentVM.change_value("add")
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.access_int).toBe(2)

    await wrapper.componentVM.change_value("edit")
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.access_int).toBe(3)

    await wrapper.componentVM.change_value("see")
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.access_int).toBe(4)

    await wrapper.componentVM.change_value("???")
    await wrapper.vm.$nextTick()
})