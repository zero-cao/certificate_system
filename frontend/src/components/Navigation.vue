<template>
<div class="nav">
	<el-menu
		class="el-menu-demo"
		mode="horizontal"
		background-color="#409EFF"
		text-color="#fff"
		active-text-color="#ffd04b">

		<el-menu-item index="1">
			<el-link href="/" type="success">Home</el-link>
		</el-menu-item>  

		<el-menu-item index="2">
			<el-link href="/certificate/publish" type="success">Publish certificate</el-link>
		</el-menu-item>

		<el-menu-item index="3">
			<el-link href="/certificate/parsing" type="success">Parse certificate</el-link>
		</el-menu-item>   
	</el-menu>
</div>
</template>

<script>
export default {
	name: 'Navigation'
}
</script>
