<template>
<div id="certificate">
  <el-dialog title="Parsed certificate or request is" width="50%"
    :before-close="handleDialog" :visible.sync="crtVisible">
    <el-input  type="textarea" v-model="crtOutput" rows="24" readonly></el-input>
    <span slot="footer" class="dialog-footer">
      <el-button type="primary" @click="handleDialog">Sure</el-button>
    </span>
  </el-dialog>
</div>    
</template>
  
<script>
export default {
  name: 'AsciiCertificateDialog',
  computed: {
    crtVisible () {
      return this.$store.state.ascii_crt_visible
    },
    crtOutput () {
      return this.$store.state.byte_crt
    }
  },
  methods: {   
    handleDialog () {
      this.$store.commit({type: 'update_ascii_crt_visible', data: false})     
      this.$store.commit({type: 'update_byte_crt', data: ''})
    }   
  }
}
</script>
