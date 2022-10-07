/*
    author: yhy2001
    date: 2021/5/4
    state: finished
*/
import { shallowMount, mount, config } from '@vue/test-utils'
import createLocalVue from '@vue/test-utils'
import have_app_list from '@/views/have_app_list.vue'
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
        edit: jest.fn(
            (token, app_key, key, type, detail) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: token == 'test_fail' ? "fail" : "succeed",
                        msg: "",
                        message: "",
                    } });
                }),
        ),
        remove: jest.fn(
            (token, key, key_list, type) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: token == 'test_fail' ? "fail" : "succeed",
                        msg: "",
                        message: "",
                    } });
                }),
        ),
        add_app: jest.fn(
            (l, user_name, pass_word) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: user_name == 'test_fail' ? "fail" : "succeed",
                        msg: "",
                        message: "",
                    } });
                }),
        ),
    };
});

const wrapper = shallowMount(have_app_list, {
    props: {
        app_list: [
            0, 1, 2, 3, 4, 5
        ]
    }
})

test('open_and_close', async () => {
    await wrapper.componentVM.close_share_dialog()
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.selected_token).toBe("")
    expect(wrapper.vm.share_dialog_visible).toBe(false)

    await wrapper.componentVM.open_share_dialog("token", "key")
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.selected_token).toBe("token")
    expect(wrapper.vm.share_dialog_visible).toBe(true)

    await wrapper.componentVM.open_new_app()
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.dialog_type).toBe(0)
    expect(wrapper.vm.add_app_dialog_visible).toBe(true)

    await wrapper.componentVM.add_closed()
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.add_app_dialog_visible).toBe(false)
})

test('edit', async () => {
    await wrapper.componentVM.edit("", "", "", test_fail)
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty("update")
    let emit_update = wrapper.emitted("update")
    expect(emit_update).toHaveLength(1)

    await wrapper.componentVM.edit("", "", "", test_succeed)
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty("update")
    emit_update = wrapper.emitted("update")
    expect(emit_update).toHaveLength(2)
})

test('edit_app', async () => {
    await wrapper.componentVM.edit_app("token", {
        key: "key",
        name: "name",
        description: "description"
    })
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.dialog_type).toBe(1)
    expect(wrapper.vm.state.key).toBe("key")
    expect(wrapper.vm.state.name).toBe("name")
    expect(wrapper.vm.state.description).toBe("description")
    expect(wrapper.vm.selected_token).toBe("token")
    expect(wrapper.vm.edit_app_dialog_visible).toBe(true)
})

test('edit_closed', async () => {
    await wrapper.componentVM.edit_closed()
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.selected_token).toBe("")
    expect(wrapper.vm.edit_app_dialog_visible).toBe(false)
})

test('show_app_token', async () => {
    // no tokens

    // correct tokens
    await wrapper.componentVM.show_app_token([{
        content: "0"
    }], "")
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.token_dialog_visible).toBe(true)
    expect(wrapper.vm.selected_token).toBe("0")
})

test('close_app_token_dialog', async () => {
    await wrapper.componentVM.close_app_token_dialog()
    await wrapper.vm.$nextTick()

    expect(wrapper.emitted()).toHaveProperty("update")
    let emit_update = wrapper.emitted("update")
    expect(emit_update).toHaveLength(3)
    expect(wrapper.vm.token_dialog_visible).toBe(false)
    expect(wrapper.vm.selected_token).toBe("")
})

test('set_token', async () => {
    await wrapper.componentVM.set_token()
    await wrapper.vm.$nextTick()

    expect(wrapper.emitted()).toHaveProperty("show_detail")
    let emit_update = wrapper.emitted("show_detail")
    expect(emit_update).toHaveLength(1)
})

test('delete_app', async () => {
    await wrapper.componentVM.delete_app(test_fail, {
        key: ""
    })
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty("update")
    let emit_update = wrapper.emitted("update")
    expect(emit_update).toHaveLength(4)

    await wrapper.componentVM.delete_app(test_succeed, {
        key: ""
    })
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty("update")
    emit_update = wrapper.emitted("update")
    expect(emit_update).toHaveLength(5)
})


test('new_app', async () => {
    // test_fail
    await wrapper.setData({
        user_name: test_fail
    })
    await wrapper.vm.$nextTick()
    await wrapper.componentVM.new_app("", "")
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty("update")
    let emit_update = wrapper.emitted("update")
    expect(emit_update).toHaveLength(6)

    // test_succeed
    await wrapper.setData({
        user_name: test_succeed
    })
    await wrapper.vm.$nextTick()
    await wrapper.componentVM.new_app("", "")
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty("update")
    emit_update = wrapper.emitted("update")
    expect(emit_update).toHaveLength(7)
})

test('change_app_list', async () => {
    await wrapper.setProps({
        app_list: [
            0, 1, 2, 3, 4, 5, 6, 7, 8
        ]
    })
})
