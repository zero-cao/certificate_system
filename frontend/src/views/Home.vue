<template>
<div id="home">
	<el-col :span="12">
		<h1>Welcome to visit mywebsit</h1>
		<h3>Overview frontend source code</h3>
		<el-link href="https://github.com/zero-cao/certificate_system_frontend" type="warning">
			<i class="el-icon-view el-icon--right"></i> 
		</el-link> 

		<h3>Overview backend source code</h3>
		<el-link href="https://github.com/zero-cao/certificate_system_backend" type="warning">
			<i class="el-icon-view el-icon--right"></i> 
		</el-link>

		<h3>Search what you need</h3>
		<el-form :inline="true" :model="formInline" class="demo-form-inline">
			<el-form-item>
				<el-input v-model="formInline.input"></el-input>
			</el-form-item>
			<el-form-item>
				<el-button type="primary" icon="el-icon-search" @click="onSubmit">Search</el-button>
			</el-form-item>
		</el-form>
	</el-col>
</div>
</template>

<script>
export default {
	name: 'Home',
	data () {
		return {
			formInline: {
				input: '',
			}
		}
	},
	methods: {
		onSubmit () {
			console.log('submit')
		}
	}
}
</script>

<style scoped>
#home {
	text-align: left;
}
</style>