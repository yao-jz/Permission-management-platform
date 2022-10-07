<!--
 * @Description: 文件及简介
 * @Author: Cary
 * @Date: 2021-03-16 10:51:17
 * @FilePath: \excel-to-jsone:\work\vue-project\frontend\src\layout\index.vue
-->
<template>
  <div class="layout">
    <el-container style="height: 100vh;">
      <el-aside :width="getLwidth" class="left-aside">
        <el-menu
          :default-openeds="['1', '2']"
          background-color="#545c64"
          text-color="#fff"
          :collapse="isCollapse"
          active-text-color="#ffd04b">
          <!-- <router-link to="/layout/index">
              
            </router-link>
            <router-link to="/layout/index2">
              
            </router-link> -->

          <el-menu-item index="1">
            <i class="el-icon-menu"></i>
            <template #title>导航二</template>
          </el-menu-item>
          <el-menu-item index="2">
            <i class="el-icon-setting"></i>
            <template #title>导航四</template>
          </el-menu-item>
          <el-submenu index="3">
            <template #title>
              <i class="el-icon-location"></i>
              <span>导航一</span>
            </template>
            <el-menu-item index="3-4-1">选项1</el-menu-item>
            <el-menu-item index="3-4-2">选项1</el-menu-item>
            <el-menu-item index="3-4-3">选项1</el-menu-item>
            <el-menu-item index="3-4-4">选项1</el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header class="c-elheader">
          <div class="header-top" style="height: 100%;">
            <div>
              <fold-icon @click="handleFoldClick"/>
            </div>
            <div>
              <el-dropdown trigger="click">
                <el-avatar style="margin-top: 10px" :src="avatar"></el-avatar>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="a">首页</el-dropdown-item>
                    
                    <el-dropdown-item command="e" divided>Logout</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
        </el-header>
        <el-main style="padding: 0">
          <router-view/>
        </el-main>
        <!-- <el-footer>Footer</el-footer> -->
      </el-container>
    </el-container>
  </div>
</template>

<script>
import LogoSrc from '../assets/logo.png'
import FoldIcon from './components/fold-icon'
export default {
  components: {
    FoldIcon
  },
  data() {
    return {
      avatar: LogoSrc,
      isCollapse: false,
      leftWidth: 230
    }
  },
  computed: {
    getLwidth() {
      return this.leftWidth + 'px'
    }
  },
  mounted() {},
  methods: {
    handleFoldClick() {
      this.isCollapse = !this.isCollapse
      let min = 62
      let max = 230
      if (this.isCollapse) {
        min = 230
        max = 62
      }
      this.animationTime(min, max, 8, (num) => {
        console.log('num', num)
        this.leftWidth = num
      })
    },

    animationTime(from, to, step, call) {
      let timeid = null
      step = from > to ? -step : step 
      timeid && clearTimeout(timeid)
      let _fr = from
      timeid = setInterval(() => {
        if (step < 0) {
          if (_fr < to) {
            clearTimeout(timeid)
            call(to)
          } else {
            _fr += step
            call(_fr)
          }
          return
        }
        if (_fr >= to) {
          clearTimeout(timeid)
          call(to)
        } else {
          _fr += step
          call(_fr)
        }
      }, 10)
    }

  },
}
</script>
<style>
  .el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
  }
</style>
<style lang="scss" scoped>

.layout {
  .el-menu {
    border-right:none;
  }
  :deep .c-elheader {
    box-shadow: 0 1px 4px rgb(0 21 41 / 8%);
  }
  
  .left-aside {
    border-right: solid 1px #e6e6e6;
    overflow-x: hidden;
    background-color: #545c64;
  }
  .header-top {
    line-height: 60px;
    display: flex;
    justify-content: space-between;
  }
}
</style>
