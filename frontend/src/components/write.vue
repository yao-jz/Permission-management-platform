<template>
    <form>
        <div class="form-group mb-3"></div>
        <div class="form-group mb-3">
            <el-form>
                <el-form-item label="发送给">
                    <el-input
                        class="name"
                        placeholder="用户名"
                        v-model="to"
                        autocomplete="off"
                    ></el-input>
                </el-form-item>
                <el-form-item label="主题">
                    <el-input
                        class="title"
                        placeholder="主题"
                        v-model="title"
                        autocomplete="off"
                    ></el-input>
                </el-form-item>
                <el-form-item label="信息">
                    <el-input
                        class="msg"
                        type="textarea"
                        :rows="10"
                        placeholder="信息"
                        v-model="msg"
                        autocomplete="off"
                    ></el-input>
                </el-form-item>
            </el-form>
        </div>

        <div class="float-right mt-3">
            <button
                type="button"
                @click="send"
                class="btn waves-effect waves-light btn-primary"
            >
                Send
            </button>
        </div>
    </form>
</template>

<script>
export default {
    props: {
        send_to: "",
    },
    emits: ["send_msg"],
    data() {
        return {
            to: "",
            msg: "",
            title: "",
        };
    },
    methods: {
        send: function () {
            this.$emit("send_msg", this.to, this.msg, this.title);
            this.to = "";
            this.msg = "";
            this.title = "";
        },
    },
    mounted() {
        this.to = this.send_to;
    },
};
</script>
