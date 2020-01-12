<template>
<div id="crt_parse">
  <el-col :span="16">
    <el-form :model="form" :rules="rules" ref="form" status-icon label-width="180px">
      <h3>Request or Certificate</h3>	
      <div class="subject">    
        <el-form-item label="Browser local">
          <el-switch v-model="form.subject.upload"></el-switch>
        </el-form-item>       

        <el-form-item label="Type">
          <el-select v-model="form.subject.type">
            <el-option label="Certificate Signing Request" value="req"></el-option>
            <el-option label="Certificate" value="crt"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="Codec">
          <el-select v-model="form.subject.codec">
            <el-option label="PEM/Base64" value="pem"></el-option>
            <el-option label="DER" value="der" disabled></el-option>
          </el-select>
        </el-form-item>

        <el-form-item v-if="form.subject.upload" label="File">
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

        <el-form-item v-else label="Content" prop="content">
          <el-input type="textarea" rows=10 v-model="form.subject.obj"></el-input>
        </el-form-item>  
      </div>

      <div class="submit">
        <el-form-item>
          <el-button type="primary" @click="onSubmit('form')">Submit</el-button>
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
    // var validateContent = (rule, value, callback) => {
    //   if (!value) { 
    //     return callback(new Error('Empty not be allowed')) 
    //   }
    //   else {
    //     callback();
    //   }
    // } 

		return {
      form: {
        subject: {
          upload: false,
          filelist: [],     
          type: 'crt',     
          codec: 'pem',
          obj: null
        }
      },  
      rules: {
        // content: [
        //   {validator: validateContent, trigger: 'change'},
        // ]
      }
    }
  },
  methods: {
    handleExceed () {
      this.$message.warning('Just allow only 1 file to be uploaded')
    },
    handleChange (file, fileList) { 
      // console.log(file)
      // console.log(fileList)
      this.form.subject.obj = file.raw
      this.form.subject.filelist = fileList
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
            this.$router.push({name: 'crt_data'})
            this.$store.commit({type: 'update_crt_data', data: response})    
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
