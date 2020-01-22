<template>
<div id="upload">     
  <el-dialog width="40%" title="Upload your certificates" :before-close="handleDialog" :visible.sync="uploadVisible">
    <el-upload class="upload-demo" action=""
      :auto-upload="false" :multiple="true" :limit="10"
      :on-exceed="handleExceed" :on-change="handleChange">
      <el-button style="margin-top: 10px;" slot="trigger" size="small" type="primary">Choose files</el-button>
      <el-button style="margin-left: 10px;" size="small" type="success" @click="handleUpload">Upload</el-button>
      <div style="margin-bottom: 30px;" slot="tip" class="el-upload__tip">File mime type must be application/x-x509-ca-cert</div>
    </el-upload>
  </el-dialog>
</div>
</template>

<script>
export default {
  name:'UploadDialog',
  data () {
    return {
      crt_list: []
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
    },     
    handleExceed () {
      this.$message.warning('Just allow only 10 file to be uploaded')
    },
    handleChange (file) {
      if (file.raw.type === 'application/x-x509-ca-cert') {
        this.crt_list.push(file)
      }
      else {
        this.$message.warning('File mime type is not application/x-x509-ca-cert')
      }
    },    
    handleUpload() {
      let data = new FormData()
      let file_list = this.crt_list

      for (var index in file_list) {
        data.append(file_list[index].name, file_list[index].raw)
      }

      this.$http.upload_crt_files(data, 'multipart/form-data')
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
