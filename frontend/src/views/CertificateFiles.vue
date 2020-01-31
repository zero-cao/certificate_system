<template>
<div id="crt_files">
  <el-table stripe border :data="received_file_list" style="width: 100%">
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

    <el-table-column >
      <template slot="header">
        <el-button plain type="success" icon="el-icon-upload" @click="upload">Upload</el-button>
        <el-button plain type="warning" icon="el-icon-edit-outline" @click="make">Make</el-button>    
      </template>
      <template slot-scope="scope">
        <el-button plain round type="info" icon="el-icon-view" @click="parse(scope.$index, scope.row)"></el-button>
        <el-button plain round type="primary" icon="el-icon-download" @click="download(scope.$index, scope.row)"></el-button>    
        <el-button plain round type="danger" icon="el-icon-delete" @click="remove(scope.$index, scope.row)"></el-button> 
      </template>   
    </el-table-column>
  </el-table>

  <ParseDialog />
  <UploadDialog />
  <MakeDialog />
</div>
</template>


<script>
import ParseDialog from '../components/ParseDialog'
import UploadDialog from '../components/UploadDialog'
import MakeDialog from '../components/MakeDialog'

export default {
  name: 'CertificateFiles',
  components: { ParseDialog, UploadDialog, MakeDialog },  
	data () {
		return {
      received_file_list: [],
		}
	},
	created () {	
    this.$http.get_crt_files()
      .then(response => {
        var res = response

        for (var file in res) {
          this.received_file_list.push({
            filename: file,
            created_time: res[file]['created_time'],        
            modified_time: res[file]['modified_time'],
            file_size: res[file]['file_size'],
            file_type: res[file]['file_type'],       
          })
        }
      })
      .catch(error => {
        this.$alert(error.message.content, error.message.title, {confirmButtonText: 'OK'})  
      })
  },
  methods: { 
    upload () { 
      this.$store.commit({type: 'update_upload_visible', data: true})
    },  
    make () {
      this.$store.commit({type: 'update_make_visible', data: true})
    },
    parse (index, row) {
      let req_params = {'filename': row['filename'], 'operation': 'parse'}
      this.$http.get_crt_file(req_params)
      .then(response => {
        this.$store.commit({type: 'update_parsed_file', data: response})
      })
      .catch(error => {
        this.$alert(error.message.content, error.message.title, {confirmButtonText: 'OK'})           
      })
    },
    download (index, row) {
      let req_params = {'filename': row['filename'], 'operation': 'download'}
      let file_name = row['filename']
      this.$http.get_crt_file(req_params, 'blob')
      .then(response => {
        this.blob(file_name, response.data) 
      })
      .catch(error => {
        this.$alert(error.message.content, error.message.title, {confirmButtonText: 'OK'})                     
      })
    },
    remove (index, row) {
      this.$confirm(row['filename'], 'Delete Certificate File ?', {
        confirmButtonText: 'Sure',
        cancelButtonText: 'Cancel',
        type: 'warning'
      })
      .then(() => {
        this.$http.remove_crt_file({'filename': row['filename'], 'style': 'file'})
        .then(() => {
          this.$router.go(0)
        })
        .catch(error => {
          this.$alert(error.message.content, error.message.title, {confirmButtonText: 'OK'})           
        })          
      })
      .catch(() => {})      
    }        
  }
}
</script>