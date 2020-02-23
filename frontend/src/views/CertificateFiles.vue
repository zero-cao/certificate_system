<template>
<div id="crt_files">
  <!-- <el-input v-model="searched_content" size="medium" placeholder="输入关键字搜索"/> -->

  <el-table stripe border :data="received_file_list" style="width: 100%" :height="window_height" :max-height="max_height">
    <el-table-column type="index" width="30"></el-table-column>

    <el-table-column label="certificate_name" width="150">
      <template slot-scope="scope">{{scope.row.filename}}</template>
    </el-table-column>
    <el-table-column label="mime_type" width="200" >
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

  <component :is="componentName"/>
</div>
</template>


<script>

import DialogUpload from '../components/DialogUpload'
import DialogMake from '../components/DialogMake'
import DialogParse from '../components/DialogParse'
import DialogConvert from '../components/DialogConvert'
import DialogDownload from '../components/DialogDownload'
import DialogRemove from '../components/DialogRemove'

export default {
  name: 'CertificateFiles',
  components: { 
    DialogUpload, DialogMake, 
    DialogParse, DialogConvert, DialogDownload, 
    DialogRemove 
  }, 
  computed: {
    componentName () {
      return this.$store.state.component_name
    }
  },
	data () {
		return {
      component_name: '',
      received_file_list: [],
      searched_content: '',
      window_height: window.innerHeight,
      max_height: window.innerHeight * 0.9
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
      this.$store.commit({type: 'update_component_name', data: 'DialogUpload'})
    },  
    make () {
      this.$store.commit({type: 'update_component_name', data: 'DialogMake'})
    },
    parse (index, row) {
      if (row['file_type'] === 'application/x-x509-ca-cert') {
        this.$store.commit({type: 'update_component_name', data: 'DialogParse'})
        this.$store.commit({type: 'update_selected_file', data: {'filename': row['filename'], 'file_type': row['file_type']}})  
      }
      else if (row['file_type'] === 'application/x-pkcs12') {
        this.$store.commit({type: 'update_component_name', data: 'DialogConvert'})
        this.$store.commit({type: 'update_selected_file', data: {'filename': row['filename'], 'file_type': row['file_type']}})
      }   
    },
    download (index, row) {
      this.$store.commit({type: 'update_component_name', data: 'DialogDownload'})
      this.$store.commit({type: 'update_selected_file', data: {'filename': row['filename'], 'file_type': row['file_type']}})
    },
    remove (index, row) {
      this.$store.commit({type: 'update_component_name', data: 'DialogRemove'})
      this.$store.commit({type: 'update_selected_file', data: {'filename': row['filename'], 'file_type': row['file_type']}})     
    }        
  }
}
</script>