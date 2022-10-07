<!--
 * @FileDescription: 添加和编辑app对话框，可以用来设置app的名字和描述
 * @Author: yaojianzhu
 * @Date: 2021.3.20
 * @LastEditors: yaojianzhu
 * @LastEditTime: 2021.3.27
 -->
<template>
    <el-dialog
        @close="close"
        :title="title_list[type]"
        v-model="dialog_form_visible"
    >
        <el-form>
            <el-form-item label="app名称">
                <el-input
                    class="name"
                    v-model="local_state.name"
                    autocomplete="off"
                ></el-input>
            </el-form-item>
            <el-form-item label="app key">
                <el-input
                    class="key"
                    v-model="local_state.key"
                    autocomplete="off"
                ></el-input>
            </el-form-item>
            <el-form-item label="app描述">
                <el-input
                    class="description"
                    v-model="local_state.description"
                    autocomplete="off"
                ></el-input>
            </el-form-item>

        </el-form>
        <!-- <template #footer> -->
        <div style="text-align: right">
            <span class="dialog-footer">
                <el-button class="cancel_button" @click="close"
                    >取 消</el-button
                >
                <el-button
                    class="confirm_button"
                    type="primary"
                    @click="confirm"
                    >确 定</el-button
                >
            </span>
        </div>
        <!-- </template> -->
    </el-dialog>
</template>

<script>
export default {
    name: "Add_App_Dialog",
    props: {
        visible: false,
        token: "",
        type: 0, //0表示新建app，1表示编辑app
        state: {
            name: "",
            description: "",
            key: "",
        },
    },
    data() {
        return {
            title_list: ["创建app", "编辑app"], //标题列表
            local_state: {
                //修改内容
                name: "",
                key: "",
                description: "",
            },

            dialog_form_visible: false, //是否可见
        };
    },
    emits: ["edit", "close", "new_app"],
    methods: {
        close: function () {
            /**
             * @description: 关闭对话框
             * @return void
             */

            this.init();
            this.$emit("close");
        },
        confirm: function () {
            /**
             * @description: 确认更改，并向父组件传递修改信号
             * @return void
             */
            if (this.type == 1) {
                //编辑app时的confirm
                this.$emit(
                    "edit",
                    this.local_state.name,
                    this.local_state.key,
                    this.local_state.description,
                    this.token
                );
                this.$emit("close");
                this.init();
            } else {
                //添加app时的confirm
                this.$emit(
                    "new_app",
                    this.local_state.name,
                    this.local_state.key,
                    this.local_state.description
                );
                this.$emit("close");
                this.init();
            }
        },
        init: function () {
            /**
             * @description: 初始化对话框内的表单
             * @return void
             */

            this.local_state.name = "";
            this.local_state.description = "";
            this.local_state.key = "";
        },
    },
    mounted() {
        this.dialog_form_visible = this.visible;
    },
    watch: {
        visible: {
            handler(vis) {
                this.dialog_form_visible = vis;
                if (this.type == 1) {
                    //如果是编辑对话框，需要将原有的name和description放到对话框里
                    this.local_state.name = this.state.name;
                    this.local_state.description = this.state.description;
                    this.local_state.key = this.state.key;
                }
            },
        },
        "state.name": {
            handler(s) {
                this.local_state.name = s;
            },
        },
        "state.description": {
            handler(s) {
                this.local_state.description = s;
            },
        },
        "state.key": {
            handler(s){
                this.local_state.key = s;
            }
        }
    },
};
</script>
