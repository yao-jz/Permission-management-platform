<!--
 * @FileDescription: 角色列表，用来展示所有角色和角色的所有操作
 * @Author: yaojianzhu
 * @Date: 2021.3.16
 * @LastEditors: yaojianzhu
 * @LastEditTime: 2021.3.27
 -->
<template>
    <select_dialog
        @close="close_select_dialog"
        :visible="select_dialog_visible"
        :type="type"
        :token="app_token"
        :selected_role="selected_role"
        :selected_key="selected_key"
    ></select_dialog>
    <add_dialog
        :app_token="app_token"
        @close="close"
        @new_add="add"
        @new_edit="edit"
        :type="type"
        :visible="add_dialog_visible"
        :dialog_type="dialog_type"
        :selected_key="selected_key"
        :selected_name="selected_role"
    ></add_dialog>
    <list_dialog
        @close="close_list"
        :type="list_type"
        :visible="list_dialog_visible"
        :list_data="list_data"
    ></list_dialog>
    <el-row>
        <el-col :span="2">
            <div class="grid-content bg-purple-dark">
                <el-button
                    class="add_button"
                    type="success"
                    round
                    @click="add_role_dialog"
                    icon="el-icon-document-add"
                    >添加角色</el-button
                >
            </div>
        </el-col>
        <el-col :span="16">
            <div class="grid-content bg-purple-light"></div>
        </el-col>
        <el-col :span="5">
            <div class="grid-content bg-purple">
                <el-input
                    @change="search"
                    class="search_input"
                    placeholder="请输入内容"
                    prefix-icon="el-icon-search"
                    v-model="input"
                >
                </el-input>
            </div>
        </el-col>
        <el-col :span="1">
            <div class="grid-content bg-purple-light">
                <el-button
                    @click="search"
                    class="search_button"
                    icon="el-icon-search"
                    plain
                    type="primary"
                ></el-button>
            </div>
        </el-col>
    </el-row>
    
    <el-table :data="role_list" stripe>
        <el-table-column class="key" prop="key" label="key"> </el-table-column>

        <el-table-column class="name" prop="name" label="角色">
        </el-table-column>

        <el-table-column
            class="created_time"
            prop="created_time"
            label="创建时间"
        >
        </el-table-column>

        <el-table-column label="查看">
            <template #default="scope">
                <el-button
                    class="show_user_button"
                    type="primary"
                    plain
                    icon="el-icon-view"
                    @click="open_list(scope.row)"
                    >用户</el-button
                >
            </template>
        </el-table-column>

        <el-table-column label="编辑">
            <template #default="scope">
                <el-button
                    class="edit_permission_button"
                    type="primary"
                    plain
                    icon="el-icon-edit"
                    @click="role_permission(scope.row)"
                    >编辑权限</el-button
                >
            </template>
        </el-table-column>

        <el-table-column label="操作">
            <template #default="scope">
                <el-button
                    class="edit_button"
                    type="primary"
                    round
                    icon="el-icon-edit"
                    @click="open_edit(scope.row)"
                    >编辑</el-button
                >
                <el-popconfirm title="确定删除吗？" @confirm="rm(scope.row)">
                    <template #reference>
                        <el-button
                            class="delete_button"
                            type="danger"
                            round
                            icon="el-icon-delete"
                            >删除</el-button
                        >
                    </template>
                </el-popconfirm>
            </template>
        </el-table-column>
        -->
    </el-table>
    
</template>

<script>
import {
    attach,
    detach,
    edit,
    remove,
    add,
    show_relative,
} from "../utils/communication.js";
import { parser, parse_to_string } from "../utils/time_parser.js";
import { fail_msg, succeed_msg } from "../utils/msg";
import add_dialog from "./add_dialog.vue";
import modify_dialog from "./modify_dialog.vue";
import list_dialog from "./list_dialog.vue";
import select_dialog from "./select_dialog.vue";
export default {
    name: "Role_List",
    props: {
        app_token: "", //apptoken
        role_list: Array, //当前展示的所有条目
    },
    emits: ["update", "search"],
    components: {
        add_dialog,
        modify_dialog,
        list_dialog,
        select_dialog,
    },
    data() {
        return {
            input: "", //搜索输入
            type: 1, //类型
            add_dialog_visible: false, //添加对话框是否可见
            list_dialog_visible: false, //条目展示对话框是否可见
            select_dialog_visible: false, //关联对话框是否可见
            list_type: 1, //条目展示类型
            dialog_type: 0, //对话框类型
            selected_key: "", //选择的key
            list_data: [], //储存用来展示table_Dialog的list
            selected_role: "", //选择的角色

            now_page: 1, //当前页码
            loading: true, //是否正在加载中
            loading_instance: this.$loading()
        };
    },
    methods: {
        close_select_dialog: function () {
            /**
             * @description: 关闭关联对话框
             * @return void
             */

            this.select_dialog_visible = false;
        },
        search: function () {
            /**
             * @description: 搜索
             * @return void
             */
            this.loading_instance = this.$loading()
            this.loading = true;
            this.$emit("search", this.input);
        },
        add: function (state, type) {
            /**
             * @description: 添加角色
             * @param {Object} state
             * @param {Number} type
             * @return void
             */

            // console.log("add", state, type);
            var that = this;
            add(this.app_token, localStorage.getItem("app_key"), 1, [
                {
                    name: state.name,
                    key: state.key,
                },
            ]).then(function (res) {
                // console.log(res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else succeed_msg("添加成功");
                that.$emit("update", that.now_page, 1);
            });
        },
        add_role_dialog: function () {
            /**
             * @description: 打开添加角色对话框
             * @return void
             */

            this.selected_key = "";
            this.selected_role = "";
            this.dialog_type = 0;
            this.add_dialog_visible = true;
        },
        close: function () {
            /**
             * @description: 关闭添加角色对话框
             * @return void
             */

            this.add_dialog_visible = false;
            this.selected_key = "";
            this.selected_role = "";
        },
        role_permission: function (role) {
            /**
             * @description: 打开关联对话框
             * @param {Object} role
             * @return void
             */

            this.selected_role = role.name;
            this.selected_key = role.key;
            this.select_dialog_visible = true;
        },
        modify: function (now, direction, arr) {
            /**
             * @description: 进行关联操作
             * @param {Array} now
             * @param {String} direction
             * @param {Array} arr
             * @return void
             */

            var add_key_list = []; //角色增加的权限列表
            var rm_key_list = []; //角色删除的权限列表
            // console.log(now); //当前拥有的
            // console.log(direction); //方向
            // console.log(arr); //改变了
            var j = 1,
                len = 1;
            if (direction == "right") {
                //增加
                for (j = 0, len = arr.length; j < len; j++) {
                    add_key_list.push(arr[j]);
                }
                attach(
                    this.app_token,
                    localStorage.getItem("app_key"),
                    [],
                    [this.selected_key],
                    add_key_list
                );
            } else if (direction == "left") {
                //删除
                for (j = 0, len = arr.length; j < len; j++) {
                    rm_key_list.push(arr[j]);
                }
                detach(
                    this.app_token,
                    localStorage.getItem("app_key"),
                    [],
                    [this.selected_key],
                    rm_key_list
                );
            }
        },
        open_list: function (value) {
            /**
             * @description: 显示关联内容
             * @param {Object} value
             * @return void
             */

            var that = this;
            show_relative(
                this.app_token,
                localStorage.getItem("app_key"),
                1,
                0,
                value.key,
                0,
                19
            ).then(function (res) {
                // console.log(res);
                if (res.data.status == "fail") {
                    if (res.data.msg == "out of range") {
                        fail_msg("这个角色还没有被分到任何用户！");
                    } else {
                        fail_msg(res.data.msg);
                    }
                } else {
                    var temp_list_data = res.data.list;
                    for (var i = 0; i < temp_list_data.length; i++) {
                        temp_list_data[i].created_time = parse_to_string(
                            parser(temp_list_data[i].created_time)
                        );
                    }
                    that.list_data = temp_list_data;
                    that.list_dialog_visible = true;
                }
            });
        },
        close_list: function () {
            /**
             * @description: 关闭关联内容显示
             * @return void
             */

            this.list_dialog_visible = false;
            this.list_data = []; //返回初始值
        },
        edit: function (state, type) {
            /**
             * @description: 编辑信息
             * @param {Object} state
             * @param {Number} type
             * @return void
             */

            var that = this;
            edit(
                this.app_token,
                localStorage.getItem("app_key"),
                this.selected_key,
                type,
                {
                    name: state.name,
                    key: state.key,
                }
            ).then(function (res) {
                // console.log("编辑完成", res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else succeed_msg("编辑已保存");
                that.selected_key = "";
                that.$emit("update", that.now_page, 1);
            });
        },
        open_edit: function (state) {
            /**
             * @description: 打开编辑对话框
             * @param {Object} state
             * @return void
             */

            this.dialog_type = 1;
            this.selected_key = state.key;
            this.selected_role = state.name;
            this.add_dialog_visible = true;
        },
        rm: function (state) {
            /**
             * @description: 删除条目
             * @param {Object} state
             * @return void
             */

            // console.log("delete ", state);
            var that = this;
            remove(
                this.app_token,
                localStorage.getItem("app_key"),
                [state.key],
                1
            ).then(function (res) {
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else succeed_msg("已删除");
                // console.log("删除角色", res);
                that.$emit("update", that.now_page, 1);
            });
        },
    },
    watch: {
        role_list: {
            handler() {
                this.loading_instance.close()
                this.loading = false;
            },
        },
    },
};
</script>

<style></style>
