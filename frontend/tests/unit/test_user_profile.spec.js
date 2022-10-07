/*
    author: yhy2001
    date: 2021/5/5
    state: finished
*/
import { mount, config, shallowMount } from '@vue/test-utils'
import user_profile from '@/views/user_profile.vue'
import axios from 'axios'
import {
    get_avatar,
    get_info,
    delete_user,
    receive_list,
    logout,
} from "@/utils/communication.js";
import flushPromises from "flush-promises"
import { createRouter, createWebHistory } from 'vue-router'
import GLOBAL from "@/utils/global_variable.js";

const test_fail = 'test_fail'
const test_succeed = 'test_succeed'

jest.mock('@/utils/communication.js', () => {
    return {
        __esModule: true,
        get_avatar: jest.fn(
            (user_name, pass_word) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: user_name == 'test_fail' ? "fail" : "succeed",
                        avatar: '/THUiLoveYou!!!',
                        msg: "",
                        message: "",
                    } });
                }),
        ),
        get_info: jest.fn(
            (user_name, pass_word) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: user_name == 'test_fail' ? "fail" : "succeed",
                        email: "hhh",
                        message: "",
                        msg: ""
                    } });
                }),
        ),
        delete_user: jest.fn(
            (user_name, pass_word) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: user_name == 'test_fail' ? "fail" : "succeed",
                        message: "",
                    } });
                }),
        ),
        sent_list: jest.fn(
            (user_name, pass_word, from, to) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: user_name == 'test_fail' ? "fail" : "succeed",
                        msg: "",
                        message: "",
                    } });
                })
        ),
        receive_list: jest.fn(
            (user_name, pass_word, from, to) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: user_name == 'test_fail' ? "fail" : "succeed",
                        msg: "",
                        message: "",
                    } });
                })
        ),
        logout: jest.fn(
            (user_name, pass_word) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: user_name == 'test_fail' ? "fail" : "succeed",
                        msg: "",
                        message: "",
                    } });
                })
        )
    };
});

jest.mock('@/../public/assets/js/pcoded.min.js', () => {})
jest.mock('@/../public/assets/js/ripple.js', () => {})
jest.mock('@/../public/assets/js/vendor-all.min.js', () => {})
jest.mock('@/../public/assets/js/menu-setting.min.js', () => {})
jest.mock('@/../public/assets/js/plugins/jquery-ui.min.js', () => {})
jest.mock('@/../public/assets/js/plugins/fullcalendar.min.js', () => {})

const $message = {
    state: {
      count: 25
    },
    commit: jest.fn(),
    error: jest.fn(),
  }

const wrapper = shallowMount(user_profile, {
    global: {
        mocks: {
            $message
        }
    }
})

test('open_and_close', async () => {
    await wrapper.componentVM.open_user_delete_dialog()
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.user_delete_dialog_visible).toBe(true)
    
    await wrapper.componentVM.close_user_delete_dialog()
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.user_delete_dialog_visible).toBe(false)
    
    await wrapper.componentVM.open_email_edit_dialog()
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.email_edit_dialog_visible).toBe(true)
    
    await wrapper.componentVM.close_email_edit_dialog()
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.email_edit_dialog_visible).toBe(false)
    
    await wrapper.componentVM.open_user_edit_dialog()
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.user_edit_dialog_visible).toBe(true)
    
    await wrapper.componentVM.close_user_edit_dialog()
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.user_edit_dialog_visible).toBe(false)
    
})

test('test_confirm_user_delete_method', async () => {
    // failed
    await wrapper.setData({
        user_name: test_fail
    })
    await wrapper.componentVM.confirm_user_delete()
    await wrapper.vm.$nextTick()
    
    // succeed
    await wrapper.setData({
        user_name: test_succeed
    })
    await wrapper.componentVM.confirm_user_delete()
    await wrapper.vm.$nextTick()
})

test('func', async () => {
    await wrapper.componentVM.func()
})

test('init_form', async () => {
    await wrapper.componentVM.init_form()
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.form.user_name).toBe("")
    expect(wrapper.vm.form.pass_word).toBe("")
})

test('test_method_before_avatar_upload', async () => {
    // 该方法已删除
    // not JPG and file too large
    //expect(wrapper.getComponent(Foo).vm.msg).toBe('hello world')
    let file = "C:\\Users\\asus\\Desktop\\Math.txt"
    await wrapper.componentVM.before_avatar_upload(file)
    expect($message.error).toHaveBeenCalledTimes(2)
    file = "@\\..\\public\\111.jpg"
    await wrapper.componentVM.before_avatar_upload(file)
    expect($message.error).toHaveBeenCalledTimes(4)
})

test('test_method_handle_avatar_success', async () => {
    // 未解决！！！
    /*
    let file = {
        raw: "@\\..\\public\\111.jpg"
    }
    wrapper.componentVM.handle_avatar_success(0, file)
    */
})