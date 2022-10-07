/*
    description:针对组件渲染的测试
    author:tshoigyr
    date:2021/03/21
*/
import { mount } from '@vue/test-utils'

// modify_dialog

import modify_dialog from "@/components/modify_dialog.vue"

test('dialog_title_modify_user', () => {
    const wrapper = mount(modify_dialog, {
        props: {
            type: 0
        }
    })
    const title = wrapper.get("el-dialog[id='test_dialog']").attributes().title
    expect(title).toBe("修改用户")
})
test('dialog_title_modify_user', () => {
    const wrapper = mount(modify_dialog, {
        props: {
            type: 1
        }
    })
    const title = wrapper.get("el-dialog[id='test_dialog']").attributes().title
    expect(title).toBe("修改角色")
})

//close
test('close', async() => {
    const wrapper = mount(modify_dialog, {
        props: {
            type: 0,
        }
    })
    await wrapper.componentVM.close();
    expect(wrapper.emitted()).toHaveProperty("close")
})

//change
test('close', async() => {
    const wrapper = mount(modify_dialog, {
        props: {
            type: 0,
        }
    })

    wrapper.get("el-transfer").trigger("change")
    expect(wrapper.emitted()).toHaveProperty("change")
})

//visible
test('visible', async() => {
    const wrapper = mount(modify_dialog, {
        props: {
            type: 0, //展示类型
            visible: false, //是否可见
            selected_user: "", //选择的用户
            selected_key: "", //表示被选中的key
            token: "", //app token
        }
    })
    await wrapper.setData({
        value: [233],
        data: [{
            key: 233,
            label: "233",
            disabled: false,
        }]
    })
    await wrapper.setProps({ visible: true })
    expect(wrapper.vm.outer_visible).toEqual(true)
    expect(wrapper.vm.data).toHaveLength(1)
})