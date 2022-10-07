/*
    author: yhy2001
    date: 2021/3/30
    state: finished
*/
import $ from 'jquery'
global.$ = $
import { mount, config } from '@vue/test-utils'
import login from '@/views/login/login.vue'
import axios from 'axios'
import flushPromises from "flush-promises"

const user_name = 'keven_durant'
const pass_word = '123456'

jest.mock('@/../public/assets/js/pcoded.min.js', () => {})
jest.mock('@/../public/assets/js/ripple.js', () => {})
jest.mock('@/../public/assets/js/vendor-all.min.js', () => {})
jest.mock('@/../public/assets/js/menu-setting.min.js', () => {})

test('empty_username_or_password', async () => {
    const wrapper = mount(login, {
        props: {
            type: 0
        }
    })
    //await wrapper.find('el-input[name="user_name"]').setValue(user_name)
    //await wrapper.find('el-input[name="pass_word"]').setValue('')
    await wrapper.setData({ login_form: {
            user_name: user_name,
            pass_word: "",
    } })
    await wrapper.setData({ login_form: {
        pass_word: "",
    } })
    await wrapper.find('el-button').trigger('click')

    //console.log(wrapper.find('el-message'))
    //const message = wrapper.vm.$message
    //console.log(wrapper.vm)
    //expect(wrapper.emitted('message')).toBeTruthy()
    //const message_event = wrapper.emitted('message')[0]
    //expect(message_event.type).toBe(["error"])
    //const login_form = wrapper.get('[data-test="login_form"]')
    //console.log(wrapper.find('el-input[name="user_name"]').attributes())
    expect(wrapper.vm.login_form.user_name).toBe(user_name)
    expect(wrapper.vm.login_form.pass_word).toBe('')
    expect(wrapper.find('el-input[name="user_name"]').attributes().modelvalue).toBe(user_name)
    expect(wrapper.find('el-input[name="pass_word"]').attributes().modelvalue).toBe('')

    await wrapper.setData({ login_form: {
        user_name: "",
        pass_word: pass_word,
    } })    
    expect(wrapper.find('el-input[name="user_name"]').attributes().modelvalue).toBe("")
    expect(wrapper.find('el-input[name="pass_word"]').attributes().modelvalue).toBe(pass_word)
})

/*
jest.mock('axios', () => ({
    post: jest.fn(() => Promise.resolve({
        data: {
            status: "failed",
            message: ""
        }
    }))
}))
*/

jest.mock('@/utils/communication.js', () => {
    return {
        __esModule: true,
        // mock queryUserName!!!!!
        login: jest.fn(
            (user_name, pass_word) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: user_name == 'test_failed' || pass_word == 'test_failed' ? "failed" : "succeed",
                        message: ""
                    } });
                }),
        ),
        register: jest.fn(
            (user_name, pass_word) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: user_name == 'test_failed' || pass_word == 'test_failed' ? "failed" : "succeed",
                        message: ""
                    } });
                }),
        ),
        
    };
});


test('no_such_username_or_wrong_password', async () => {
    // no such username
    
    const wrapper = mount(login, {
        props: {
            type: 0
        }
    })
    await wrapper.setData({ login_form: {
            user_name: 'test_failed',
            pass_word: "???",
    } })
    await wrapper.find('el-button').trigger('click')
    /*
    await mockAxios.post.mockImplementationOnce(() => {
        return Promise.resolve({
            data: {
                status: "failed",
                message: "no such username"
          },
        })
      })
    */
    await flushPromises()

    expect(wrapper.find('el-input[name="user_name"]').attributes().modelvalue).toBe('')
    expect(wrapper.find('el-input[name="pass_word"]').attributes().modelvalue).toBe('')

    // wrong password

    await wrapper.setData({ login_form: {
            user_name: '???',
            pass_word: "test_failed",
    } })
    await wrapper.find('el-button').trigger('click')
    await flushPromises()

    expect(wrapper.find('el-input[name="user_name"]').attributes().modelvalue).toBe('')
    expect(wrapper.find('el-input[name="pass_word"]').attributes().modelvalue).toBe('')
})

test('failed_register', async () => {
    // no username or password
    const wrapper = mount(login)
    await wrapper.setData({
        type: 1
    })
    await wrapper.setData({ login_form: {
        user_name: '',
        pass_word: "???",
    } })
    await wrapper.find('.register_button').trigger('click')
    await wrapper.vm.$nextTick()

    expect(wrapper.find('el-input[name="user_name"]').attributes().modelvalue).toBe('')
    expect(wrapper.find('el-input[name="pass_word"]').attributes().modelvalue).toBe('???')

    // failed http request
    await wrapper.setData({ login_form: {
        user_name: 'test_failed',
        pass_word: "???",
    } })
    wrapper.setData({
        type: 0
    })
    await wrapper.find('.register_button').trigger('click')
    await flushPromises()
    await wrapper.setData({ login_form: {
        user_name: 'test_failed',
        pass_word: "???",
    } })
    await wrapper.find('.register_button').trigger('click')
    await flushPromises()
    expect(wrapper.find('el-input[name="user_name"]').attributes().modelvalue).toBe('')
    expect(wrapper.find('el-input[name="pass_word"]').attributes().modelvalue).toBe('')
})

test('succeed_register', async () => {
    const wrapper = mount(login)
    await wrapper.setData({
        type: 1
    })
    await wrapper.setData({ login_form: {
        user_name: 'test_succeed',
        pass_word: "test_succeed",
    } })
    await wrapper.find('.register_button').trigger('click')
    await wrapper.vm.$nextTick()

    expect(wrapper.find('el-input[name="user_name"]').attributes().modelvalue).toBe('test_succeed')
    expect(wrapper.find('el-input[name="pass_word"]').attributes().modelvalue).toBe('test_succeed')
})

test('return_to_login', async () => {
    const wrapper = mount(login)
    await wrapper.setData({
        type: 1
    })
    await wrapper.componentVM.return_to_login()
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.type).toBe(0)
    expect(wrapper.vm.login_form.user_name).toBe("")
    expect(wrapper.vm.login_form.pass_word).toBe("")
})
