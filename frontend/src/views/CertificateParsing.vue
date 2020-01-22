<template>
<div id="crt_parse">
  <el-col :span="16">
    <el-form :model="form" ref="form" status-icon label-width="180px">
      <h3>Request or Certificate</h3>	
      <div class="subject">       
        <el-form-item label="Type">
          <el-select v-model="form.subject.type">
            <el-option label="Certificate Signing Request" value="req"></el-option>
            <el-option label="Certificate" value="crt"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="Codec">
          <el-select v-model="form.subject.codec">
            <el-option label="PEM/Base64" value="pem"></el-option>
            <el-option label="DER" value="der"></el-option>
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
  <Certificate />
</div>
</template>    

<script>
import Certificate from '../components/Certificate'
import Upload from '../components/Upload'

export default {
  name: 'CertificateParsing',
  components: { Certificate, Upload },
  data () {
		return {
      form: {
        subject: {  
          type: 'crt',     
          codec: 'pem'
        }
      }
    }
  },
  methods: {
    onSubmit (form) {
      this.$refs[form].validate((valid) => {
        if (!valid) { return false }

        let data = new FormData()
        data.append('codec', this.form.subject.codec)  
        data.append('obj', this.$store.state.file_obj)
        data.append('type', this.form.subject.type)   

        this.$http.crt_parse(data, 'multipart/form-data')
        .then(response => {
          this.$store.commit({type: 'update_crt_visible', data: true})
          this.$store.commit({type: 'update_crt_format', data: 'parsed'})
          this.$store.commit({type: 'update_certificate', data: response})              
        })
        .catch(error => {
          this.$alert(error.message.content, error.message.title, {confirmButtonText: 'OK'})  
        })
      })
    }
  }
}
</script>
