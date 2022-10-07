<!--
 * @FileDescription: 列表对话框，用来展示一个条目关联的其他条目的信息
 * @Author: yaojianzhu
 * @Date: 2021.3.16
 * @LastEditors: yaojianzhu
 * @LastEditTime: 2021.3.27
 -->
<template>

  <el-dialog :title="title_list[type]" v-model="dialog_table_visible">
    <el-table
      stripe
      :data="list_data"
      row-key="key"
      border
      :tree-props="{children: 'child_permissions'}"
    >
      <el-table-column class="name" prop="name" :label="name_list[type]">
      </el-table-column>
      <el-table-column class="key" prop="key" label="key"> </el-table-column>
      <el-table-column
        class="created_time"
        prop="created_time"
        label="创建时间"
      >
      </el-table-column>
    </el-table>
    <div style="text-align: right" class="dialog-footer">
      <div class="dialog-footer">
        <el-button class="close_button" @click="close">关闭</el-button>
      </div>
    </div>
  </el-dialog>
</template>

<script>

export default {
	name: "List_Dialog",
	props: {
		type: 0,
		visible: false,
		list_data: Array,
	},
	data() {
		return {
			dialog_table_visible: false, //是否可见
			title_list: [
				//标题列表
				"用户", "角色", "权限", "子权限"
			],
			name_list: [
				//name 列表
				"名称", "名称", "权限名称", "子权限名称"
			],
		}
	},
	methods: {
		close: function() {
			/**
             * @description: 关闭当前对话框
             * @return void
             */

			this.$emit("close")
		},
	},
	watch:{
		"visible":{
			handler(vis) {
				this.dialog_table_visible = vis
			}
		},
	},
}
</script>

<style></style>
