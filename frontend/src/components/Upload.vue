<template>
<div id="upload">
  <el-upload class="upload-demo" drag action=""
    :auto-upload="false" :multiple="false" :limit="1"
    :on-exceed="handleExceed" :on-remove="handleRemove" :on-change="handleChange">
    <i class="el-icon-upload"></i>
    <div class="el-upload__text">Drop file here or <em>click to upload</em></div>
  </el-upload>
</div>
</template>

<script>
export default {
  name: 'Upload',
  methods: {
    handleExceed () {
      this.$message.warning('Just allow only 1 file to be uploaded')
    },
    handleRemove () {
      this.$store.commit({type: 'update_pending_file', data: {}})
    },
    handleChange (file) {
      this.$store.commit({type: 'update_pending_file', data: {name: file.name, raw: file.raw}})
    }
  }
}
</script>