<template>
<div id="certificate">
  <el-dialog title="Parsed certificate or request is" width="40%"
    :before-close="handleDialog" :visible.sync="crtVisible">
    <el-tree :data="crtOutput"></el-tree>
    <span slot="footer" class="dialog-footer">
      <el-button type="primary" @click="handleDialog">Sure</el-button>
    </span>
  </el-dialog>
</div>      
</template>
  
<script>
export default {
  name: 'ParseDialog',
  computed: {
    crtVisible () {
      return this.$store.state.parse_visible
    },
    crtOutput () {
      var crt = this.$store.state.byte_crt
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
    
      return certificate
    }
  },
  methods: {   
    handleDialog () {
      this.$store.commit({type: 'update_parse_visible', data: false})    
      this.$store.commit({type: 'update_byte_crt', data: ''})
    }   
  }
}
</script>
