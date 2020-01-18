<template>
<div id="crt_ca">
	<h3>The certificates are:</h3>
  <el-table stripe :data="crtFiles" style="width: 100%">
    <el-table-column type="selection" width="30"></el-table-column>       
    <el-table-column type="index" width="30"></el-table-column>

    <el-table-column label="filename" width="150">
      <template slot-scope="scope">{{scope.row.filename}}</template>
    </el-table-column>
    <el-table-column label="file_type" width="200" >
      <template slot-scope="scope">{{scope.row.file_type[0]}}</template>
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
</div>
</template>


<script>
export default {
	name: 'CertificateCA',
	data () {
		return {
      crtFiles: [],		
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
    overview (index, row) {
      this.$http.get_crt_file({
        'filename': row['filename'],
        'style': 'content' 
      })
        .then(response => {
          this.$router.push({name: 'crt_data'})
          this.$store.commit({type: 'update_crt_data', data: response}) 
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
      this.$http.get_crt_file({
        'filename': row['filename'],
        'style': 'file' 
      })
        .then(response => {
          console.log(response)
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
      this.$http.remove_crt_file({
        'filename': row['filename'],
        'style': 'file' 
      })
        .then(response => {
          console.log(response)
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
    }        
  }
}
</script>