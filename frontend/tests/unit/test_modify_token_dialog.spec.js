/*
    author: yhy2001
    date: 2021/4/1
    state: finished
*/
import { mount, config } from '@vue/test-utils'
import modify_token_dialog from '@/components/modify_token_dialog.vue'
import axios from 'axios'
import flushPromises from "flush-promises"
import { createRouter, createWebHistory } from 'vue-router'

const test_fail = 'test_fail'
const test_succeed = 'test_succeed'

jest.mock('@/utils/communication.js', () => {
    return {
        __esModule: true,
        add_token: jest.fn(
            (token, list, user_name, pass_word) =>
            new Promise((resolve, reject) => {
                resolve({
                    data: {
                        status: user_name == 'test_fail' || pass_word == 'test_fail' ? "fail" : "succeed",
                        message: ""
                    }
                });
            }),
        ),
        change_token: jest.fn(
            (list, user_name, pass_word) =>
            new Promise((resolve, reject) => {
                resolve({
                    data: {
                        status: user_name == 'test_fail' || pass_word == 'test_fail' || list[0].app_token == 'test_fail' ? "fail" : "succeed",
                        message: "",
                        msg: list[0].app_token == 'test_succeed' ? "" : "???" 
                    }
                });
            }),
        ),
    };
});

const wrapper = mount(modify_token_dialog, {
    props: {
        type: 0,
        visible: false,
        selected_token: "",
    }
})

test('test_method_close', async() => {
    await wrapper.componentVM.close()
    //wrapper.findAll('el-button')[0].trigger('click')
    expect(wrapper.emitted()).toHaveProperty("update")
    const emit_update = wrapper.emitted("update")
    expect(emit_update).toHaveLength(1)

    expect(wrapper.emitted()).toHaveProperty("close")
    const emit_close = wrapper.emitted("close")
    expect(emit_close).toHaveLength(1)
})

test('test_method_confirm', async() => {
    // add_token failed
    await wrapper.setData({
        user_name: test_fail,
        pass_word: test_fail
    })
    await wrapper.componentVM.confirm()
        //wrapper.findAll('el-button')[1].trigger('click')
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty("close")
    const emit_close = wrapper.emitted("close")
    expect(emit_close).toHaveLength(2)

    // change_token failed
    await wrapper.setProps({
        type: 1
    })
    await wrapper.componentVM.confirm()
    await flushPromises()

    expect(emit_close).toHaveLength(3)

    // change_token succeed
    await wrapper.setData({
        user_name: test_succeed,
        pass_word: test_succeed
    })
    await wrapper.componentVM.confirm()
        //wrapper.findAll('el-button')[1].trigger('click')
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty("update")
    const emit_update = wrapper.emitted("update")
    expect(emit_update).toHaveLength(4)
    expect(emit_close).toHaveLength(4)

    // add_token succeed
    await wrapper.setProps({
        type: 0
    })
    await wrapper.componentVM.confirm()
    await flushPromises()

    expect(emit_update).toHaveLength(5)
    expect(emit_close).toHaveLength(5)

})

test('html_content', async() => {
    //新增token
    await wrapper.setProps({
        visible: true,
        type: 0
    })
    await wrapper.setData({
        value: 100
    })
    await wrapper.vm.$nextTick()

    const el_dialog = wrapper.find('el-dialog')

    expect(el_dialog.attributes().title).toBe("新增token")
    expect(el_dialog.attributes().modelvalue).toBe("true")
    expect(el_dialog.isVisible()).toBe(true)
    expect(el_dialog.text()).toContain('token')

    const el_slider = wrapper.find('el-slider')
    expect(el_slider.attributes().modelvalue).toEqual("100")

    //编辑token
    await wrapper.setProps({
        visible: false,
        type: 1
    })
    await wrapper.vm.$nextTick()

    expect(el_dialog.attributes().title).toBe("编辑token")
    expect(el_dialog.attributes().modelvalue).toBe("false")
        //expect(el_dialog.isVisible()).toBe(false)
    expect(el_dialog.text()).toContain('token')

    //expect(el_slider.attributes().modelvalue).toEqual("100")
})

test('error_type', async() => {
    await wrapper.setProps({
        visible: false,
        type: 'klsadnfalf'
    })
    await wrapper.vm.$nextTick()
    await wrapper.componentVM.confirm()
})


test('infinite', async () => {
    await wrapper.setProps({
        selected_token: test_fail
    })
    await wrapper.vm.$nextTick()
    await wrapper.componentVM.infinite()
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty("close")
    let emit_close = wrapper.emitted("close")
    expect(emit_close).toHaveLength(7)
    expect(wrapper.emitted()).toHaveProperty("update")
    let emit_update = wrapper.emitted("update")
    expect(emit_update).toHaveLength(6)

    await wrapper.setProps({
        app_token: test_succeed
    })
    await wrapper.vm.$nextTick()
    await wrapper.componentVM.infinite()
    await flushPromises()

    expect(emit_close).toHaveLength(8)
    expect(emit_update).toHaveLength(7)

    await wrapper.setProps({
        app_token: test_succeed + '?'
    })
    await wrapper.vm.$nextTick()
    await wrapper.componentVM.infinite()
    await flushPromises()

    expect(emit_close).toHaveLength(9)
    expect(emit_update).toHaveLength(8)
})
