/*
    author: yhy2001
    date: 2021/4/1
    state: finished
*/
import { mount, config } from '@vue/test-utils'
import confirm_delete from '@/components/confirm_delete.vue'
import axios from 'axios'
import flushPromises from "flush-promises"
import { createRouter, createWebHistory } from 'vue-router'

const user_name = 'kevenDurent'
const pass_word = '123456'

const wrapper = mount(confirm_delete)

test('test_method_close', async () => {
    await wrapper.componentVM.close()
    await wrapper.vm.$nextTick()

    expect(wrapper.emitted()).toHaveProperty('close')
    const emit_close = wrapper.emitted('close')
    expect(emit_close).toHaveLength(1)
})


test('test_method_confirm', async () => {
    // delete failed
    await wrapper.setData({
        user_name: user_name,
        pass_word: pass_word,
        input_content: user_name + ' nb!',
    })
    await wrapper.componentVM.confirm()
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.fail_msg).toBe("请正确输入确认标语")
    const div = wrapper.find('div[style="color: red;"]')
    expect(div.text()).toBe("请正确输入确认标语")

    // delete succeeded
    await wrapper.setProps({
        visible: 1
    })
    await wrapper.setProps({
        visible: 0
    })
    await wrapper.setProps({
        visible: 1
    })
    await wrapper.setData({
        user_name: user_name,
        pass_word: pass_word,
        input_content: "我确认要注销" + user_name + "用户"
    })
    await wrapper.componentVM.confirm()
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.fail_msg).toBe("")
    expect(div.text()).toBe("")
    expect(wrapper.emitted()).toHaveProperty('close')
    const emit_close = wrapper.emitted('close')
    expect(emit_close).toHaveLength(2)

    expect(wrapper.emitted()).toHaveProperty('confirm')
    const emit_confirm = wrapper.emitted('confirm')
    expect(emit_confirm).toHaveLength(1)
})

test('html_content', async () => {
    await wrapper.setData({
        user_name: user_name,
        pass_word: pass_word
    })
    await wrapper.vm.$nextTick()

    expect(wrapper.find('h1').text()).toContain(user_name)
})
