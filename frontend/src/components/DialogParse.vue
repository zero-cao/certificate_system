<template>
<div id="parse">
  <el-dialog title="Parsed certificate or request is" width="40%"
    :before-close="closeDialog" :visible.sync="dialogVisible">
    <el-tree :data="parsedFile"></el-tree>
    <span slot="footer" class="dialog-footer">
      <el-button type="primary" @click="closeDialog">Sure</el-button>
    </span>
  </el-dialog>  
</div>  
</template>

<script>
export default {
  name: 'DialogParse',
  data () {
    return {
      dialogVisible: true,
      parsedFile: []
    }
  },
  created () {
    let filename = this.$store.state.selected_file.filename
    if (filename === '') {
      this.$alert('filename should not be empty', 'Filename Error', {confirmButtonText: 'OK'})
      return false        
    }        
    this.$http.parse_crt_file(filename)
    .then(response => {
      this.dialogVisible = true
      var parsed_file = response

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
        this.parsedFile.push({
          label: title, 
          children: children_1
        })          
      }      
    })
    .catch(error => {
      this.$alert(error.message.content, error.message.title, {confirmButtonText: 'OK'})           
    })    
  },
  methods: {   
    closeDialog () {
      this.$store.commit({type: 'update_component_name', data: ''})
      this.dialogVisible = false
    }   
  }
}
</script>

<style>

</style>