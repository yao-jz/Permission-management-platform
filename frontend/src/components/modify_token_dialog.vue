<!--
 * @FileDescription: 设置app_token时限对话框
 * @Author: yaojianzhu
 * @Date: 2021.3.29
 * @LastEditors: yaojianzhu
 * @LastEditTime: 2021.3.30
 -->
<template>
    <el-dialog
        :title="title_list[type]"
        v-model="visible"
        width="30%"
        @close="close"
    >
        请设置token期限（单位：天）
        <div class="block">
            <el-slider
                v-model="value"
                show-input
                :min="min"
                :max="max"
            ></el-slider>
        </div>
        <div text-align="right">
            <span class="dialog-footer">
                <el-button v-if="type == 1" type="danger" @click="infinite"
                    >绑定时间设为无穷</el-button
                >
                <el-button @click="close">取 消</el-button>
                <el-button :disabled="!value" type="primary" @click="confirm">确 定</el-button>
            </span>
        </div>
    </el-dialog>
</template>

<script>
import { add_token, change_token } from "../utils/communication.js";
import { fail_msg, succeed_msg } from "../utils/msg.js";
export default {
    name: "modify_token_dialog",
    props: {
        selected_token: String, //当前选择执行的token
        visible: false, //对话框是否可见
        type: 0, //dialog种类，0为添加dialog，1为编辑dialog
    },
    emits: ["close", "update"],
    data() {
        return {
            title_list: ["新增token", "编辑token"], //标题列表
            value: Number, //选择token有效的时间
            min: 0, //可以选择的时间最小值
            max: 365, //可以选择的时间最大值
            user_name: String, //用户名
            pass_word: String, //密码
        };
    },
    methods: {
        infinite: function () {
            var that = this;
            //为已有token添加时长
            change_token(
                [
                    {
                        app_token: this.selected_token,
                        app_key: localStorage.getItem("app_key"),
                        alive_time: "forever",
                    },
                ],
                localStorage.getItem("user_name"),
                localStorage.getItem("pass_word")
            ).then(function (res) {
                // console.log(res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else {
                    if (!res.data.msg) succeed_msg("已将时间设为无穷");
                    else fail_msg(res.data.msg);
                }
                that.$emit("update"); //更新token列表
            });
            this.$emit("close");
        },
        close: function () {
            /**
             * @description: 关闭当前编辑token对话框
             * @return void
             */
            this.$emit("update"); //先执行更新
            this.$emit("close"); //再进行关闭
        },
        confirm: function () {
            /**
             * @description: 确认添加/编辑token
             * @return void
             */
            var that = this;
            if (this.type == 0) {
                //添加token
                add_token(
                    this.selected_token,
                    localStorage.getItem("app_key"),
                    [
                        {
                            alive_time: this.value * 86400,
                        },
                    ],
                    this.user_name,
                    this.pass_word
                ).then(function (res) {
                    // console.log(res);
                    if (res.data.status == "fail") fail_msg(res.data.msg);
                    else succeed_msg("创建token成功！");
                    that.$emit("update"); //更新token列表
                });
            } else if (this.type == 1) {
                //为已有token添加时长
                change_token(
                    [
                        {
                            app_token: this.selected_token,
                            app_key: localStorage.getItem("app_key"),
                            alive_time: this.value * 86400,
                        },
                    ],
                    this.user_name,
                    this.pass_word
                ).then(function (res) {
                    // console.log(res);
                    if (res.data.status == "fail") fail_msg(res.data.msg);
                    else {
                        if (!res.data.msg) succeed_msg("添加时长成功");
                        else fail_msg(res.data.msg);
                    }
                    that.$emit("update"); //更新token列表
                });
            }
            this.$emit("close");
        },
    },
    watch: {
        visible: {
            handler() {
                this.user_name = localStorage.getItem("user_name");
                this.pass_word = localStorage.getItem("pass_word");
                this.value = 0;
            },
        },
    },
};
</script>

<style></style>
