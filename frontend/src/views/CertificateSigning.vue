<template>
<div id="crt_sign">
  <el-col :span="16">
    <el-form :model="form" label-width="180px">
      <h3>Issuer</h3>
      <div class="issuer">      
        <el-form-item label="Certificate Authority">
          <el-select v-model="form.issuer.ca">
            <el-option label="wenca-rootca" value="wenca-rootca"></el-option>
            <el-option label="wenca-subca" value="wenca-subca"></el-option >
            <el-option label="wenca-grandca" value="wenca-grandca"></el-option>             
          </el-select>
        </el-form-item>

        <el-form-item label="Valid Year" >
          <el-input-number v-model="form.issuer.valid_year" :min="1" :max="20"></el-input-number>
        </el-form-item>

        <el-form-item label="Hash Alogorithm">
          <el-select v-model="form.issuer.hash_alg">
            <el-option label="MD5" value="md5"></el-option>
            <el-option label="SHA1" value="sha1"></el-option>       
            <el-option label="SHA256" value="sha256"></el-option>          
            <el-option label="SHA384" value="sha384"></el-option>          
            <el-option label="SHA512" value="sha512"></el-option>          
          </el-select>
        </el-form-item>

        <el-form-item label="Is CA">
          <el-switch v-model="form.issuer.is_ca"></el-switch>
        </el-form-item>
      </div>

      <h3>Request</h3>	
      <div class="subject">     
        <el-form-item label="Request Codec">
          <el-select v-model="form.subject.codec">
            <el-option label="PEM/Base64" value="pem"></el-option>
            <el-option label="DER" value="der"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="Request File">
          <el-upload class="upload-demo" drag action=""
            :auto-upload="false"
            :multiple="false"
            :limit="1"
            :file-list="form.subject.filelist"
            :on-exceed="handleExceed"
            :on-change="handleChange">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">Drop file here or <em>click to upload</em></div>
          </el-upload>
        </el-form-item>
      </div>

      <div class="submit">
        <el-form-item>
          <el-button type="primary" @click="onSubmit">Submit</el-button>
        </el-form-item>
      </div>
    </el-form>	
  </el-col>
</div>
</template>

<script>
export default {
  name: 'CertificateSigning',
  data () {
		return {
      form: {
				issuer: {
					ca: 'wenca-rootca',
					valid_year: 1,
					hash_alg: 'sha256',
					is_ca: false
        },
        subject: {
          filelist: [],          
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
    handleChange (file, fileList) { 
      this.form.subject.obj = file.raw
      this.form.subject.filelist = fileList
    },
    onSubmit () {
      let data = new FormData()
      data.append('ca', this.form.issuer.ca)
      data.append('valid_year', this.form.issuer.valid_year)
      data.append('hash_alg', this.form.issuer.hash_alg)
      data.append('is_ca', this.form.issuer.is_ca)
      data.append('req_codec', this.form.subject.codec)
      data.append('req', this.form.subject.obj)      

      this.$http.crt_sign(data, 'multipart/form-data')
        .then(response => {
          this.$router.push({name: 'crt_file'})
          this.$store.commit({type: 'update_crt_file', data: response})          
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
    }
  }
}
</script>
