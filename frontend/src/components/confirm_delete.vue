<!--
 * @FileDescription: 确认删除系统用户确认框
 * @Author: yaojianzhu
 * @Date: 2021.3.31
 * @LastEditors: yaojianzhu
 * @LastEditTime: 2021.3.31
 -->
<template>
    <el-dialog @close="close" title="注销用户" v-model="visible">
        <div>请将下面文字输入到输入框里</div>
        <h1
            style="
                -webkit-user-select: none;
                color: red;
                -moz-user-select: none;
                -ms-user-select: none;
                user-select: none;
            "
        >
            我确认要注销{{ user_name }}用户
        </h1>
        <el-input
            v-model="input_content"
            placeholder="请输入上述内容"
        ></el-input>
        <div style="color: red">{{ fail_msg }}</div>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="close">取 消</el-button>
                <el-button type="primary" @click="confirm">确 定</el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script>
// import { fail_msg, succeed_msg } from "../utils/msg.js";
export default {
    name: "confirm_delete",
    props: {
        visible: false, //对话框是否可见
    },
    emits: ["close", "confirm"],
    data() {
        return {
            user_name: "", //保存的用户名
            pass_word: "", //保存的密码
            input_content: "", //用户输入的内容
            confirm_available: false, //是否能够confirm
            fail_msg: "", //确认输入错误的提示语
        };
    },
    methods: {
        close: function () {
            /**
             * @description: 关闭当前对话框
             * @return void
             */
            this.$emit("close");
            this.fail_msg = "";
            this.input_content = "";
        },
        confirm: function () {
            /**
             * @description: 确认删除用户
             * @return void
             */
            if (
                this.input_content ==
                "我确认要注销" + this.user_name + "用户"
            ) {
                this.$emit("confirm");
                this.$emit("close");
                this.fail_msg = "";
                this.input_content = "";
            } else {
                this.fail_msg = "请正确输入确认标语";
            }
        },
    },
    watch: {
        visible: {
            handler(vis) {
                if (vis == true) {
                    this.user_name = localStorage.getItem("user_name");
                    this.pass_word = localStorage.getItem("pass_word");
                }
            },
        },
    },
};
</script>

<style></style>
