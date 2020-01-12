<template>
<div id="crt_data">
	<h3>The result is:</h3>
  <el-table stripe :data="crtData" height="400" max-height="1000" style="width: 100%">
    <el-table-column prop="title" label="title" width="180"></el-table-column>
    <el-table-column prop="subtitle" label="subtitle" width="180"></el-table-column>
    <el-table-column prop="value" label="value"></el-table-column>
  </el-table>
	<br>
	<el-button type="primary" icon="el-icon-arrow-left" @click="back">
		Back
	</el-button>
</div>
</template>


<script>
export default {
	name: 'CertificateData',
	data () {
		return {
			crtData: []			
		}
	},
	created () {	
		var jsonData = this.$store.state.crt_data
		for (var title in jsonData) {
			for (var subtitle in jsonData[title]) {
				this.crtData.push({
					title: title,
					subtitle: subtitle,
					value: jsonData[title][subtitle]
				})
			}
		}
	},
	methods: {
		back () {
			this.$router.go(-1)
		}
	}
}
</script>