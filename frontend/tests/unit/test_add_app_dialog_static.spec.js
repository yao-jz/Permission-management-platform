/*
    description:针对组件渲染的测试
    author:tshoigyr
    date:2021/03/21
*/
import { mount, config } from '@vue/test-utils'
import ElementPlus from 'element-plus'

config.plugins.VueWrapper.install()

// add_app_dialog

import add_app_dialog from "@/components/add_app_dialog.vue"

// testing title

test('add_app_dialog_title', () => {
    const wrapper = mount(add_app_dialog, {
        props: {
            type: 0
        }
    })
    const title = wrapper.get("el-dialog").attributes().title
    expect(title).toBe("创建app")
})
test('modify_app_dialog_title', () => {
    const wrapper = mount(add_app_dialog, {
        props: {
            type: 1
        }
    })
    const title = wrapper.get("el-dialog").attributes().title
    expect(title).toBe("编辑app")
})

//testing form-item

test('form-item', () => {
    const wrapper = mount(add_app_dialog)
    const form = wrapper.findAll("el-form-item")
    expect(form).toHaveLength(3)
    expect(form[0].attributes().label).toBe("app名称")
    expect(form[1].attributes().label).toBe("app key")
    expect(form[2].attributes().label).toBe("app描述")
})
test('input-static', () => {
    const wrapper = mount(add_app_dialog)
    const form = wrapper.findAll("el-form-item")
    expect(form).toHaveLength(3)
    const input0 = form[0].get("el-input")
    const input1 = form[1].get("el-input")
    expect(input0.attributes().autocomplete).toBe("off")
    expect(input1.attributes().autocomplete).toBe("off")
})
