<template>
<div id="crt_ca">
	<h3>The certificates are:</h3>
  <el-table stripe highlight-current-row @current-change="handleCurrentChange" 
    :data="crtFiles" style="width: 100%">
    <el-table-column type="index" width="30"></el-table-column>
    <el-table-column prop="filename" label="filename" width="150"></el-table-column>
    <el-table-column prop="file_type" label="file_type" width="200" ></el-table-column>
    <el-table-column prop="file_size" label="size (Bytes)" width="120" ></el-table-column>
    <el-table-column prop="created_time" label="created_time" width="160"></el-table-column>    
    <el-table-column prop="modified_time" label="modified_time" width="160"></el-table-column>    
    <el-table-column prop="url" label="url" width="350" ></el-table-column>        
    <el-table-column label="Operations">
      <el-button type="primary" icon="el-icon-document" @click="overview()"></el-button>
      <el-button type="success" icon="el-icon-download" @click="download()"></el-button>    
      <el-button type="danger" icon="el-icon-delete" @click="remove()" disabled></el-button>    
    </el-table-column>
  </el-table>
</div>
</template>


<script>
export default {
	name: 'CertificateCA',
	data () {
		return {
      crtFiles: [],
      currentRow: {}			
		}
	},
	created () {	
    this.$http.crt_files()
      .then(response => {
        var res = response

        for (var file in res) {
          this.crtFiles.push({
            filename: file,
            created_time: res[file]['created_time'],        
            modified_time: res[file]['modified_time'],
            file_size: res[file]['file_size'],
            file_type: res[file]['file_type'],    
            url: res[file]['url']       
          })
        }
      })
      .catch(error => {
        this.$alert(error.message.content, error.message.title, {
          confirmButtonText: 'OK',
          callback: action => {
            this.$message({
              type: 'error',
              showClose: true,
              message: `action: ${ action }`
            })  
          }
        })  
      })
  },
  methods: {
    handleCurrentChange (row) {
      this.currentRow = row
    },
    overview () {
      var currentUrl = this.currentRow['url']
      console.log(currentUrl)
    },
    download () {
      var currentUrl = this.currentRow['url']
      console.log(currentUrl)
    },
    delete () {
      var currentUrl = this.currentRow['url']
      console.log(currentUrl)
    }        
  }
}
</script>