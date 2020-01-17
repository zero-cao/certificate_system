<template>
<div id='crt_file'>
	<el-col :span="12">
		<h3>Certificate content is:</h3>
		<el-input type="textarea" v-model="crt_file" rows="24" readonly></el-input>
		<br><br>
		<el-button type="primary" icon="el-icon-arrow-left" @click="back">Back</el-button>
	</el-col>
</div>
</template>

<script>
export default {
	name: 'CertificateFile',
	data () {
		return {
			'crt_file': ''
		}
	},
	created () {
		this.crt_file = this.$store.state.crt_file
	},
	methods: {
		back () {
			this.$router.go(-1)
		}
	}
}
</script>
