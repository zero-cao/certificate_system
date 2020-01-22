<template>
<div id="crt_files">
	<h3>The certificates are:</h3>
  <el-table stripe :data="crtFiles" style="width: 100%">
    <el-table-column type="selection" width="30"></el-table-column>       
    <el-table-column type="index" width="30"></el-table-column>

    <el-table-column label="filename" width="150">
      <template slot-scope="scope">{{scope.row.filename}}</template>
    </el-table-column>
    <el-table-column label="file_type" width="200" >
      <template slot-scope="scope">{{scope.row.file_type}}</template>
    </el-table-column>

    <el-table-column label="size (Bytes)" width="120" >
      <template slot-scope="scope">{{scope.row.file_size}}</template>      
    </el-table-column>

    <el-table-column label="created_time" width="180">
      <template slot-scope="scope">
        <i class="el-icon-time"></i>
        <span style="margin-left: 10px">{{scope.row.created_time}}</span>
      </template>      
    </el-table-column>    
    <el-table-column label="modified_time" width="180">
      <template slot-scope="scope">
        <i class="el-icon-time"></i>
        <span style="margin-left: 10px">{{scope.row.modified_time}}</span>
      </template>       
    </el-table-column>   

    <el-table-column label="Operations">
      <template slot-scope="scope">
        <el-button type="primary" icon="el-icon-document" @click="overview(scope.$index, scope.row)"></el-button>
        <el-button type="success" icon="el-icon-download" @click="download(scope.$index, scope.row)"></el-button>    
        <el-button type="danger" icon="el-icon-delete" @click="remove(scope.$index, scope.row)"></el-button> 
      </template>   
    </el-table-column>
  </el-table>
  <Certificate />
</div>
</template>


<script>
import Certificate from '../components/Certificate'

export default {
  name: 'CertificateFiles',
  components: { Certificate },  
	data () {
		return {
      crtFiles: [],		
      dialogVisible: false,
      crtParsed: []    
		}
	},
	created () {	
    this.$http.get_crt_files()
      .then(response => {
        var res = response

        for (var file in res) {
          this.crtFiles.push({
            filename: file,
            created_time: res[file]['created_time'],        
            modified_time: res[file]['modified_time'],
            file_size: res[file]['file_size'],
            file_type: res[file]['file_type'],       
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
    handleDialog () {
      this.dialogVisible = false
      this.crtParsed = []
    },
    overview (index, row) {
      this.$http.get_crt_file({
        'filename': row['filename'],
        'style': 'content' 
      })
      .then(response => {
        this.$store.commit({type: 'update_crt_visible', data: true})
        this.$store.commit({type: 'update_crt_format', data: 'parsed'})
        this.$store.commit({type: 'update_certificate', data: response})
      })
      .catch(error=> {
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
    download (index, row) {
      let req_params = {
        'filename': row['filename'],
        'style': 'file' 
      }
      this.$http.get_crt_file(req_params, 'blob')
      .then(response => {
        // var file_name = decodeURI(response.headers['content-disposition'].split(';')[1])
        var file_name = req_params['filename']
        var blob = new Blob([response.data])

        if (window.navigator.msSaveOrOpenBlob) {
          navigator.msSaveBlob(blob, file_name)
        }
        
        else {
          var a = document.createElement('a')
          a.download = file_name
          a.href = window.URL.createObjectURL(blob)
          a.click()
        }
      })
      .catch(error=> {
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
    remove (index, row) {
      this.$confirm(row['filename'], 'Delete Certificate File ?', {
        confirmButtonText: 'Sure',
        cancelButtonText: 'Cancel',
        type: 'warning'
      })
      .then(() => {
        this.$http.remove_crt_file({
          'filename': row['filename'],
          'style': 'file' 
        })
        .then(response => {
          if (response.code === 200) {              
            this.$router.go(0)
          }
        })
        .catch(error=> {
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
      })
      .catch(() => {})      
    }        
  }
}
</script>