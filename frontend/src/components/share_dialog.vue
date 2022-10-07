<template>
    <el-dialog @close="close" title="共享App" v-model="visible">
        <el-form>
            <el-form-item label="共享的用户名">
                <el-input
                    v-model="shared_user_name"
                    autocomplete="off"
                ></el-input>
            </el-form-item>
            <el-form-item label="共享权限">
                <el-radio-group
                    @change="change_value"
                    v-model="access"
                    size="medium"
                >
                    <el-radio-button label="admin"></el-radio-button>
                    <el-radio-button label="add"></el-radio-button>
                    <el-radio-button label="edit"></el-radio-button>
                    <el-radio-button label="see"></el-radio-button>
                </el-radio-group>
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
import { share_app } from "../utils/communication.js";
import { fail_msg, succeed_msg } from "../utils/msg.js";
export default {
    props: {
        visible: false,
        token: "",
    },
    emits:["close"],
    data() {
        return {
            shared_user_name: "",
            access: "",
            access_int: 1,
        };
    },
    methods: {
        close: function () {
            this.shared_user_name = "";
            this.access_int = 1;
            this.access = "";
            this.$emit("close");
        },
        confirm: function () {
            var that = this;
            share_app(
                this.token,
                localStorage.getItem("app_key"),
                this.shared_user_name,
                this.access_int,
                localStorage.getItem("user_name"),
                localStorage.getItem("pass_word")
            ).then(function (res) {
                // console.log("分享app", res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else {
                    succeed_msg("分享成功");
                    that.close();
                }
            });
        },
        change_value: function (value) {
            if (value == "all") {
                this.access_int = 0;
            } else if (value == "admin") {
                this.access_int = 1;
            } else if (value == "add") {
                this.access_int = 2;
            } else if (value == "edit") {
                this.access_int = 3;
            } else if (value == "see") {
                this.access_int = 4;
            }
        },
    },
};
</script>

<style></style>
