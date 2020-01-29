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

        let data = new FormData()
        data.append('codec', this.form.subject.codec)  
        data.append('obj', this.$store.state.file_obj)
        data.append('type', this.form.subject.type)   

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
