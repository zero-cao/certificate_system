<template>
<div id="crt_parse">
  <el-col :span="16">
    <el-form :model="form" ref="form" status-icon label-width="100px">
      <!-- <h3>Request or Certificate</h3>	 -->
      <div class="subject">       
        <el-form-item label="Type">
          <el-select v-model="form.subject.type">
            <el-option label="Certificate" value="crt"></el-option>
            <el-option label="Certificate Chain" value="chain" disabled></el-option>
            <el-option label="Certificate Signing Request" value="req"></el-option>
          </el-select>
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
          type: 'crt'     
        }
      }
    }
  },
  methods: {
    onSubmit (form) {
      this.$refs[form].validate((valid) => {
        if (!valid) { return false }

        let file_type = this.form.subject.type
        let file_obj = this.$store.state.file_obj

        if (file_type === 'chain') {
          if (!(file_obj.type in ['application/x-pkcs7-certificates', 'application/x-pkcs12'])) {
            this.$message.warning('Please provide valid certificate chain')
            return false
          }
        }
        else if (file_type === 'crt') {
          if (file_obj.type != 'application/x-x509-ca-cert') {
            this.$message.warning('Please provide valid certificate')
            return false
          }
        }
        else if (file_type === 'req') {
          if (file_obj.type != '') {
            this.$message.warning('Please provide valid certificate signing request')
            return false
          }
        }
        
        let data = new FormData()
        data.append('obj', file_obj)
        data.append('type', file_type)   

        this.$http.crt_parse(data, 'multipart/form-data')
        .then(response => {
          this.$store.commit({type: 'update_parse_visible', data: true})
          this.$store.commit({type: 'update_byte_crt', data: response})              
        })
        .catch(error => {
          this.$alert(error.message.content, error.message.title, {confirmButtonText: 'OK'})  
        })
      })
    }
  }
}
</script>
