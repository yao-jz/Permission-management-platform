<template>
    <read
        v-if="show_read"
        @back="back"
        :from="selected_from"
        :created_time="selected_created_time"
        :msg="selected_msg"
        :to="selected_to"
        :title="selected_title"
    ></read>
    <div v-if="!show_read">
        <el-table :data="list">
            <el-table-column prop="title" property="title" label="主题">
            </el-table-column>
            <el-table-column prop="from" property="from" label="发送方">
            </el-table-column>
            <el-table-column prop="to" property="from" label="接受方">
            </el-table-column>
            <el-table-column label="操作"
                ><template #default="scope"
                    ><el-button @click="see(scope.row)">查看详情</el-button></template
                >
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
import read from "../components/read.vue";
export default {
    props: {
        list: Array,
    },
    components: {
        read,
    },
    data() {
        return {
            selected_from: "",
            selected_to: "",
            selected_msg: "",
            selected_created_time: "",
            selected_title: "",
            show_read: false,
        };
    },
    methods: {
        back: function(){
            this.selected_from = "";
            this.selected_to = "";
            this.selected_title = "";
            this.selected_created_time = "";
            this.selected_msg = "";
            this.show_read = false;
        },
        see: function (val) {
            this.selected_from = val.from;
            this.selected_to = val.to;
            this.selected_title = val.title;
            this.selected_created_time = val.created_time;
            this.selected_msg = val.message;
            this.show_read = true;
        },
    },
    watch:{
        list: {
            handler(){
                this.back();
            }
        }
    }
};
</script>
