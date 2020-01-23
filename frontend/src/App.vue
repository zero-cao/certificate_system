<template>
<div id="app">
<el-container style="border: 1px solid #eee">
  <el-aside width="180px" style="background-color: rgb(238, 241, 246)">
    <Navigation />
  </el-aside>
  
  <el-container>
    <!-- <el-header style="text-align: right; font-size: 12px">
    </el-header> -->
    
    <el-main><Main /></el-main>
  </el-container>
</el-container>
</div>
</template>

<script>
import Navigation from './components/Navigation'
import Main from './components/Main'

export default {
  name: 'app',
  components: { Main, Navigation }
}
</script>
