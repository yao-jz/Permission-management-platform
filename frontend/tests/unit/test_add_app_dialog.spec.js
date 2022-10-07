/*
    description:针对组件渲染的测试
    author:tshoigyr
    date:2021/03/21
*/
import { mount } from '@vue/test-utils'
import Input from 'element-plus/lib/el-input'


// add_app_dialog

import add_app_dialog from "@/components/add_app_dialog.vue"
import { setSyntheticLeadingComments } from 'typescript'

//test clear
const cleared = (wrapper) => {
    expect(wrapper.vm.local_state.name).toBe("")
    expect(wrapper.vm.local_state.description).toBe("")
}
const setted = (wrapper) => {
    expect(wrapper.vm.local_state.name).toBe("tshoigyr")
    expect(wrapper.vm.local_state.description).toBe("new_app")
}
const set = (form) => {
    const input0 = form[0].get("input")
    const input1 = form[2].get("input")
    input0.setValue("tshoigyr")
    input1.setValue("new_app")
}

// testing title

test('add_app_dialog_title', () => {
    const wrapper = mount(add_app_dialog, {
        props: {
            type: 0
        }
    })
    const title = wrapper.get("el-dialog").attributes().title
    expect(title).toBe("创建app")
    cleared(wrapper)
})
test('modify_app_dialog_title', () => {
    const wrapper = mount(add_app_dialog, {
        props: {
            type: 1
        }
    })
    const title = wrapper.get("el-dialog").attributes().title
    expect(title).toBe("编辑app")
    cleared(wrapper)
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

//dynamic input
test('input', async() => {
    const wrapper = mount(add_app_dialog, {
        global: {
            plugins: [Input]
        }
    })
    const form = wrapper.findAll("el-form-item")
    expect(form).toHaveLength(3)
    set(form)
    setted(wrapper)

})

//close
test('close', async() => {
    const wrapper = mount(add_app_dialog, {
        global: {
            plugins: [Input]
        }
    })
    const form = wrapper.findAll("el-form-item")
    expect(form).toHaveLength(3)
    set(form)
    setted(wrapper)

    wrapper.get("el-dialog").trigger("close")
    expect(wrapper.emitted()).toHaveProperty("close")
    cleared(wrapper)
})

//confirm add
test('confirm add', async() => {
    const wrapper = mount(add_app_dialog, {
        global: {
            plugins: [Input]
        }
    })
    const form = wrapper.findAll("el-form-item")
    expect(form).toHaveLength(3)
    set(form)
    setted(wrapper)

    wrapper.findAll("el-button")[1].trigger("click")
    expect(wrapper.emitted()).toHaveProperty("new_app")
    cleared(wrapper)
})

//confirm edit
test('confirm edit', async() => {
    const wrapper = mount(add_app_dialog, {
        global: {
            plugins: [Input]
        },
        props: {
            type: 1
        }
    })
    const form = wrapper.findAll("el-form-item")
    expect(form).toHaveLength(3)
    set(form)
    setted(wrapper)

    wrapper.findAll("el-button")[1].trigger("click")
    expect(wrapper.emitted()).toHaveProperty("edit")
    cleared(wrapper)
})

//visible
test("visible", async() => {
    const wrapper = mount(add_app_dialog, {
        props: {
            type: 2,
            state: {
                name: "233",
                description: "2333"
            }
        },
    })
    await wrapper.setProps({ visible: false })
    expect(wrapper.vm.dialog_form_visible).toBe(false)
    await wrapper.setProps({ type: 1, visible: true })
    expect(wrapper.vm.dialog_form_visible).toBe(true)
    expect(wrapper.vm.local_state.description).toBe("2333")
    expect(wrapper.vm.local_state.name).toBe("233")
})

//state
test("visible", async() => {
    const wrapper = mount(add_app_dialog, {
        props: {
            type: 2,
            state: {
                name: "0",
                description: "00"
            }
        },
    })
    await wrapper.setProps({ state: { name: "233", description: "2333" } })
    expect(wrapper.vm.local_state.description).toBe("2333")
    expect(wrapper.vm.local_state.name).toBe("233")
})