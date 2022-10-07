/*
    author: yhy2001
    date: 2021/4/6
    state: semi-finished
*/
import { mount, config } from '@vue/test-utils'
import select_dialog from '@/components/select_dialog.vue'
import axios from 'axios'
import flushPromises from "flush-promises"

const test_fail = 'test_fail'
const test_succeed = 'test_succeed'

let list = [
    {
        key: '1',
        name: '1',
        child_permissions: []
    },
    {
        key: '1',
        name: '1',
        child_permissions: []
    }
]

jest.mock('@/utils/communication.js', () => {
    return {
        __esModule: true,
        get_list: jest.fn(
            (token, type, from, to) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: token == 'test_fail' ? "fail" : "succeed",
                        message: "",
                        list: token == 'test_fail' ? [] : [
                            {
                                key: '1',
                                name: '1',
                                child_permissions: []
                            },
                            {
                                key: '1',
                                name: '1',
                                child_permissions: []
                            }
                        ]
                    } });
                }),
        ),
        show_relative: jest.fn(
            (token, type, want_type, key, from, to) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: token == 'test_fail' ? "fail" : "succeed",
                        message: "",
                        list: token == 'test_fail' ? [] : [
                            {
                                key: '1',
                                name: '1',
                                child_permissions: []
                            },
                            {
                                key: '1',
                                name: '1',
                                child_permissions: []
                            }
                        ]
                    } });
                }),
        ),
        attach: jest.fn(
            (token, user_key_list, role_key_list, permission_key_list) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: "succeed",
                        message: "",
                    } });
                }),
        ),
        detach: jest.fn(
            (token, user_key_list, role_key_list, permission_key_list) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: "succeed",
                        message: "",
                    } });
                }),
        ),
    };
});

const $refs = {
    tree: {
        filter: jest.fn()
    }
}
/*
const wrapper = mount(select_dialog, {
    global: {
        mocks: {
            $refs
        }
    }
})
*/
const wrapper = mount(select_dialog)

test('test_method_close', async () => {
    await wrapper.componentVM.close()
    await wrapper.vm.$nextTick()

    expect(wrapper.emitted()).toHaveProperty('close')
    let emit_close = wrapper.emitted('close')
    expect(emit_close).toHaveLength(1)
})

test('html_content', async() => {
    // html content
    await wrapper.setProps({
        type: 0
    })
    await wrapper.vm.$nextTick()

    const el_dialog = wrapper.find('el-dialog')
    expect(el_dialog.html()).toContain("操作用户名")
    expect(el_dialog.attributes().title).toBe("编辑用户")

    await wrapper.setProps({
        type: 1
    })
    await wrapper.vm.$nextTick()
    
    expect(el_dialog.html()).toContain("操作角色名")
    expect(el_dialog.attributes().title).toBe("编辑角色")

    // change visible
    await wrapper.setProps({
        token: test_succeed,
        visible: true
    })
    await wrapper.setProps({
        token: test_fail,
        visible: false
    })

    // change filter_text
    // 未解决！！！
    /*
    await wrapper.setData({
        filter_text: "haha"
    })
    await wrapper.vm.$nextTick()
    await flushPromises()

    expect($refs.tree.filter).toHaveBeenCalledTimes(1)
    */
})

test('test_method_filter_node', async () => {
    let f
    // empty value
    f = await wrapper.componentVM.filter_node('', list[0]);
    expect(f).toBe(true)

    // value in data
    f = await wrapper.componentVM.filter_node('1', list[0]);
    expect(f).toBe(true)

    // value not in data
    f = await wrapper.componentVM.filter_node('2', list[0]);
    expect(f).toBe(false)
})

test('test_method_handle_check_change', async () => {
    // detach
    await wrapper.componentVM.handle_check_change(list[1], false)

    // attach
    await wrapper.componentVM.handle_check_change(list[1], true)
    
})