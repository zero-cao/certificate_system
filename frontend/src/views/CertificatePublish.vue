<template>
<div id="crt_pblh">
  <el-col :span="16">
    <el-form :model="form" label-width="180px">
      <h3>Have a request file?</h3>
      <el-form-item label="">
        <el-switch
          style="display: block"
          v-model="form.handle"
          active-color="#13ce66"
          inactive-color="#ff4949"
          active-text="Yes"
          inactive-text="No, go to create">
        </el-switch>
      </el-form-item>

      <h3 style="margin-top: 40px">Issuer</h3>
      <div class="issuer">      
        <el-form-item label="Certificate Authority">
          <el-select v-model="form.issuer.ca">
            <el-option label="wenca-rootca" value="wenca-rootca"></el-option>
            <el-option label="wenca-subca" value="wenca-subca"></el-option >
            <el-option label="wenca-grandca" value="wenca-grandca"></el-option>   
            <el-option v-if="!form.handle" label="self sign" value="SelfSign"></el-option>                      
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


      <div v-if="form.handle" class="subject"> 
        <h3 style="margin-top: 40px">Request</h3>    
        <el-form-item label="Request Codec">
          <el-select v-model="form.subject.codec">
            <el-option label="PEM/Base64" value="pem"></el-option>
            <el-option label="DER" value="der"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="Request File">
          <Upload />
        </el-form-item>
      </div>

      <div v-else>
        <h3 style="margin-top: 40px">Basic Information</h3>
        <div class="subjectBasic">
          <el-form-item label="Common Name">
            <el-input v-model="form.basic_information.common_name" clearable></el-input>
          </el-form-item>

          <el-form-item label="Country Name">
            <el-select v-model="form.basic_information.country">
              <el-option label="CN/China" value="CN"></el-option>
              <el-option label="US/America" value="US"></el-option>               
            </el-select>
          </el-form-item>

          <el-form-item label="Province">
            <el-input v-model="form.basic_information.province" clearable></el-input>
          </el-form-item>

          <el-form-item label="Locality">
            <el-input v-model="form.basic_information.locality" clearable></el-input>
          </el-form-item>

          <el-form-item label="Organization Name">
            <el-input v-model="form.basic_information.organization" clearable></el-input>
          </el-form-item>

          <el-form-item label="Organization Unit">
            <el-input v-model="form.basic_information.unit" clearable></el-input>
          </el-form-item>   
        </div>  

        <h3>Extensions</h3>
        <div class="subjectExtensions">
          <el-form-item label="Subject Alternative Names">
            <div v-for="(alias_name, index) in form.extensions.alias_names" :key="index">
              <el-input v-model="alias_name.value" class="input-with-select" clearable>
                <el-button slot="prepend" type="text" disabled>{{alias_name.type}}</el-button>
                <el-button slot="append" icon="el-icon-close" @click.prevent="removeSAN(alias_name)"></el-button>
              </el-input>
            </div>        
            <el-button icon="el-icon-circle-plus" @click="addSAN('IPv4')">IPv4</el-button>  
            <el-button icon="el-icon-circle-plus" @click="addSAN('IPv6')">IPv6</el-button>  
            <el-button icon="el-icon-circle-plus" @click="addSAN('DNS')">DNS</el-button>                      
          </el-form-item>

          <el-form-item label="Key Usages">
            <el-checkbox-group v-model="form.extensions.key_usages">
              <el-checkbox label="data_encipherment" name="key_usages"></el-checkbox>
              <el-checkbox label="digital_signature" name="key_usages"></el-checkbox>
              <el-checkbox label="key_cert_sign" name="key_usages"></el-checkbox>
              <el-checkbox label="content_commitment" name="key_usages"></el-checkbox>
              <el-checkbox label="key_encipherment" name="key_usages"></el-checkbox>
              <el-checkbox label="decipher_only" name="key_usages"></el-checkbox>
              <el-checkbox label="crl_sign" name="key_usages"></el-checkbox>
              <el-checkbox label="key_aggreement" name="key_usages"></el-checkbox>
              <el-checkbox label="encipher_only" name="key_usages"></el-checkbox>
            </el-checkbox-group>
          </el-form-item>

          <el-form-item label="Extended Key Usages">
            <el-checkbox-group v-model="form.extensions.extended_key_usages">
              <el-checkbox label="server_auth" name="extendec_key_usages"></el-checkbox>
              <el-checkbox label="client_auth" name="extendec_key_usages"></el-checkbox>
              <el-checkbox label="code_signing" name="extendec_key_usages"></el-checkbox>
              <el-checkbox label="email_protection" name="extendec_key_usages"></el-checkbox>
              <el-checkbox label="any_extended_key_usage" name="extendec_key_usages"></el-checkbox>
              <el-checkbox label="time_stamping" name="extendec_key_usages"></el-checkbox>
              <el-checkbox label="ocsp_signing" name="extendec_key_usages"></el-checkbox>
            </el-checkbox-group>
          </el-form-item>
        </div>  

        <h3>Key</h3>
        <div class="subjectKey">
          <el-form-item label="Key Type">
            <el-select v-model="form.key.key_type">
              <el-option label="RSA" value="rsa"></el-option>
              <el-option label="DSA" value="dsa" disabled></el-option>
              <el-option label="ECDSA" value="ecdsa" disabled></el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="Key Length">
            <el-select v-model="form.key.key_length">
              <el-option label="1024" :value="1024"></el-option>
              <el-option label="2048" :value="2048"></el-option>
              <el-option label="3072" :value="3072"></el-option>
              <el-option label="4096" :value="4096"></el-option>          
            </el-select>
          </el-form-item>	

          <el-form-item label="Password">
            <el-input type="password" v-model="form.key.password" clearable></el-input>
          </el-form-item>
        </div>   
      </div>

      <div class="submit">
        <el-form-item>
          <el-button type="primary" @click="onSubmit">Submit</el-button>
        </el-form-item>
      </div>
    </el-form>	
  </el-col>
  <AsciiCertificateDialog />  
</div>
</template>

<script>
import AsciiCertificateDialog from '../components/AsciiCertificateDialog'
import Upload from '../components/Upload'

export default {
  name: 'CertificatePublish',
  components: { AsciiCertificateDialog, Upload },  
  data () {
		return {
      form: {
        handle: true,
				issuer: {
					ca: 'wenca-rootca',
					valid_year: 1,
					hash_alg: 'sha256',
					is_ca: false
        },
        subject: {        
          codec: 'pem',
          obj: '',
          name: ''
        },
        basic_information: {
					common_name: '',
					country: 'CN',
					province: '',
					locality: '',
					organization: '',
					unit: ''
        },
        extensions: {
          alias_names: [
            {type: 'IPv4', value: ''},
            {type: 'IPv6', value: ''},
            {type: 'DNS', value: ''}
          ], 
          key_usages: [
            'data_encipherment',
            'digital_signature'
          ],
          extended_key_usages: [
            'server_auth'
          ]
        },
        key: {
          key_type: 'rsa',
          key_length: 2048,
          password: ''
        },        
      }  
    }
  },
  methods: {
    removeSAN (item) {
      var index = this.form.extensions.alias_names.indexOf(item);
      if (index !== -1) {
        this.form.extensions.alias_names.splice(index, 1);
      }
    },
    addSAN (type) {
      this.form.extensions.alias_names.push({type: type, value: ''});
    },    
		onSubmit () {
      if (this.form.handle) {
        let data = new FormData()
        data.append('ca', this.form.issuer.ca)
        data.append('valid_year', this.form.issuer.valid_year)
        data.append('hash_alg', this.form.issuer.hash_alg)
        data.append('is_ca', this.form.issuer.is_ca)
        data.append('req_codec', this.form.subject.codec)
        data.append('req', this.$store.state.file_obj)     

        this.$http.crt_sign(data, 'multipart/form-data')
        .then(response => {
          var file_name = this.$store.state.file_name.split('.')[0]+'.cer'
          this.blob(file_name, response.data)             
        })
        .catch(error => {
          this.$alert(error.message.content, error.message.title, {confirmButtonText: 'OK'})  
        })
      }

      else {
        let data = this.form
        this.$http.crt_make(data, 'application/json')
        .then(response => {
          this.$store.commit({type: 'update_ascii_crt_visible', data: true})        
          this.$store.commit({type: 'update_byte_crt', data: response})             
        })
        .catch(error => {
          this.$alert(error.message.content, error.message.title, {confirmButtonText: 'OK'})  
        })
      }      
    }
  }
}
</script>
