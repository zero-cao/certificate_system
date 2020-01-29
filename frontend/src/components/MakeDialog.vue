<template>
<div id="crt_pblh">
  <el-dialog width="50%" title="Make certificate" :before-close="handleDialog" :visible.sync="makeVisible">
    <el-form :model="form" label-width="150px">
      <el-tabs tab-position="left" style="height: 360px;" stretch>
        <el-tab-pane label="Issuer">
          <el-form-item label="Certificate Authority">
            <el-select v-model="form.issuer.ca">
              <el-option label="wenca-rootca" value="wenca-rootca"></el-option>
              <el-option label="wenca-subca" value="wenca-subca"></el-option >
              <el-option label="wenca-grandca" value="wenca-grandca"></el-option>   
              <el-option v-if="!enableSign" label="self sign" value="SelfSign"></el-option>                      
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
        </el-tab-pane>

        <el-tab-pane v-if="enableSign" label="Request">
          <el-form-item label="File">
            <Upload />
          </el-form-item>          
        </el-tab-pane>

        <el-tab-pane v-if="! enableSign" label="Basic Info">
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
        </el-tab-pane>

        <el-tab-pane v-if="! enableSign" label="SAN">
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
        </el-tab-pane>

        <el-tab-pane v-if="!enableSign" label="KU">
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
        </el-tab-pane>

        <el-tab-pane v-if="! enableSign" label="EKU">
          <el-form-item label="Extended Key Usages">
            <el-checkbox-group v-model="form.extensions.extended_key_usages">
              <el-checkbox label="server_auth" name="extended_key_usages"></el-checkbox>
              <el-checkbox label="client_auth" name="extended_key_usages"></el-checkbox>
              <el-checkbox label="code_signing" name="extended_key_usages"></el-checkbox>
              <el-checkbox label="email_protection" name="extended_key_usages"></el-checkbox>
              <el-checkbox label="any_extended_key_usage" name="extended_key_usages"></el-checkbox>
              <el-checkbox label="time_stamping" name="extended_key_usages"></el-checkbox>
              <el-checkbox label="ocsp_signing" name="extended_key_usages"></el-checkbox>
            </el-checkbox-group>
          </el-form-item>
        </el-tab-pane>

        <el-tab-pane v-if="! enableSign" label="Key">
          <el-form-item label="Type">
            <el-select v-model="form.key.key_type">
              <el-option label="RSA" value="rsa"></el-option>
              <el-option label="DSA" value="dsa" disabled></el-option>
              <el-option label="ECDSA" value="ecdsa" disabled></el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="Length">
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
        </el-tab-pane>
      </el-tabs>
    </el-form>	

    <div style="margin-top: 50px">
      <el-switch style="width:60%; float:left; display:block"
        v-model="enableSign"
        active-color="#13ce66"
        inactive-color="#ff4949"
        active-text="Have a request file"
        inactive-text="No, create a request file">
      </el-switch>

      <el-button style="width:15%; float:right"  
        type="primary" size="mini" @click="onSubmit">Submit
      </el-button>
    </div>
  </el-dialog> 
</div>
</template>

<script>
import Upload from '../components/Upload'

export default {
  name: 'CertificatePublish',
  components: { Upload }, 
  computed: {
    makeVisible () {
      return this.$store.state.make_visible
    }
  }, 
  data () {
		return {
      enableSign: false,
      form: {
				issuer: {
					ca: 'wenca-rootca',
					valid_year: 1,
					hash_alg: 'sha256',
					is_ca: false
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
    handleDialog () {
      this.$store.commit({type: 'update_make_visible', data: false})
    },      
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
      if (this.enableSign) {
        let data = new FormData()
        data.append('ca', this.form.issuer.ca)
        data.append('valid_year', this.form.issuer.valid_year)
        data.append('hash_alg', this.form.issuer.hash_alg)
        data.append('is_ca', this.form.issuer.is_ca)
        data.append('req', this.$store.state.file_obj)   

        let file_name = this.$store.state.file_name.split('.')[0]+'.cer'
        let req_params = {'filename': file_name, 'operation': 'sign'}
        
        this.$http.sign_crt_file(data, req_params)
        .then(response => {
          this.$store.commit({type: 'update_make_visible', data: false})
          this.blob(file_name, response.data)   
        })
        .catch(error => {
          this.$alert(error.message.content, error.message.title, {confirmButtonText: 'OK'})  
        })
      }

      else {
        let data = this.form
        let crt_file_name = this.form.basic_information.common_name + '.cer'  
        let key_file_name = this.form.basic_information.common_name + '.key'        
        let req_params = {'filename': crt_file_name, 'operation': 'make'}

        this.$http.make_crt_file(data, req_params)
        .then(response => {
          this.$store.commit({type: 'update_make_visible', data: false})
          this.blob(crt_file_name, response.data)             
          this.blob(key_file_name, response.data)               
        })
        .catch(error => {
          this.$alert(error.message.content, error.message.title, {confirmButtonText: 'OK'})  
        })
      }      
    }
  }
}
</script>
