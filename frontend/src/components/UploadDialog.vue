<template>
<div id="upload">     
  <el-dialog width="40%" title="Upload your certificates" :before-close="handleDialog" :visible.sync="uploadVisible">
    <el-upload class="upload-demo" action=""
      :auto-upload="false" :multiple="true" :limit="10" :file-list="pending_file_list"
      :on-exceed="handleExceed" :on-remove="handleRemove" :on-change="handleChange">
      <el-button style="margin-top: 10px;" slot="trigger" size="small" type="success">Choose files</el-button>
      <div style="margin-bottom: 30px;" slot="tip" class="el-upload__tip">File mime type must be application/x-x509-ca-cert</div>
    </el-upload>
    <span slot="footer" class="dialog-footer">
      <el-button style="margin-left: 10px;" size="small" type="primary" @click="handleUpload">Upload</el-button>
    </span>
  </el-dialog>
</div>
</template>

<script>
export default {
  name:'UploadDialog',
  data () {
    return {
      pending_file_list: []
    }
  },
  computed: {
    uploadVisible () {
      return this.$store.state.upload_visible
    }
  },
  methods: {
    handleDialog () {
      this.$store.commit({type: 'update_upload_visible', data: false})
      this.pending_file_list = []
    },     
    handleExceed () {
      this.$message.warning('Just allow only 10 file to be uploaded')
    },
    handleRemove () {
      this.pending_file_list.pop()
    },
    handleChange (file) {
      if (file.raw.type === 'application/x-x509-ca-cert') {
        this.pending_file_list.push({name: file.name, raw: file.raw})
      }
      else {      
        this.pending_file_list.pop()
        this.$message.warning('File mime type is not application/x-x509-ca-cert')
      }
    },    
    handleUpload() {
      let file_list = this.pending_file_list
      if (file_list.length == 0) {
        this.$message.warning('Please choose at least 1 certificate file to upload')
        return false
      }

      let form_data = new FormData()
      for (var index in file_list) {
        form_data.append(file_list[index].name, file_list[index].raw)
      }

      this.$http.upload_crt_files(form_data)
      .then(() => {
        this.$store.commit({type: 'update_upload_visible', data: false})
        this.$router.go(0)
      })
      .catch(error => {
        this.$alert(error.message.content, error.message.title, {confirmButtonText: 'OK'})  
      })

    }
  }
}
</script>
