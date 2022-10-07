/*
    author: yhy2001
    date: 2021/4/7
    state: finished
*/
import { shallowMount, mount, config } from '@vue/test-utils'
import user_edit from '@/components/user_edit.vue'
import axios from 'axios'
import flushPromises from "flush-promises"
import { createRouter, createWebHistory } from 'vue-router'
import * as init_local from '@/utils/init_local.js'
import * as communication from '@/utils/communication.js'

test('init_local', async () => {
    init_local.init_local()
})

test('communication.js', async () => {
    communication.get_list("", 0, 0, 1)
    communication.attach("", [], [], [])
    communication.detach("", [], [], [])
    communication.check_key("", "", "")
    communication.remove("", [], 1)
    communication.add_app([], "", "")
    communication.add("", 0, [])
    communication.login("", "")
    communication.get_app_list("", "")
    communication.logout()
    communication.register("", "")
    communication.get_detail("", 0, "")
    communication.get_app_detail("")
    communication.show_relative("", 0, 1, "", 0, 100)
    communication.get_total("", 0)
    communication.get_description("", 0, "")
    communication.edit("", "", 0, "")
    communication.search_content("", "", 0, 0, 100)
    communication.add_token("", [], "", "")
    communication.delete_token([], "", "")
    communication.change_token([], "", "")
    communication.edit_user("", "", "", "")
    communication.get_avatar("", "")
    communication.delete_user("", "")
    communication.verify_code("", "")
    communication.edit_email("", "", "")
    communication.get_info("", "")
    communication.set_role_time("", "", [], [])
    communication.share_app("", "", "", 0, "", "")
    communication.get_shared_app("", "")
    communication.get_user_group("", "")
    communication.change_token_access([], "", "")
    communication.sent_message("", "", "", "", "", "")

})
