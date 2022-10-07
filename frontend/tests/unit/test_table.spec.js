/*
    author: yhy2001
    date: 2021/4/7
    state: finished
*/
import { shallowMount, mount, config } from '@vue/test-utils'
import table from '@/components/table.vue'
import axios from 'axios'
import flushPromises from "flush-promises"
import { createRouter, createWebHistory } from 'vue-router'

const test_fail = 'test_fail'
const test_succeed = 'test_succeed'

const list = [
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
        get_total: jest.fn(
            (token, type) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: token == 'test_fail' ? "fail" : "succeed",
                        message: "",
                        total: 10
                    } });
                }),
        ),
        search_content: jest.fn(
            (token, content, type, from, to) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: token == 'test_fail' ? "fail" : "succeed",
                        message: "",
                        total: 10,
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


const wrapper = shallowMount(table)

test('html_content', async () => {
    // 非搜索结果
    await wrapper.setData({
        table_type: 0
    })
    await wrapper.vm.$nextTick()
    await wrapper.setProps({
        type: 1
    })
    await wrapper.setProps({
        type: 2
    })
    await wrapper.setProps({
        type: 0
    })
    await flushPromises()

    // 搜索结果
    await wrapper.setData({
        table_type: 1
    })
    await wrapper.setProps({
        type: 0
    })
    await flushPromises()
})

test('test_method_update_data', async () => {
    // get_total fail
    await wrapper.setData({
        total_item: 0,
        table_type: 0
    })
    await wrapper.setProps({
        token: test_fail
    })
    await wrapper.componentVM.update_data()
    await flushPromises()

    expect(wrapper.vm.total_item).toBe(0)

    // get_total succeed
    await wrapper.setProps({
        token: test_succeed
    })
    await wrapper.componentVM.update_data()
    await flushPromises()

    expect(wrapper.vm.total_item).toBe(10)

})

test('test_method_change_page', async () => {
    // 非搜索结果
    // fail
    await wrapper.setProps({
        token: test_fail
    })
    await wrapper.setData({
        table_type: 0
    })
    await wrapper.componentVM.change_page(2)
    await flushPromises()

    expect(wrapper.vm.current_page).toBe(1)

    // succeed
    await wrapper.setProps({
        token: test_succeed
    })
    await wrapper.componentVM.change_page(2)
    await flushPromises()

    expect(wrapper.vm.current_page).toBe(2)


    // 搜索结果
    // fail
    await wrapper.setProps({
        token: test_fail
    })
    await wrapper.setData({
        table_type: 1
    })
    await wrapper.componentVM.change_page(2)
    await flushPromises()

    expect(wrapper.vm.current_page).toBe(1)

    // succeed
    await wrapper.setProps({
        token: test_succeed
    })
    await wrapper.componentVM.change_page(2)
    await flushPromises()

    //expect(wrapper.vm.list_data).toEqual(list)
})

test('test_method_search', async () => {
    const from = 0
    const to = 100
    // fail
    await wrapper.setData({
        total_item: 0
    })
    await wrapper.setProps({
        token: test_fail
    })
    await wrapper.componentVM.search("", from, to)
    await flushPromises()

    expect(wrapper.vm.total_item).toBe(0)

    // succeed
    await wrapper.setProps({
        token: test_succeed
    })
    await wrapper.componentVM.search("", from, to)
    await flushPromises()

    expect(wrapper.vm.total_item).toEqual(10)
    //expect(wrapper.vm.list_data).toEqual(list)
    expect(wrapper.vm.search_from).toEqual(from)
})
