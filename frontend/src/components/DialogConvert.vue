<template>
<div id="convert">
  <el-dialog title="Please provide certificate chain password" width="40%"
    :before-close="closeDialog" :visible.sync="dialogVisible">
    <el-form :model="form" ref="form" status-icon label-width="100px">
      <div class="subject">       
        <el-form-item label="Password">
          <el-input type='password' v-model="form.password"></el-input>
        </el-form-item>
      </div>

      <div class="submit">
        <el-form-item>
          <el-button type="primary" @click="onSubmit('form')">Submit</el-button>
        </el-form-item>
      </div>
    </el-form>	
  </el-dialog>
</div>
</template>    

<script>
export default {
  name: 'DialogConvert',
  data () {
    return {
      dialogVisible: false,
      fileName: '',
      fileType: '',
      form: {
        password: ''
      }  
    }
  },
  created () {
    this.fileName = this.$store.state.selected_file.filename
    this.fileType = this.$store.state.selected_file.file_type
    if (this.fileType === 'application/x-pkcs12') {
      this.dialogVisible = true
    }
  },
  methods: {
    closeDialog () {
      this.$store.commit({type: 'update_selected_file', data: {}})
      this.dialogVisible = false
    },          
    onSubmit (form) {
      this.$refs[form].validate((valid) => {
        if (!valid) { return false }

        let json_data = this.form
        this.$http.convert_crt_file(json_data, this.fileName)
        .then(response => {         
          this.$store.commit({type: 'update_selected_file', data: {}})
          console.log(response)
        })
        .catch(error => {
          this.$alert(error.message.content, error.message.title, {confirmButtonText: 'OK'})  
        })
      })
    }
  }
}
</script>
