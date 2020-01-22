<template>
<div id="certificate">
  <el-dialog v-if="crtFormat === 'parsed'" 
    title="Parsed certificate or request is" width="50%"
    :before-close="handleDialog" :visible.sync="crtVisible">
    <el-tree :data="crtOutput"></el-tree>
    <span slot="footer" class="dialog-footer">
      <el-button type="primary" @click="handleDialog">Sure</el-button>
    </span>
  </el-dialog>
  <el-dialog v-if="crtFormat === 'ascii'"
    title="Parsed certificate or request is" width="50%"
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
  name: 'Certificate',
  computed: {
    crtVisible () {
      return this.$store.state.crt_visible
    },
    crtFormat () {
      return this.$store.state.crt_format
    },
    crtOutput () {
      var crt = this.$store.state.certificate

      if (this.crtFormat === 'parsed') {
        var certificate = []

        for (var title in crt) {
          var children_1 = []
          for (var subtitle in crt[title]) {
            var children_2 = []
            children_2.push({
              label: crt[title][subtitle]
            })
            children_1.push({
              label: subtitle,
              children: children_2
            })
          }
          certificate.push({
            label: title, 
            children: children_1
          })          
        }
      }

      else if (this.crtFormat === 'ascii') {
        certificate = crt
      }

      return certificate
    }
  },
  methods: {   
    handleDialog () {
      this.$store.commit({type: 'update_crt_visible', data: false})
      this.$store.commit({type: 'update_crt_format', data: ''})      
      this.$store.commit({type: 'update_certificate', data: ''})
    }   
  }
}
</script>
