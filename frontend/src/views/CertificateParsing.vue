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
          <el-upload class="upload-demo" drag action=""
            :auto-upload="false"
            :multiple="false"
            :limit="1"
            :on-exceed="handleExceed"
            :on-change="handleChange">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">Drop file here or <em>click to upload</em></div>
          </el-upload>
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

export default {
  name: 'CertificateParsing',
  components: { Certificate },
  data () {
		return {
      form: {
        subject: {  
          type: 'crt',     
          codec: 'pem',
          obj: ''
        }
      }
    }
  },
  methods: {
    handleExceed () {
      this.$message.warning('Just allow only 1 file to be uploaded')
    },
    handleChange (file) { 
      this.form.subject.obj = file.raw
    },
    onSubmit (form) {
      this.$refs[form].validate((valid) => {
        if (!valid) { return false }

        let data = new FormData()
        data.append('codec', this.form.subject.codec)
        data.append('obj', this.form.subject.obj)   
        data.append('type', this.form.subject.type)   

        this.$http.crt_parse(data, 'multipart/form-data')
          .then(response => {
            this.$store.commit({type: 'update_crt_visible', data: true})
            this.$store.commit({type: 'update_crt_format', data: 'parsed'})
            this.$store.commit({type: 'update_certificate', data: response})              
          })
          .catch(error => {
            this.$alert(error.message.content, error.message.title, {
              confirmButtonText: 'OK',
              callback: action => {
                this.$message({
                  type: 'error',
                  showClose: true,
                  message: `action: ${ action }`
                })  
              }
            })  
          })

      })
    }
  }
}
</script>
