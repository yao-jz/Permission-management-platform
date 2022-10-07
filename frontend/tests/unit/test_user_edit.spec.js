/*
    author: yhy2001
    date: 2021/4/1
    state: semi-finished
*/
import { shallowMount, mount, config } from '@vue/test-utils'
import user_edit from '@/components/user_edit.vue'
import axios from 'axios'
import flushPromises from "flush-promises"
import { createRouter, createWebHistory } from 'vue-router'

const user_name = 'kevenDurant'
const pass_word = '123456'

const $message = {
    state: {
      count: 25
    },
    commit: jest.fn(),
    error: jest.fn(),
  }

const wrapper = mount(user_edit, {
    global: {
        mocks: {
            $message
        }
    }
})
/*
test('test_method_before_avatar_upload', async () => {
    // 该方法已删除
    // not JPG and file too large
    //expect(wrapper.getComponent(Foo).vm.msg).toBe('hello world')
    let file = "C:\\Users\\asus\\Desktop\\Math.txt"
    await wrapper.componentVM.before_avatar_upload(file)
    expect($message.error).toHaveBeenCalledTimes(2)
    file = "@\\..\\public\\111.jpg"
    await wrapper.componentVM.before_avatar_upload(file)
    expect($message.error).toHaveBeenCalledTimes(4)
})
*/

test('test_method_handle_avatar_success', async () => {
    // 未解决！！！
    /*
    let file = {
        raw: "@\\..\\public\\111.jpg"
    }
    wrapper.componentVM.handle_avatar_success(0, file)
    */
})

test('test_method_close', async () => {
    await wrapper.setProps({
        visible: true
    })
    await wrapper.setProps({
        visible: false
    })
    await wrapper.componentVM.close()
    await wrapper.vm.$nextTick()

    expect(wrapper.emitted()).toHaveProperty('close')
    let emit_close = wrapper.emitted('close')
    expect(emit_close).toHaveLength(1)
})

const test_fail = 'test_fail'
const test_succeed = 'test_succeed'

jest.mock('@/utils/communication.js', () => {
    return {
        __esModule: true,
        edit_user: jest.fn(
            (old_user_name, old_password, new_user_name, new_password) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: new_user_name == 'test_fail' || new_password == 'test_fail' ? "fail" : "succeed",
                        message: ""
                    } });
                }),
        ),
    };
});

test('test_method_confirm', async() => {
    // empty password and old_user_name == new_user_name
    await wrapper.setData({
        old_user_name: 'yhy'
    })
    await wrapper.setData({
        form: {
            user_name: wrapper.vm.old_user_name,
            pass_word: ""
        }
    })
    await wrapper.componentVM.confirm()
    await wrapper.vm.$nextTick()

    let emit_close = wrapper.emitted('close')
    expect(emit_close).toHaveLength(2)

    // empty new_user_name
    await wrapper.setData({
        form: {
            user_name: ''
        }
    })
    await wrapper.componentVM.confirm()
    await wrapper.vm.$nextTick()

    expect(emit_close).toHaveLength(3)

    // failed_user_edit
    await wrapper.setData({
        form: {
            user_name: test_fail
        }
    })
    await wrapper.componentVM.confirm()
    await flushPromises()

    // succeeded_user_edit
    await wrapper.setData({
        form: {
            user_name: test_succeed
        }
    })
    await wrapper.componentVM.confirm()
    await flushPromises()

    expect(emit_close).toHaveLength(4)


    // failed_user_edit with new_pass_word
    await wrapper.setData({
        form: {
            pass_word: test_fail
        }
    })
    await wrapper.componentVM.confirm()
    await flushPromises()

    // succeeded_user_edit with new_pass_word
    await wrapper.setData({
        form: {
            pass_word: test_succeed
        }
    })
    await wrapper.componentVM.confirm()
    await flushPromises()

    expect(emit_close).toHaveLength(5)

})
