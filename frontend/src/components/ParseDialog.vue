<template>
<div id="certificate">
  <el-dialog title="Parsed certificate or request is" width="40%"
    :before-close="handleDialog" :visible.sync="dialogVisible">
    <el-tree :data="parsedFile"></el-tree>
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
    dialogVisible () {
      var parsed_file = this.$store.state.parsed_file

      if (JSON.stringify(parsed_file) == '{}') {
        return false
      }
      else {
        return true
      }
    },
    parsedFile () {
      var parsed_file = this.$store.state.parsed_file
      var certificate = []

      for (var title in parsed_file) {
        var children_1 = []
        for (var subtitle in parsed_file[title]) {
          var children_2 = []
          children_2.push({
            label: parsed_file[title][subtitle]
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
      this.$store.commit({type: 'update_parsed_file', data: {}})
    }   
  }
}
</script>
