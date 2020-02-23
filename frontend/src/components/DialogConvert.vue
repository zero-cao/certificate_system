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
      dialogVisible: true,
      form: { password: ''}  
    }
  },
  methods: {
    closeDialog () {
      this.$store.commit({type: 'update_selected_file', data: {}})
      this.dialogVisible = false
    },          
    onSubmit () {
      let filename = this.$store.state.selected_file.filename
      let password = this.form.password
      if (filename === '') {
        this.$alert('filename should not be empty', 'Filename Error', {confirmButtonText: 'OK'})
        return false        
      }
      if (password === '') {
        this.$alert('password should not be empty', 'Password Error', {confirmButtonText: 'OK'})
        return false
      }
      this.$http.convert_crt_file(filename, password)
      .then(response => {         
        this.dialogVisible = false
        this.$store.commit({type: 'update_selected_file', data: {}})
        this.blob(filename + '.cer', response.subject.bytes)
        this.blob(filename + '.key', response.key.bytes)
      })
      .catch(error => {
        this.$alert(error.message.content, error.message.title, {confirmButtonText: 'OK'})  
      })
    }
  }
}
</script>
