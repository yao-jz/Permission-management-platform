/*
    author: yhy2001
    date: 2021/4/27
    state: finished
*/
import { shallowMount, mount, config } from '@vue/test-utils'
import permission_list from '@/components/permission_list.vue'
import axios from 'axios'
import flushPromises from "flush-promises"
import { createRouter, createWebHistory } from 'vue-router'

const test_fail = 'test_fail'
const test_succeed = 'test_succeed'
const token_content = 'THUiLoveYou!!!'

const test_list = [
    {
        created_time: 10,
        dead_time: 100
    },
    {
        created_time: -1,
        dead_time: -100
    }
]

jest.mock('@/utils/communication.js', () => {
    return {
        __esModule: true,
        add: jest.fn(
            (token, key, type, list) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: token == 'test_fail' || token == 'test_fail' + 'test_succeed' ? "fail" : "succeed",
                        msg: token == 'test_fail' ? "" : "out of range",
                        message: "",
                        list: [
                            {
                                created_time: 10,
                                dead_time: 100
                            },
                            {
                                created_time: -1,
                                dead_time: -100
                            }
                        ],
                    } });
                }),
        ),
        edit: jest.fn(
            (token, app_key, key, type, detail) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: token == 'test_fail' ? "fail" : "succeed",
                        tokens: [
                                {
                                    created_time: 10,
                                    dead_time: 100
                                },
                                {
                                    created_time: -1,
                                    dead_time: -100
                                }
                            ],
                        message: "",
                        msg: ""
                    } });
                }),
        ),
        remove: jest.fn(
            (token, key, key_list, type) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: token == 'test_fail' ? "fail" : "succeed",
                        tokens: [
                                {
                                    created_time: 10,
                                    dead_time: 100
                                },
                                {
                                    created_time: -1,
                                    dead_time: -100
                                }
                            ],
                        message: "",
                        msg: ""
                    } });
                }),
        ),
        show_relative: jest.fn(
            (token, app_key, type, want_type, key, from, to) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: token == 'test_fail' || token == 'test_fail' + 'test_succeed' ? "fail" : "succeed",
                        msg: token == 'test_fail' ? "" : "out of range",
                        message: "",
                        list: [
                            {
                                created_time: 10,
                                dead_time: 100
                            },
                            {
                                created_time: -1,
                                dead_time: -100
                            }
                        ],
                    } });
                }),
        ),
    };
});

const wrapper = shallowMount(permission_list, {
    global: {
        mocks: {
            $loading: jest.fn().mockReturnValue({
                close: jest.fn()
            })
        }
    }
})

test('test_open_child_components', async () => {
    await wrapper.componentVM.open_add_child({
        key: "key"
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.selected_key).toBe("key")
    expect(wrapper.vm.dialog_type).toBe(2)
    expect(wrapper.vm.add_child_dialog_visible).toBe(true)
    
    await wrapper.componentVM.add_permission_dialog()
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.selected_key).toBe("")
    expect(wrapper.vm.selected_permission).toBe("")
    expect(wrapper.vm.dialog_type).toBe(0)
    expect(wrapper.vm.add_dialog_visible).toBe(true)

    await wrapper.componentVM.open_edit({
        key: "key"
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.dialog_type).toBe(1)
    expect(wrapper.vm.add_dialog_visible).toBe(true)
})

test('test_close_child_components', async () => {
    await wrapper.componentVM.close_child_dialog()
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.add_child_dialog_visible).toBe(false)

    await wrapper.componentVM.close()
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.selected_key).toBe("")
    expect(wrapper.vm.selected_permission).toBe("")
    expect(wrapper.vm.add_dialog_visible).toBe(false)

    await wrapper.componentVM.close_list()
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.list_data).toEqual([])
    expect(wrapper.vm.list_dialog_visible).toBe(false)
})

test('test_add_child_method', async () => {
    // failed
    await wrapper.setProps({
        app_token: test_fail
    })
    await wrapper.componentVM.add_child({
        name: "",
        key: ""
    })
    await flushPromises()

    // succeeded
    await wrapper.setProps({
        app_token: test_succeed
    })
    await wrapper.componentVM.add_child({
        name: "",
        key: ""
    })
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty("update")
    let emit_update = wrapper.emitted("update")
    expect(emit_update).toHaveLength(1)
})

test('test_search_method', async () => {
    await wrapper.componentVM.search()
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty("search")
    let emit_search = wrapper.emitted("search")
    expect(emit_search).toHaveLength(1)
})

test('test_add_method', async () => {
    // failed
    await wrapper.setProps({
        app_token: test_fail
    })
    await wrapper.componentVM.add({
        name: "",
        key: ""
    }, 2)
    await flushPromises()

    // succeeded
    await wrapper.setProps({
        app_token: test_succeed
    })
    await wrapper.componentVM.add({
        name: "",
        key: ""
    }, 2)
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty("update")
    let emit_update = wrapper.emitted("update")
    expect(emit_update).toHaveLength(3)
})

test('test_open_list_method', async () => {
    // num == 3
    await wrapper.componentVM.open_list(3, {
        child_permissions: [
            {
                created_time: 1
            },
            {
                created_time: 2
            },
        ]
    })
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.list_type).toBe(3)
    //expect(wrapper.vm.list_data).toBe("child_permissions")
    expect(wrapper.vm.list_dialog_visible).toBe(true)

    // num != 3
    // failed
    await wrapper.setProps({
        app_token: test_fail + test_succeed
    })
    await wrapper.componentVM.open_list(2, {
        child_permissions: [
            {
                created_time: 1
            },
            {
                created_time: 2
            },
        ]
    })
    await flushPromises()

    await wrapper.setProps({
        app_token: test_fail
    })
    await wrapper.componentVM.open_list(2, {
        child_permissions: [
            {
                created_time: 1
            },
            {
                created_time: 2
            },
        ]
    })
    await flushPromises()

    // succeeded
    await wrapper.setProps({
        app_token: test_succeed
    })
    await wrapper.componentVM.open_list(2, {
        child_permissions: [
            {
                created_time: 1
            },
            {
                created_time: 2
            },
        ]
    })
    await flushPromises()

    expect(wrapper.vm.list_type).toBe(2)
    //expect(wrapper.vm.list_data).toEqual(test_list)
    expect(wrapper.vm.list_dialog_visible).toBe(true)
})

test('test_edit_method', async () => {
    // failed
    await wrapper.setProps({
        app_token: test_fail
    })
    await wrapper.componentVM.edit({
        name: "",
    }, 2)
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty("update")
    let emit_update = wrapper.emitted("update")
    expect(emit_update).toHaveLength(4)

    // succeeded
    await wrapper.setProps({
        app_token: test_succeed
    })
    await wrapper.componentVM.edit({
        name: "",
    }, 2)
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty("update")
    emit_update = wrapper.emitted("update")
    expect(emit_update).toHaveLength(5)
})

test('test_rm_method', async () => {
    // failed
    await wrapper.setProps({
        app_token: test_fail
    })
    await wrapper.componentVM.rm({
        name: "",
    })
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty("update")
    let emit_update = wrapper.emitted("update")
    expect(emit_update).toHaveLength(6)

    // succeeded
    await wrapper.setProps({
        app_token: test_succeed
    })
    await wrapper.componentVM.rm({
        name: "",
    })
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty("update")
    emit_update = wrapper.emitted("update")
    expect(emit_update).toHaveLength(7)
})

test('change_permission_list', async () => {
    await wrapper.setProps({
        permission_list: ["1", "2"]
    })
})
