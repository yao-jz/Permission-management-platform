/*
    author: yhy2001
    date: 2021/4/1
    state: semi-finished
*/
import { mount, config } from '@vue/test-utils'
import modify_token_dialog from '@/components/modify_token_dialog.vue'
import axios from 'axios'
import flushPromises from "flush-promises"
import { createRouter, createWebHistory } from 'vue-router'

const wrapper = mount(modify_token_dialog, {
    props: {
        type: 0,
        visible: false,
        selected_token: "",
    }
})

test('test_method_close', async () => {
    await wrapper.componentVM.close()
    console.log(wrapper.html())
    //wrapper.findAll('el-button')[0].trigger('click')
    expect(wrapper.emitted()).toHaveProperty("update")
    const emit_update = wrapper.emitted("update")
    expect(emit_update).toHaveLength(1)

    expect(wrapper.emitted()).toHaveProperty("close")
    const emit_close = wrapper.emitted("close")
    expect(emit_close).toHaveLength(1)
})

test('test_method_confirm', async () => {
    await wrapper.componentVM.confirm()
    //wrapper.findAll('el-button')[1].trigger('click')
    expect(wrapper.emitted()).toHaveProperty("close")
    const emit_close = wrapper.emitted("close")
    expect(emit_close).toHaveLength(2)
})

test('html_content', async () => {
    //新增token
    await wrapper.setProps({
        visible: true
    })
    await wrapper.setData({
        value: 100
    })
    await wrapper.vm.$nextTick()

    console.log(wrapper.html())
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
