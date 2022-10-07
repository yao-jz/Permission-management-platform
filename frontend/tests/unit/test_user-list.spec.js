/*
    author: yhy2001
    date: 2021/4/1
    state: semi-finished
*/
import { mount, config, shallowMount } from '@vue/test-utils'
import user_list from '@/views/user-list.vue'
import axios from 'axios'
import flushPromises from "flush-promises"
import { createRouter, createWebHistory } from 'vue-router'
import GLOBAL from "@/utils/global_variable.js";

const test_fail = 'test_fail'
const test_succeed = 'test_succeed'

const test_list = [
    {
        created_time: 10
    },
    {
        created_time: -1
    }
]

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
        get_app_list: jest.fn(
            (user_name, pass_word) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: user_name == 'test_fail' ? "fail" : "succeed",
                        list: [
                                {
                                    created_time: 10
                                },
                                {
                                    created_time: -1
                                }
                            ],
                        message: "",
                        msg: ""
                    } });
                }),
        ),
        edit: jest.fn(
            (token, app_key, key, type, detail) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: token == 'test_fail' ? "fail" : "succeed",
                        message: "",
                        msg: ""
                    } });
                }),
        ),
        add_app: jest.fn(
            (l, user_name, pass_word) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: user_name == 'test_fail' ? "fail" : "succeed",
                        message: "",
                        msg: ""
                    } });
                }),
        ),
        logout: jest.fn(
            () =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: "",
                        message: "",
                    } });
                }),
        ),
        remove: jest.fn(
            (token, key, key_list, type) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: token == 'test_fail' ? "fail" : "succeed",
                        message: "",
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
        get_shared_app: jest.fn(
            (user_name, pass_word) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: user_name == 'test_fail' ? "fail" : "succeed",
                        list: [
                                {
                                    created_time: 10
                                },
                                {
                                    created_time: -1
                                }
                            ],
                        message: "",
                        msg: ""
                    } });
                }),
        ),
    };
});

jest.mock('@/../public/assets/js/pcoded.min.js', () => {})
jest.mock('@/../public/assets/js/ripple.js', () => {})
jest.mock('@/../public/assets/js/vendor-all.min.js', () => {})
jest.mock('@/../public/assets/js/menu-setting.min.js', () => {})
jest.mock('@/../public/assets/js/plugins/jquery-ui.min.js', () => {})
jest.mock('@/../public/assets/js/plugins/fullcalendar.min.js', () => {})

const mock_router = {
    replace: jest.fn(),
    push: jest.fn()
}

const router = createRouter({
    history: createWebHistory(),
    routes: [
        /*
        {
            path: '/aa',
            name: home,
            component: home,
        },
        */
        {
            path: '/',
            name: 'Userlist',
            component: {
                template: '/'
            }
        },
    ]
})

//console.log(user_list)
const wrapper = shallowMount(user_list, {
    global: {
        mocks: {
            $router: mock_router
        },
        plugins: [router]
    }
})

test('test_open_child_components', async () => {
    await wrapper.componentVM.open_new_app()
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.dialog_type).toBe(0)
    expect(wrapper.vm.add_app_dialog_visible).toBe(true)
})

test('test_close_child_components', async () => {
    await wrapper.componentVM.close_msg_send()
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.send).toBe(false)
    expect(wrapper.vm.send_msg_token).toBe("")
    expect(wrapper.vm.send_msg_key).toBe("")
    expect(wrapper.vm.send_to).toBe("")

    await wrapper.componentVM.add_closed()
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.add_app_dialog_visible).toBe(false)
})

test('turn_to_send_msg', async () => {
    await wrapper.componentVM.turn_to_send_msg("token", "key", "who")
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.send).toBe(true)
    expect(wrapper.vm.send_msg_token).toBe("token")
    expect(wrapper.vm.send_msg_key).toBe("key")
    expect(wrapper.vm.send_to).toBe("who")
})

test('show_detail', async() => {
    await wrapper.componentVM.show_detail(1)
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.app_available).toBe(true)
    expect(wrapper.vm.app_type).toBe(1)
})

test('change_nav', async () => {
    await wrapper.componentVM.change_nav()
})

test('active', async () => {
    await wrapper.componentVM.active(1)
    await wrapper.componentVM.active(0)
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.app_available).toBe(false)
    expect(wrapper.vm.app_type).toBe(0)

    await wrapper.componentVM.active(9)
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.active_index).toBe(9)
})

test('test_set_avatar_method', async () => {
    // failed
    await wrapper.setData({
        user_name: test_fail
    })
    await wrapper.componentVM.set_avatar()
    await wrapper.vm.$nextTick()
    
    // succeed
    await wrapper.setData({
        user_name: test_succeed
    })
    await wrapper.componentVM.set_avatar()
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.avatar_url).toBe(GLOBAL.url + '/THUiLoveYou!!!')
})
/*
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

test('test_set_token_method', async () => {
    await wrapper.componentVM.set_token("", {
        key: ""
    })
})
*/

test('test_get_list_method', async () => {
    // failed
    await wrapper.setData({
        user_name: test_fail
    })
    await wrapper.componentVM.get_list()
    await wrapper.vm.$nextTick()
    
    // succeed
    await wrapper.setData({
        user_name: test_succeed
    })
    await wrapper.componentVM.get_list()
    await wrapper.vm.$nextTick()
    
    expect(wrapper.vm.app_number).toBe(test_list.length)
})

test('get_shared_list', async () => {
    // failed
    await wrapper.setData({
        user_name: test_fail
    })
    await wrapper.componentVM.get_shared_list()
    await wrapper.vm.$nextTick()
    
    // succeed
    await wrapper.setData({
        user_name: test_succeed
    })
    await wrapper.componentVM.get_shared_list()
    await wrapper.vm.$nextTick()
    
    expect(wrapper.vm.shared_app_number).toBe(test_list.length)
})

test('test_new_app_method', async () => {
    // failed
    await wrapper.setData({
        user_name: test_fail
    })
    await wrapper.componentVM.new_app("", "")
    await wrapper.vm.$nextTick()
    
    // succeed
    await wrapper.setData({
        user_name: test_succeed
    })
    await wrapper.componentVM.new_app("", "")
    await wrapper.vm.$nextTick()
})


/*
test('test_edit_app_method', async () => {
    await wrapper.componentVM.edit_app("", {
        key: "",
        name: ""
    })
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.edit_app_dialog_visible).toBe(true)

})
*/

test('test_edit_method', async () => {  //
    // failed
    await wrapper.setProps({
        token: test_fail
    })
    await wrapper.componentVM.edit("", "", "", wrapper.props.token)
    await wrapper.vm.$nextTick()
    
    // succeed
    await wrapper.setProps({
        token: test_succeed
    })
    await wrapper.componentVM.edit("", "", "", wrapper.props.token)
    await wrapper.vm.$nextTick()
})
/*
test('test_show_app_token_method', async () => {
    await wrapper.componentVM.show_app_token([
        {
            content: ""
        }
    ], {
        key: ""
    })
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.token_dialog_visible).toBe(true)
})
*/