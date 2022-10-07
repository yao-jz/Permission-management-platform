/*
    author: yhy2001
    date: 2021/5/4
    state: finished
*/
import $ from 'jquery'
import { shallowMount, mount, config } from '@vue/test-utils'
import createLocalVue from '@vue/test-utils'
import message from '@/views/message.vue'
import axios from 'axios'
import flushPromises from "flush-promises"
import { createRouter, createWebHistory } from 'vue-router'
import { delete_token, get_app_detail, sent_list, receive_list } from "@/utils/communication.js";
import modify_token_dialog from "@/components/modify_token_dialog.vue";
import { fail_msg, succeed_msg } from "@/utils/msg.js";
import { parser, parse_to_string } from "@/utils/time_parser.js";


const test_fail = 'test_fail'
const test_succeed = 'test_succeed'
const token_content = 'THUiLoveYou!!!'

jest.mock('@/utils/communication.js', () => {
    return {
        __esModule: true,
        sent_message: jest.fn(
            (token, key, message, to_user_name, user_name, pass_word, title) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: token == 'test_fail' ? "fail" : "succeed",
                        msg: "",
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
        )
    };
});

jest.mock('@/../public/assets/js/pcoded.min.js', () => {})
jest.mock('@/../public/assets/js/ripple.js', () => {})
jest.mock('@/../public/assets/js/vendor-all.min.js', () => {})
jest.mock('@/../public/assets/js/menu-setting.min.js', () => {})

const wrapper = shallowMount(message)

test('send_msg', async () => {
    // test_fail
    await wrapper.setProps({
        send_token: test_fail
    })
    await wrapper.vm.$nextTick()
    await wrapper.componentVM.send_msg("", "")
    await flushPromises()

    // test_succeed
    await wrapper.setProps({
        send_token: test_succeed
    })
    await wrapper.vm.$nextTick()
    await wrapper.componentVM.send_msg("", "")
    await flushPromises()

    expect(wrapper.vm.show_type).toBe(0)
    expect(wrapper.emitted()).toHaveProperty("close_msg_send")
    let emit_close_msg_send = wrapper.emitted("close_msg_send")
    expect(emit_close_msg_send).toHaveLength(1)
})

