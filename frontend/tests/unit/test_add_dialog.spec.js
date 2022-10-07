/*
    description:针对组件渲染的测试
    author:tshoigyr
    date:2021/03/21
*/
import { mount } from '@vue/test-utils'
import Input from 'element-plus/lib/el-input'
import flushPromises from 'flush-promises'


// add_dialog

import add_dialog from "@/components/add_dialog.vue"
import { json } from 'body-parser'
import { reject, resolve } from 'q'

// testing title

jest.mock('@/utils/communication.js', () => {
    return {
        check_key: jest.fn((app_token, app_key, type, key) => {
            return new Promise((resolve, reject) => {
                return resolve({
                    data: {
                        status: key == "correct" ? "succeed" : "failed",
                        msg: key == "correct" ? "" : key
                    }
                })
            })
        })
    }
})

test('dialog_title_add_user', () => {
    const wrapper = mount(add_dialog, {
        props: {
            dialog_type: 0,
            type: 0
        }
    })
    const title = wrapper.get("el-dialog").attributes().title
    expect(title).toBe("添加用户")
    expect(wrapper.vm.state.name).toBe("")
    expect(wrapper.vm.state.created_time).toBe("")
    expect(wrapper.vm.state.key).toBe("")
    expect(wrapper.vm.key_valid).toBe(false)
    expect(wrapper.vm.name_valid).toBe(false)
})
test('dialog_title_add_role', () => {
    const wrapper = mount(add_dialog, {
        props: {
            dialog_type: 0,
            type: 1
        }
    })
    const title = wrapper.get("el-dialog").attributes().title
    expect(title).toBe("添加角色")
    expect(wrapper.vm.state.name).toBe("")
    expect(wrapper.vm.state.created_time).toBe("")
    expect(wrapper.vm.state.key).toBe("")
    expect(wrapper.vm.key_valid).toBe(false)
    expect(wrapper.vm.name_valid).toBe(false)
})
test('dialog_title_add_permission', () => {
    const wrapper = mount(add_dialog, {
        props: {
            dialog_type: 0,
            type: 2
        }
    })
    const title = wrapper.get("el-dialog").attributes().title
    expect(title).toBe("添加权限")
    expect(wrapper.vm.state.name).toBe("")
    expect(wrapper.vm.state.created_time).toBe("")
    expect(wrapper.vm.state.key).toBe("")
    expect(wrapper.vm.key_valid).toBe(false)
    expect(wrapper.vm.name_valid).toBe(false)
})
test('dialog_title_edit_user', () => {
    const wrapper = mount(add_dialog, {
        props: {
            dialog_type: 1,
            type: 0
        }
    })
    const title = wrapper.get("el-dialog").attributes().title
    expect(title).toBe("编辑用户")
    expect(wrapper.vm.state.name).toBe("")
    expect(wrapper.vm.state.created_time).toBe("")
    expect(wrapper.vm.state.key).toBe("")
    expect(wrapper.vm.key_valid).toBe(false)
    expect(wrapper.vm.name_valid).toBe(false)
})
test('dialog_title_edit_role', () => {
    const wrapper = mount(add_dialog, {
        props: {
            dialog_type: 1,
            type: 1
        }
    })
    const title = wrapper.get("el-dialog").attributes().title
    expect(title).toBe("编辑角色")
    expect(wrapper.vm.state.name).toBe("")
    expect(wrapper.vm.state.created_time).toBe("")
    expect(wrapper.vm.state.key).toBe("")
    expect(wrapper.vm.key_valid).toBe(false)
    expect(wrapper.vm.name_valid).toBe(false)
})
test('dialog_title_edit_permission', () => {
    const wrapper = mount(add_dialog, {
        props: {
            dialog_type: 1,
            type: 2
        }
    })
    const title = wrapper.get("el-dialog").attributes().title
    expect(title).toBe("编辑权限")
    expect(wrapper.vm.state.name).toBe("")
    expect(wrapper.vm.state.created_time).toBe("")
    expect(wrapper.vm.state.key).toBe("")
    expect(wrapper.vm.key_valid).toBe(false)
    expect(wrapper.vm.name_valid).toBe(false)
})
test('dialog_title_add_sub_permisson', () => {
    const wrapper = mount(add_dialog, {
        props: {
            dialog_type: 2,
            type: 2
        }
    })
    const title = wrapper.get("el-dialog").attributes().title
    expect(title).toBe("添加子权限")
    expect(wrapper.vm.state.name).toBe("")
    expect(wrapper.vm.state.created_time).toBe("")
    expect(wrapper.vm.state.key).toBe("")
    expect(wrapper.vm.key_valid).toBe(false)
    expect(wrapper.vm.name_valid).toBe(false)
})

//testing form-item
test('form-item_user', () => {
    const wrapper = mount(add_dialog, {
        props: {
            dialog_type: 0,
            type: 0
        }
    })
    const formlist = wrapper.findAll("el-form-item")
    expect(formlist).toHaveLength(2)
    expect(formlist[0].attributes().label).toBe("用户姓名")
    expect(formlist[1].attributes().label).toBe("key")
})
test('form-item_role', () => {
    const wrapper = mount(add_dialog, {
        props: {
            dialog_type: 0,
            type: 1
        }
    })
    const formlist = wrapper.findAll("el-form-item")
    expect(formlist).toHaveLength(2)
    expect(formlist[0].attributes().label).toBe("角色名称")
    expect(formlist[1].attributes().label).toBe("key")
})
test('form-item_permission', () => {
    const wrapper = mount(add_dialog, {
        props: {
            dialog_type: 0,
            type: 2
        }
    })
    const formlist = wrapper.findAll("el-form-item")
    expect(formlist).toHaveLength(2)
    expect(formlist[0].attributes().label).toBe("权限名称")
    expect(formlist[1].attributes().label).toBe("key")
})

//dynamic input
test('input', async() => {
    const wrapper = mount(add_dialog, {
        props: {
            type: 0,
            dialog_type: 0
        },
        global: {
            plugins: [Input]
        }
    })
    const form = wrapper.findAll("el-form-item")
    expect(form).toHaveLength(2)
    const input0 = form[0].get("input")
    const input1 = form[1].get("input")
    input0.setValue("tshoigyr")
    input1.setValue("new_app")
    expect(wrapper.vm.state.name).toBe("tshoigyr")
    expect(wrapper.vm.state.key).toBe("new_app")

})

//close
test('close', async() => {
    const wrapper = mount(add_dialog, {
        props: {
            type: 0,
            dialog_type: 0
        },
        global: {
            plugins: [Input]
        }
    })
    const form = wrapper.findAll("el-form-item")
    expect(form).toHaveLength(2)
    const input0 = form[0].get("input")
    const input1 = form[1].get("input")
    input0.setValue("tshoigyr")
    input1.setValue("new_app")
    expect(wrapper.vm.state.name).toBe("tshoigyr")
    expect(wrapper.vm.state.key).toBe("new_app")

    wrapper.get("el-dialog").trigger("close")
    expect(wrapper.emitted()).toHaveProperty("close")
    expect(wrapper.vm.state.name).toBe("")
    expect(wrapper.vm.state.key).toBe("")
})

//confirm add
test('confirm add', async() => {
    const wrapper = mount(add_dialog, {
        props: {
            type: 0,
            dialog_type: 0
        },
        global: {
            plugins: [Input]
        }
    })
    const form = wrapper.findAll("el-form-item")
    expect(form).toHaveLength(2)
    const input0 = form[0].get("input")
    const input1 = form[1].get("input")
    input0.setValue("tshoigyr")
    input1.setValue("new_app")
    expect(wrapper.vm.state.name).toBe("tshoigyr")
    expect(wrapper.vm.state.key).toBe("new_app")

    wrapper.find("el-button[id='test_button_1']").trigger("click")
    expect(wrapper.emitted()).toHaveProperty("new_add")
    expect(wrapper.vm.state.name).toBe("")
    expect(wrapper.vm.state.key).toBe("")
})
test('confirm add', async() => {
    const wrapper = mount(add_dialog, {
        props: {
            type: 2,
            dialog_type: 2
        },
        global: {
            plugins: [Input]
        }
    })
    const form = wrapper.findAll("el-form-item")
    expect(form).toHaveLength(2)
    const input0 = form[0].get("input")
    const input1 = form[1].get("input")
    input0.setValue("tshoigyr")
    input1.setValue("new_app")
    expect(wrapper.vm.state.name).toBe("tshoigyr")
    expect(wrapper.vm.state.key).toBe("new_app")

    wrapper.find("el-button[id='test_button_1']").trigger("click")
    expect(wrapper.emitted()).toHaveProperty("new_add")
    expect(wrapper.vm.state.name).toBe("")
    expect(wrapper.vm.state.key).toBe("")
})

//confirm edit
test('confirm edit', async() => {
    const wrapper = mount(add_dialog, {
        props: {
            type: 1,
            dialog_type: 1
        },
        global: {
            plugins: [Input]
        }
    })
    const form = wrapper.findAll("el-form-item")
    expect(form).toHaveLength(2)
    const input0 = form[0].get("input")
    const input1 = form[1].get("input")
    input0.setValue("tshoigyr")
    input1.setValue("new_app")
    expect(wrapper.vm.state.name).toBe("tshoigyr")
    expect(wrapper.vm.state.key).toBe("new_app")

    wrapper.find("el-button[id='test_button_1']").trigger("click")
    expect(wrapper.emitted()).toHaveProperty("new_edit")
    expect(wrapper.vm.state.name).toBe("")
    expect(wrapper.vm.state.key).toBe("")
})

//test check_key
test("check_key", async() => {
    const wrapper = mount(add_dialog, {
        props: {
            type: 1,
            dialog_type: 1
        },
    })
    const input = wrapper.findAll(".key")[0]
    
        //correct
    await wrapper.setData({ state: { key: "correct" } })
    await wrapper.vm.$nextTick()
    await input.trigger("blur")
    await flushPromises()
    expect(wrapper.vm.key_valid).toBe(true)
        //wrong
    await wrapper.setData({ state: { key: "wrong" } })
    await wrapper.vm.$nextTick()
    await input.trigger("blur")
    await flushPromises()
    expect(wrapper.vm.key_valid).toBe(false)
    expect(wrapper.vm.key_wrong_message).toBe("wrong")
    
        //empty
    await wrapper.setData({ state: { key: "" }, old_key: "correct" })
    await wrapper.vm.$nextTick()
    await input.trigger("blur")
    await flushPromises()
    expect(wrapper.vm.key_valid).toBe(false)
    expect(wrapper.vm.key_wrong_message).toBe("请输入你的key")
    
    //unchanged
    wrapper.setData({ state: { key: "correct" }, old_key: "correct" })
    await input.trigger("blur")
    await flushPromises()
    expect(wrapper.vm.key_valid).toBe(true)
})

//test visible
test("visible", async() => {
    const wrapper = mount(add_dialog, {
        props: {
            type: 1,
            dialog_type: 2,
            selected_name: "myname",
            selected_key: "mykey"
        },
    })
    await wrapper.setProps({ visible: false })
    expect(wrapper.vm.outer_visible).toBe(false)
    await wrapper.setProps({ dialog_type: 1, visible: true })
    expect(wrapper.vm.outer_visible).toBe(true)
    expect(wrapper.vm.key_valid).toBe(true)
    expect(wrapper.vm.state.key).toBe("mykey")
    expect(wrapper.vm.state.name).toBe("myname")
    expect(wrapper.vm.old_key).toBe("mykey")
})
