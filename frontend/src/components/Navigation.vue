<template>
<div class="nav">
<el-menu class="el-menu-vertical-demo">
  <el-menu-item index="1">
    <i class="el-icon-menu"></i>
    <span slot="title">
      <el-link href="/" type="success">Home</el-link>
    </span>
  </el-menu-item>

  <el-menu-item index="2">
    <i class="el-icon-document"></i>
    <span slot="title">
      <el-link href="/certificate/parsing" type="success">Certificate parsing</el-link>
    </span>
  </el-menu-item>

  <el-menu-item index="3">
    <i class="el-icon-s-tools"></i>
    <span slot="title">
      <el-link href="/certificate/convertion" type="success">Certificate convertion</el-link>
    </span>
  </el-menu-item>

  <el-menu-item index="3">
    <i class="el-icon-folder"></i>
    <span slot="title">
      <el-link href="/files" type="success">File managment</el-link>
    </span>
  </el-menu-item>

  <el-menu-item index="7">
    <i class="el-icon-s-custom"></i>
    <span slot="title">
      <el-button plain size="mini">Login/Register</el-button>
    </span>
  </el-menu-item>
</el-menu>

</div>
</template>

<script>
export default {
	name: 'Navigation'
}
</script>
