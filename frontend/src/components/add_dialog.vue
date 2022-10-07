<!--
 * @FileDescription: 添加/编辑条目对话框
 * @Author: yaojianzhu
 * @Date: 2021.3.16
 * @LastEditors: yaojianzhu
 * @LastEditTime: 2021.3.27
 -->
<template>
    <el-dialog
        @close="close"
        :title="title_list[dialog_type][type]"
        v-model="outer_visible"
    >
        <el-form :model="state">
            <el-form-item :label="label_list[type]">
                <el-input
                    class="name"
                    placeholder="请输入内容..."
                    v-model="state.name"
                    autocomplete="off"
                ></el-input>
            </el-form-item>
        </el-form>

        <span v-if="name_valid === false" style="color: red"
            >请设置合法{{ name_list[type] }}!</span
        >

        <el-form :model="state">
            <el-form-item label="key">
                <el-input
                    class="key"
                    @blur="here_check_key"
                    placeholder="请输入key..."
                    v-model="state.key"
                    autocomplete="off"
                ></el-input>
                <br />
            </el-form-item>
            <span
                class="wrong_msg"
                v-if="key_valid === false"
                style="color: red"
                >{{ key_wrong_message }}</span
            >
            <span v-if="key_valid == true">key可以正常使用</span>
        </el-form>

        <!-- <template #footer> -->
        <div style="text-align: right" class="dialog-footer">
            <el-button class="cancel_button" @click="close">取 消</el-button>
            <el-button
                class="confirm_button"
                type="primary"
                @click="create"
                :disabled="name_valid == false || key_valid == false"
                id="test_button_1"
            >
                确认
            </el-button>
        </div>
        <!-- </template> -->
    </el-dialog>
</template>

<script>
import { check_key } from "../utils/communication.js";
export default {
    name: "Add_Dialog",
    emits: ["new_add", "close", "new_edit"],
    props: {
        type: 0,
        visible: false,
        dialog_type: 0,
        selected_key: "",
        selected_name: "",
        app_token: "",
    },
    data() {
        return {
            name_valid: false, //名字合法性
            key_valid: false, //key合法性
            outer_visible: false, //是否可见
            title_list: [
                //标题列表
                ["添加用户", "添加角色", "添加权限"],
                ["编辑用户", "编辑角色", "编辑权限"],
                ["_", "_", "添加子权限"],
            ],
            label_list: ["用户姓名", "角色名称", "权限名称"], //label列表
            modify_list: ["创建用户", "创建角色", "创建权限"], //title列表
            name_list: ["用户名", "角色名称", "权限名称"], //name列表
            state: {
                //状态
                name: "",
                created_time: "",
                key: "",
            },
            key_wrong_message: "请输入Key", //错误提示语
            old_key: "", //原有的key
        };
    },

    methods: {
        create: function () {
            /**
             * @description: 创建新条目
             * @return void
             */

            if (this.dialog_type == 0) {
                var time = new Date();
                this.state.created_time = time.toLocaleDateString();
                this.$emit("new_add", this.state, this.type);
                this.$emit("close");
            } else if (this.dialog_type == 1) {
                this.$emit("new_edit", this.state, this.type);
                this.$emit("close");
            } else {
                this.$emit("new_add", this.state, this.type);
                this.$emit("close");
            }
            this.init();
        },
        close: function () {
            /**
             * @description: 关闭当前对话框
             * @return void
             */
            this.$emit("close");
            this.init();
        },
        here_check_key: function () {
            /**
             * @description: 检查key的合法性
             * @return void
             */

            this.key_wrong_message = "";
            this.key_valid = false;
            var that = this;
            if (this.dialog_type == 1 && this.state.key == this.old_key) {
                //编辑对话框且key未改变
                this.key_valid = true;
                return;
            }
            if (this.state.key == "") {
                //key是空的
                this.key_valid = false;
                this.key_wrong_message = "请输入你的key";
                return;
            }
            //POST进行检查
            check_key(
                this.app_token,
                localStorage.getItem("app_key"),
                this.type,
                this.state.key
            ).then(function (res) {
                // console.log("key check", res);
                if (res.data.status == "succeed") {
                    that.key_valid = true;
                    that.key_wrong_message = "key可以正常使用";
                } else {
                    //如果失败，需要修改失败提示语
                    that.key_wrong_message = res.data.msg;
                    that.key_valid = false;
                }
            });
        },
        init: function () {
            /**
             * @description: 初始化表单内容以及本组件参数
             * @return void
             */

            this.state.name = "";
            this.state.created_time = "";
            this.key_wrong_message = "请输入key";
            this.state.key = "";
            this.key_valid = false;
            this.name_valid = false;
        },
    },
    watch: {
        visible: {
            handler(vis) {
                this.init();
                this.outer_visible = vis;
                if (this.dialog_type == 1) {
                    //如果是编辑对话框，需要自动补上之前的信息
                    this.state.name = this.selected_name;
                    this.state.key = this.selected_key;
                    this.old_key = this.selected_key;
                    this.key_valid = true;
                }
            },
        },
        "state.name": {
            handler(new_name) {
                //检测用户名的合法性
                this.name_valid = /^[A-Za-z\u4e00-\u9fa5][-A-Za-z0-9\u4e00-\u9fa5_]*$/.test(
                    new_name
                );
            },
        },
        "state.key": {
            handler() {
                this.key_wrong_message = "";
                if(this.old_key != this.state.key)
                    this.key_valid = false;
                else {
                    this.key_valid = true;
                }
            }
        }
    },
};
</script>

<style></style>
