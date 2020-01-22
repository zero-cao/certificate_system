<template>
<div id="upload">     
  <el-dialog width="40%" title="Upload your certificates" :before-close="handleDialog" :visible.sync="uploadVisible">
    <el-upload class="upload-demo" action=""
      :auto-upload="false" :multiple="true" :limit="10"
      :on-exceed="handleExceed" :on-preview="handlePreview" :on-remove="handleRemove" :before-remove="beforeRemove">
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
    handleUpload() {
      this.$refs.upload.submit();
    },
    handleRemove(file, fileList) {
      console.log(file, fileList);
    },
    handlePreview(file) {
      console.log(file);
    }
  }
}
</script>