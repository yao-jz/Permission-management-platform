/*
    author: yhy2001
    date: 2021/4/27
    state: finished
*/
import { shallowMount, mount, config } from '@vue/test-utils'
import createLocalVue from '@vue/test-utils'
import token_detail from '@/components/token_detail.vue'
import axios from 'axios'
import flushPromises from "flush-promises"
import { createRouter, createWebHistory } from 'vue-router'
import { delete_token, get_app_detail } from "@/utils/communication.js";
import modify_token_dialog from "@/components/modify_token_dialog.vue";
import { fail_msg, succeed_msg } from "@/utils/msg.js";
import { parser, parse_to_string } from "@/utils/time_parser.js";

/*
describe('ParentComponent', () => {
    it("displays 'Emitted!' when custom event is emitted", () => {
        //const localVue = createLocalVue()
        //localVue.use(modify_token_dialog)
        const wrapper = mount(token_detail)
        
        try {
            const wrapper = mount(token_detail)
        }
        catch (err) {
            console.log('err is', err)
        }
        
        wrapper.find(modify_token_dialog)
    })
})
*/

/*
const wrapper = mount(token_detail, {
    global: {
        stubs: {
            modify_token_dialog: true
        }
    }
})
*/

const test_fail = 'test_fail'
const test_succeed = 'test_succeed'
const token_content = 'THUiLoveYou!!!'

jest.mock('@/utils/communication.js', () => {
    return {
        __esModule: true,
        delete_token: jest.fn(
            (list, user_name, pass_word) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: user_name == 'test_fail' ? "fail" : "succeed",
                        msg: "",
                        message: "",
                    } });
                }),
        ),
        get_app_detail: jest.fn(
            (token, key) =>
                new Promise((resolve, reject) => {
                    resolve({ data: {
                        status: token == 'test_fail' ? "fail" : "succeed",
                        tokens: [
                                {
                                    created_time: 10,
                                    dead_time: 100
                                },
                                {
                                    created_time: -1,
                                    dead_time: -100
                                }
                            ],
                        message: "",
                        msg: ""
                    } });
                }),
        ),
    };
});

const wrapper = shallowMount(token_detail, {
    global: {
        mocks: {
            $loading: jest.fn().mockReturnValue({
                close: jest.fn()
            })
        }
    }
})
/*
test('get_access', async () => {
    await wrapper.componentVM.get_access({
        row: {
            access: 1
        }
    })
})
*/
test('test_open_child_components', async () => {
    await wrapper.componentVM.open_add_dialog()
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.dialog_type).toBe(0)
    expect(wrapper.vm.add_token_dialog_visible).toBe(true)

    await wrapper.componentVM.open_edit_dialog({
        row: {
            content: ""
        }
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.dialog_type).toBe(1)
    expect(wrapper.vm.add_token_dialog_visible).toBe(true)
    
})

test('test_close_child_components', async () => {
    await wrapper.componentVM.close_add_dialog()
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.add_token_dialog_visible).toBe(false)
})

test('close', async () => {
    await wrapper.setProps({
        visible: 1
    })
    await wrapper.componentVM.close()
    await wrapper.vm.$nextTick()
    await flushPromises()

    expect(wrapper.emitted()).toHaveProperty('close')
    const emit_close = wrapper.emitted('close')
    expect(emit_close).toHaveLength(1)

    await wrapper.setProps({
        visible: 0
    })
    await wrapper.vm.$nextTick()
    await wrapper.setProps({
        token: token_content
    })
    await wrapper.vm.$nextTick()
    await wrapper.setProps({
        visible: 1
    })
    await wrapper.vm.$nextTick()
})

test('test_remove_token_method', async () => {
    // failed and ==
    await wrapper.setData({
        user_name: test_fail
    })
    await wrapper.setProps({
        token: token_content
    })
    await flushPromises()
    await wrapper.componentVM.remove_token({
        content: token_content
    })
    await flushPromises()

    // succeeded and !=
    await wrapper.setData({
        user_name: test_succeed
    })
    await wrapper.setProps({
        token: token_content + "?"
    })
    await flushPromises()
    await wrapper.componentVM.remove_token({
        content: token_content
    })
    await flushPromises()
})

test('change_token_and_test_update_tokens_method', async () => {
    // failed
    await wrapper.setProps({
        visible: 1
    })
    await wrapper.vm.$nextTick()
    await wrapper.setProps({
        token: test_fail
    })
    await flushPromises()

    // succeeded
    await wrapper.setProps({
        token: test_succeed
    })
    await flushPromises()
})

/*
console.log(token_detail)
const wrapper = mount(token_detail, {
    props: {
        token: "",
        visible: false
    },
    components: {
        modify_token_dialog
    }
})
/*

/*
test('open_add_dialog', async () => {
    
})

test('close_add_dialog', async () => {

})

test('remove_token', async () => {
    
})

test('close_add_dialog', async () => {
    
})

test('update_tokens', async () => {
    
})

test('close_add_dialog', async () => {
    
})


/*
import { delete_token, get_app_detail } from "@/utils/communication.js";
import modify_token_dialog from "@/components/modify_token_dialog.vue";
import { fail_msg, succeed_msg } from "@/utils/msg.js";
import { parser, parse_to_string } from "@/utils/time_parser.js";
*/
