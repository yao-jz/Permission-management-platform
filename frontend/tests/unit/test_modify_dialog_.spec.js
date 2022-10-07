/*
    author: yhy2001
    date: 2021/4/1
    state: finished
*/
import { mount, config } from '@vue/test-utils'
import modify_dialog from '@/components/modify_dialog.vue'
import axios from 'axios'
import flushPromises from "flush-promises"
import { createRouter, createWebHistory } from 'vue-router'

const selected_name = 'kevenDurent'
const selected_key = '1'

const wrapper = mount(modify_dialog, {
    props: {
        type: 0,
        visible: false,
        selected_user: selected_name,
        selected_key: selected_key
    }
})

const test_fail = 'test_fail'
const test_succeed = 'test_succeed'

jest.mock('@/utils/communication.js', () => {
    return {
        __esModule: true,
        show_relative: jest.fn(
            (token, type, want_type, key, from, to) =>
                new Promise((resolve, reject) => {
                    if (token == 'test_fail')
                        resolve({ data: {
                            status: token == 'test_fail' ? "fail" : "succeed",
                            message: "",
                        } });
                    else
                        resolve({ data: {
                            status: token == 'test_fail' ? "fail" : "succeed",
                            message: "",
                            list: [
                                {
                                    key: '1',
                                },
                                {
                                    key: '1',
                                }
                            ]
                        } });
                }),
        ),
        get_list: jest.fn(
            (token, type, from, to) =>
                new Promise((resolve, reject) => {
                    if (token == 'test_fail')
                        resolve({ data: {
                            status: token == 'test_fail' ? "fail" : "succeed",
                            message: "",
                        } });
                    else
                        resolve({ data: {
                            status: token == 'test_fail' ? "fail" : "succeed",
                            message: "",
                            list: token == 'test_fail' ? [] : [
                                {
                                    key: '1',
                                    name: '1',
                                    child_permissions: [],
                                    created_time: '2021-4-7'
                                },
                                {
                                    key: '1',
                                    name: '1',
                                    child_permissions: [],
                                    created_time: '2021-4-8'
                                }
                            ]
                        } });
                }),
        ),
    };
});

test('modify_visible', async () => {
    await wrapper.setProps({
        token: test_succeed
    })
    await wrapper.vm.$nextTick()
    await wrapper.setProps({
        visible: true,
    })
    await wrapper.vm.$nextTick()
    await wrapper.setProps({
        visible: false,
    })
    // empty list
    await wrapper.setProps({
        token: test_fail
    })
    await wrapper.vm.$nextTick()
    await wrapper.setProps({
        visible: true,
    })
    await wrapper.vm.$nextTick()
    await wrapper.setProps({
        visible: false,
    })
    await wrapper.vm.$nextTick()

    const el_dialog = wrapper.find('el-dialog[id="test_dialog"]')
    expect(el_dialog.attributes().title).toBe("修改用户")
    expect(el_dialog.attributes().modelvalue).toBe("false")
    expect(el_dialog.isVisible()).toBe(true)
    expect(el_dialog.text()).toContain(selected_name)

    const el_transfer = wrapper.find('el-transfer')
    expect(el_transfer.attributes().titles).toContain('全部角色')
    expect(el_transfer.attributes().titles).toContain('已有角色')
})

test('test_method_modify', async () => {
    await wrapper.componentVM.modify(1, "", [])
    expect(wrapper.emitted()).toHaveProperty("change")
    const emit_change = wrapper.emitted("change")
    expect(emit_change).toHaveLength(1)
    expect(emit_change[0]).toEqual([1, '', []])
})

test('test_method_close', async () => {
    await wrapper.componentVM.close()
    expect(wrapper.emitted()).toHaveProperty("close")
    const emit_close = wrapper.emitted("close")
    expect(emit_close).toHaveLength(1)
})

test('change_type', async () => {
    const el_dialog = wrapper.find('el-dialog[id="test_dialog"]')
    const el_transfer = wrapper.find('el-transfer')
    await wrapper.setProps({
        type: 1
    })
    await wrapper.setData({
        outer_visible: false
    })
    await wrapper.vm.$nextTick()

    expect(el_dialog.attributes().title).toBe("修改角色")
    expect(el_dialog.attributes().modelvalue).toEqual("false")
    //expect(el_dialog.isVisible()).toBe(false)
    expect(el_dialog.text()).toContain(selected_name)

    expect(el_transfer.attributes().titles).toContain('全部权限')
    expect(el_transfer.attributes().titles).toContain('已有权限')

})