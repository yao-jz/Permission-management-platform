/*
    author: yhy2001
    date: 2021/4/27
    state: finished
*/
import { mount, config, shallowMount } from '@vue/test-utils'
import email from '@/components/email.vue'
import axios from 'axios'
import flushPromises from "flush-promises"
import { createRouter, createWebHistory } from 'vue-router'

const test_fail = 'test_fail'
const test_succeed = 'test_succeed'

jest.mock('@/utils/communication.js', () => {
    return {
        __esModule: true,
        verify_code: jest.fn(
            (code, email) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: email == 'test_fail' ? "fail" : "succeed",
                        message: "",
                    } });
                }),
        ),
        edit_email: jest.fn(
            (user_name, pass_word, email) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: email == 'test_fail' ? "fail" : "succeed",
                        message: "",
                    } });
                }),
        ),
        get_info: jest.fn(
            (user_name, pass_word) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: "succeed",
                        email: user_name == 'test_fail' ? 'test_fail' : 'test_succeed',
                        message: "",
                    } });
                }),
        ),
    };
});

const wrapper = mount(email)

test('test_close_method', async () => {
    await wrapper.componentVM.close()
    await wrapper.vm.$nextTick()
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty('close')
    let emit_close = wrapper.emitted('close')
    expect(emit_close).toHaveLength(1)
})

test('test_confirm_method', async () => {
    // confirm failed
    await wrapper.setData({
        email: test_fail
    })
    await wrapper.vm.$nextTick()
    await wrapper.componentVM.confirm()
    await flushPromises()

    expect(wrapper.vm.key_wrong_message).toBe("验证码错误")

    // confirm succeeded
    await wrapper.setData({
        email: test_succeed
    })
    await wrapper.vm.$nextTick()
    await wrapper.componentVM.confirm()
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty('close')
    let emit_close = wrapper.emitted('close')
    expect(emit_close).toHaveLength(2)
})

test('test_send_check_key_method', async () => {
        // send failed
        await wrapper.setData({
            email: test_fail
        })
        await wrapper.vm.$nextTick()
        await wrapper.componentVM.send_check_key()
        await flushPromises()
        
        // send succeeded
        await wrapper.setData({
            email: test_succeed
        })
        await wrapper.vm.$nextTick()
        await wrapper.componentVM.send_check_key()
        await flushPromises()
})

test('change_visible', async () => {
    await wrapper.setProps({
        visible: true
    })
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.email).toBe(test_succeed)
    expect(wrapper.vm.dialog_visible).toBe(true)

    await wrapper.setProps({
        visible: false
    })
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.email_valid).toBe(false)
    expect(wrapper.vm.key_valid).toBe(false)
    expect(wrapper.vm.email).toBe('')
    expect(wrapper.vm.code).toBe('')
    expect(wrapper.vm.dialog_visible).toBe(false)

})