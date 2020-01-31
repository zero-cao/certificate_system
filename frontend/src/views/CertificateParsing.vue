<template>
<div id="crt_parse">
  <el-col :span="16">
    <el-form :model="form" ref="form" status-icon label-width="100px">
      <div class="subject">       
        <el-form-item label="Type">
          <el-select v-model="form.subject.type">
            <el-option label="Certificate" value="crt"></el-option>
            <el-option label="Certificate Chain" value="chain"></el-option>
            <el-option label="Certificate Signing Request" value="req"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item v-if="form.subject.type==='chain'" label="Password">
          <el-input type='password' v-model="form.subject.password"></el-input>
        </el-form-item>

        <el-form-item label="File">
          <Upload />
        </el-form-item>
      </div>

      <div class="submit">
        <el-form-item>
          <el-button type="primary" @click="onSubmit('form')">Submit</el-button>
        </el-form-item>
      </div>
    </el-form>	
  </el-col>
  <ParseDialog />
</div>
</template>    

<script>
import ParseDialog from '../components/ParseDialog'
import Upload from '../components/Upload'

export default {
  name: 'CertificateParsing',
  components: { ParseDialog, Upload },
  data () {
		return {
      form: {
        subject: {  
          type: 'crt',
          password: ''     
        }
      }
    }
  },
  methods: {
    onSubmit (form) {
      this.$refs[form].validate((valid) => {
        if (!valid) { return false }

        let file_type = this.form.subject.type
        let key_password = this.form.subject.password
        let file_obj = this.$store.state.pending_file
        console.log(file_type)
        console.log(key_password)
        console.log(file_obj)

        if (JSON.stringify(file_obj) == '{}') {
          this.$message.warning('Please choose at least 1 file to upload')
          return false
        }

        if (file_type === 'crt') {
          if (file_obj.raw.type != 'application/x-x509-ca-cert') {
            this.$message.warning('Certificate mime type is invalid')
            return false
          }
        }
        else if (file_type === 'chain') {
          if (file_obj.raw.type === 'application/x-pkcs7-certificates') {
            this.$message.warning('Not support .p7b, .p7c suffix certficate chain')
            return false
          }
          if (file_obj.raw.type != 'application/x-pkcs12') {
            this.$message.warning('Certificate chain mime type is invalid')
            return false
          }   
          if (key_password === '') {
            this.$message.warning('Please input certifcate chain password, empty is not allowed')
            return false
          }       
        }
        else if (file_type === 'req') {
          if (file_obj.raw.type != '') {
            this.$message.warning('Certificate signing request mime type is invalid')
            return false
          }
        }
        
        let data = new FormData()
        data.append('obj', file_obj.raw)
        data.append('type', file_type)   
        data.append('password', key_password)

        this.$http.crt_parse(data, 'multipart/form-data')
        .then(response => {
          this.$store.commit({type: 'update_parsed_file', data: response})              
        })
        .catch(error => {
          this.$alert(error.message.content, error.message.title, {confirmButtonText: 'OK'})  
        })
      })
    }
  }
}
</script>
