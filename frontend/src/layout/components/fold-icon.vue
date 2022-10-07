<!--
 * @Description: 文件及简介
 * @Author: Cary
 * @Date: 2021-03-19 14:17:34
 * @FilePath: \excel-to-jsone:\work\vue-project\frontend\src\layout\components\fold-icon.vue
-->

<template>
  <span class="fold" @click="handleClick">
    <i :class="{ 'el-icon-s-unfold': isFold, 'el-icon-s-fold': !isFold }" class="oicon"/>
  </span>
</template>

<script>
import { ref } from 'vue'
export default {
  name:'FoldIcon',
  emits: ['click'],
  setup(porps, { emit }) {
    let isFold = ref(true)
    const handleClick = () => {
      isFold.value = !isFold.value
      emit('click', isFold.value)
    }
    console.log('isFold', isFold)
    return {
      isFold,
      handleClick

    }
  }
}
</script>

<style lang='scss' scoped>
.fold {
  cursor: pointer;
}
.oicon {
  font-size: 26px;
}
</style>

