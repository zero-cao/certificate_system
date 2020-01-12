<template>
<div id="crt_ca">
	<h3>The CA certificates are:</h3>
  <el-table stripe :data="crtCA" height="400" max-height="1000" style="width: 100%">
    <el-table-column prop="name" label="name" width="150"></el-table-column>
    <el-table-column prop="issuer" label="issuer" width="150"></el-table-column>    
    <el-table-column prop="subject" label="subject" width="150"></el-table-column>
    <el-table-column prop="sign_alg" label="sign_alg" width="150" ></el-table-column>
    <el-table-column prop="from" label="from" width="150" ></el-table-column>
    <el-table-column prop="to" label="to" width="150" ></el-table-column>        
    <el-table-column label="Operations">
        <el-button type="success" @click="download(crtCA[name])">Download</el-button>
    </el-table-column>
  </el-table>
</div>
</template>


<script>
export default {
	name: 'CertificateCA',
	data () {
		return {
			crtCA: []			
		}
	},
	created () {	
    // var jsonData = this.$store.state.crt_ca
    var jsonData = {
      rootca: { 
        issuer: 'wenca-rootca',
        subject: 'wenca-rootca',
        sign_alg: 'sha1withRSA', 
        from: '2019.1.1', 
        to: '2020.1.1', 
        crt_file: '123'
      },
      subca: { 
        issuer: 'wenca-rootca', 
        subject: 'wenca-subca', 
        sign_alg: 'sha1withRSA',  
        from: '2019.1.1', 
        to: '2020.1.1',
        crt_file: '234'
      },
      grandca: {
        issuer: 'wenca-subca', 
        subject: 'wenca-grandca', 
        sign_alg: 'sha1withRSA',  
        from: '2019.1.1', 
        to: '2020.1.1',
        crt_file: '345'
      }
    }
		for (var ca in jsonData) {
      this.crtCA.push({
        name: ca,
        issuer: jsonData[ca].issuer,        
        subject: jsonData[ca].subject,
        sign_alg: jsonData[ca].sign_alg,
        from: jsonData[ca].from,
        to: jsonData[ca].to,       
        crt_file: jsonData[ca].crt_file         
      })
		}
  },
  methods: {
    download (name) {
      console.log(name)
      console.log(this.crtCA[name])
      this.$store.commit({type: 'update_crt_file', data: this.crtCA[name].crt_file})        
      this.$router.push({name: 'crt_file'})    
    }
  }
}
</script>