<!--
 * @FileDescription: 绑定用户邮箱对话框
 * @Author: yaojianzhu
 * @Date: 2021.4.13
 * @LastEditors: yaojianzhu
 * @LastEditTime: 2021.4.13
 -->
<template>
    <el-dialog @close="close" title="绑定邮箱" v-model="dialog_visible">
        <el-form>
            <el-form-item label="邮箱">
                <el-input
                    class="name"
                    placeholder="请输入邮箱..."
                    v-model="email"
                    autocomplete="off"
                ></el-input>
            </el-form-item>
            <el-button
                type="success"
                :disabled="email_valid"
                @click="send_check_key"
                >发送验证码</el-button
            >
            <!-- <span
                class="wrong_msg"
                v-if="email_valid === false && email_wrong_message"
                style="color: red"
                >{{ email_wrong_message }}</span
            > -->
        </el-form>

        <el-form>
            <el-form-item label="验证码">
                <el-input
                    class="key"
                    placeholder="请输入验证码"
                    v-model="code"
                    autocomplete="off"
                ></el-input
                ><br />
            </el-form-item>
            <span
                class="wrong_msg"
                v-if="key_valid === false && key_wrong_message"
                style="color: red"
                >{{ key_wrong_message }}</span
            >
        </el-form>

        <div style="text-align: right" class="dialog-footer">
            <el-button class="cancel_button" @click="close">取 消</el-button>
            <el-button class="confirm_button" type="primary" @click="confirm">
                确认
            </el-button>
        </div>
    </el-dialog>
</template>
<script>
import { succeed_msg, fail_msg } from "../utils/msg";
import { get_info, verify_code, edit_email } from "../utils/communication.js";
export default {
    name: "email_dialog",
    props: {
        visible: false,
    },
    emits: ["close"],
    data() {
        return {
            user_name: "",
            pass_word: "",
            email: "", //邮箱
            dialog_visible: false, //是否可见
            code: "", //验证码
            key_wrong_message: "",
            key_valid: false,
            email_valid: false, //邮箱是否合法
            email_wrong_message: "",
        };
    },
    methods: {
        close: function () {
            this.$emit("close");
        },
        confirm: function () {
            this.check_key();
        },
        send_check_key: function () {
            // console.log(
            //     this.user_name,
            //     this.pass_word,
            //     this.email,
            //     "发送验证码"
            // );
            edit_email(this.user_name, this.pass_word, this.email).then(
                function (res) {
                    // console.log(res);
                    if (res.data.status == "fail") fail_msg(res.data.msg);
                    else succeed_msg("验证码已发送，请查看您的邮箱");
                }
            );
        },
        check_key: function () {
            var that = this;
            // console.log("verify验证码");
            verify_code(this.code, this.email).then(function (res) {
                // console.log(res);
                if (res.data.status == "fail") {
                    that.key_wrong_message = "验证码错误";
                } else {
                    succeed_msg("绑定邮箱成功");
                    localStorage.setItem("email", that.email);
                    that.close();
                }
            });
        },
    },
    watch: {
        visible: {
            handler(vis) {
                if (vis) {
                    this.user_name = localStorage.getItem("user_name");
                    this.pass_word = localStorage.getItem("pass_word");
                    var that = this;
                    get_info(this.user_name, this.pass_word).then(function (
                        res
                    ) {
                        // console.log("get email", res);
                        that.email = res.data.email;
                    });
                } else {
                    this.email = "";
                    this.code = "";
                    this.key_wrong_message = "";
                    this.key_valid = false;
                    this.email_valid = false; //邮箱是否合法
                    this.email_wrong_message = "";
                }
                this.dialog_visible = vis;
            },
        },
        // email: {
        //     handler(new_email) {
        //         if (
        //             !/^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/.test(
        //                 new_email
        //             )
        //         ) {
        //             this.email_valid = true;
        //             this.email_wrong_message = "";
        //         } else {
        //             this.email_valid = false;
        //             this.email_wrong_message = "邮件格式错误";
        //         }
        //     },
        // },
    },
};
</script>
<style></style>
