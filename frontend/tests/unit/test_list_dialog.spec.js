/*
    description:针对组件渲染的测试
    author:tshoigyr
    date:2021/03/21
*/
import { mount } from '@vue/test-utils'

// add_dialog

import list_dialog from "@/components/list_dialog.vue"

// testing title
test('user_list_dialog_title', () => {
    const wrapper = mount(list_dialog, {
        props: {
            type: 0,
            visible: false,
            list_data: []
        }
    })
    const title = wrapper.get("el-dialog").attributes().title
    expect(title).toBe("用户")
})
test('role_list_dialog_title', () => {
    const wrapper = mount(list_dialog, {
        props: {
            type: 1,
            visible: false,
            list_data: []
        }
    })
    const title = wrapper.get("el-dialog").attributes().title
    expect(title).toBe("角色")
})
test('permission_list_dialog_title', () => {
    const wrapper = mount(list_dialog, {
        props: {
            type: 2,
            visible: false,
            list_data: []
        }
    })
    const title = wrapper.get("el-dialog").attributes().title
    expect(title).toBe("权限")
})
test('subpermission_list_dialog_title', () => {
    const wrapper = mount(list_dialog, {
        props: {
            type: 3,
            visible: false,
            list_data: []
        }
    })
    const title = wrapper.get("el-dialog").attributes().title
    expect(title).toBe("子权限")
})

//close
test('close', async() => {
    const wrapper = mount(list_dialog, {
        props: {
            type: 0,
            visible: false,
            list_data: []
        }
    })

    wrapper.get(".close_button").trigger("click")
    expect(wrapper.emitted()).toHaveProperty("close")

    await wrapper.vm.close()
    expect(wrapper.emitted()).toHaveProperty("close")
})

//visible
test('close', async() => {
    const wrapper = mount(list_dialog, {
        props: {
            type: 0,
            visible: false,
            list_data: []
        }
    })

    await wrapper.setProps({ visible: true })
    expect(wrapper.vm.dialog_table_visible).toBe(true)
})