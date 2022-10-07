<!--
 * @FileDescription: 修改用户信息页
 * @Author: yaojianzhu
 * @Date: 2021.3.30
 * @LastEditors: yaojianzhu
 * @LastEditTime: 2021.3.30
 -->
<template>
    <el-dialog @close="close" title="修改信息" v-model="visible">
        如只需要更改用户名，则不需要输入下面的新密码。
       <el-form :model="form">
            <br />
            <el-form-item label="用户名" :label-width="form_label_width">
                <el-input
                    v-model="form.user_name"
                    autocomplete="off"
                ></el-input>
            </el-form-item>
            <el-form-item label="新密码" :label-width="form_label_width">
                <el-input
                    v-model="form.pass_word"
                    autocomplete="off"
                    show-password
                ></el-input>
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="close">取 消</el-button>
                <el-button type="primary" @click="confirm">确 定</el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script>
import { edit_user } from "../utils/communication.js";
import { fail_msg, succeed_msg } from "../utils/msg.js";
export default {
    name: "user_edit",
    props: {
        visible: false, //对话框是否可见
    },
    emits: ["close"],
    data() {
        return {
            form_label_width: "120px", //输入框宽度
            form: {
                //关闭对话框的清空操作为visible的watch函数负责
                user_name: "", //用户名
                pass_word: "", //密码
            },
            old_user_name: "", //旧用户名
            old_pass_word: "", //旧密码
        };
    },
    methods: {
        close: function () {
            /**
             * @description: 关闭当前对话框
             * @return void
             */
            this.$emit("close");
        },
        confirm: function () {
            /**
             * @description: 确认修改用户名和密码
             * @return void
             */
            var that = this;
            var changed = false;
            if (this.form.pass_word == "") {
                changed = true;
                if (this.old_user_name != this.form.user_name) {
                    //只修改了用户名
                    if (this.form.user_name == "") {
                        //填写的用户名为空
                        this.$emit("close");
                    } else {
                        //填写的用户名可以被正常提交
                        edit_user(
                            this.old_user_name,
                            this.old_pass_word,
                            this.form.user_name,
                            this.form.pass_word
                        ).then(function (res) {
                            // console.log("只修改用户名", res);
                            if (res.data.status == "fail")
                                fail_msg(res.data.msg);
                            else {
                                succeed_msg("修改用户名成功");
                                localStorage.setItem(
                                    "user_name",
                                    that.form.user_name
                                );
                                that.close();
                            }
                        });
                    }
                } else {
                    //什么都没有修改
                    this.$emit("close");
                }
            }
            if (changed) return;
            edit_user(
                this.old_user_name,
                this.old_pass_word,
                this.form.user_name,
                this.form.pass_word
            ).then(function (res) {
                // console.log("编辑用户信息", res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else {
                    localStorage.setItem("user_name", that.form.user_name);
                    localStorage.setItem("pass_word", that.form.pass_word);
                    that.close();
                    succeed_msg("更改用户信息成功");
                }
            });
        },
    },
    mounted() {},
    watch: {
        visible: {
            handler(vis) {
                if (vis == true) {
                    //开启
                    this.old_user_name = localStorage.getItem("user_name");
                    this.old_pass_word = localStorage.getItem("pass_word");
                    this.form.user_name = this.old_user_name;
                } else {
                    //关闭
                    this.form.user_name = "";
                    this.form.pass_word = "";
                }
            },
        },
    },
};
</script>

<style>
.avatar {
    text-align: center;
}
</style>
