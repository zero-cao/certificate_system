<template>
<div id="make">
  <el-dialog width="50%" title="Make certificate" :before-close="closeDialog" :visible.sync="makeVisible">
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
            <el-input v-model="form.subject.basic_information.common_name" clearable></el-input>
          </el-form-item>

          <el-form-item label="Country Name">
            <el-select v-model="form.subject.basic_information.country">
              <el-option label="CN/China" value="CN"></el-option>
              <el-option label="US/America" value="US"></el-option>               
            </el-select>
          </el-form-item>

          <el-form-item label="Province">
            <el-input v-model="form.subject.basic_information.province" clearable></el-input>
          </el-form-item>

          <el-form-item label="Locality">
            <el-input v-model="form.subject.basic_information.locality" clearable></el-input>
          </el-form-item>

          <el-form-item label="Organization Name">
            <el-input v-model="form.subject.basic_information.organization" clearable></el-input>
          </el-form-item>

          <el-form-item label="Organization Unit">
            <el-input v-model="form.subject.basic_information.unit" clearable></el-input>
          </el-form-item>   
        </el-tab-pane>

        <el-tab-pane v-if="! enableSign" label="SAN">
          <el-form-item label="Subject Alternative Names">
            <div v-for="(alias_name, index) in form.subject.extensions.alias_names" :key="index">
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
            <el-checkbox-group v-model="form.subject.extensions.key_usages">
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
            <el-checkbox-group v-model="form.subject.extensions.extended_key_usages">
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
            <el-select v-model="form.subject.key.key_type">
              <el-option label="RSA" value="rsa"></el-option>
              <el-option label="DSA" value="dsa" disabled></el-option>
              <el-option label="ECDSA" value="ecdsa" disabled></el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="Length">
            <el-select v-model="form.subject.key.key_length">
              <el-option label="1024" :value="1024"></el-option>
              <el-option label="2048" :value="2048"></el-option>
              <el-option label="3072" :value="3072"></el-option>
              <el-option label="4096" :value="4096"></el-option>          
            </el-select>
          </el-form-item>	

          <el-form-item label="Password">
            <el-input type="password" v-model="form.subject.key.password" clearable></el-input>
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
  name: 'DialogMake',
  components: { Upload }, 
  data () {
		return {
      makeVisible: true,
      enableSign: false,
      form: {
				issuer: {
					ca: 'wenca-rootca',
					valid_year: 1,
					hash_alg: 'sha256',
					is_ca: false
        },
        subject: {
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
          }   
        }
 
      }  
    }
  },
  methods: {
    closeDialog () {
      this.$store.commit({type: 'update_component_name', data: ''})        
      this.$store.commit({type: 'update_pending_file', data: {}})
    },      
    removeSAN (item) {
      var index = this.form.subject.extensions.alias_names.indexOf(item);
      if (index !== -1) {
        this.form.subject.extensions.alias_names.splice(index, 1);
      }
    },
    addSAN (type) {
      this.form.subject.extensions.alias_names.push({type: type, value: ''});
    },    
		onSubmit () {
      if (this.enableSign) {
        let file_obj = this.$store.state.pending_file
        if (JSON.stringify(file_obj) == '{}') {
          this.$message.warning('Certificate signing request file must be provided')
          return false
        }
        if (file_obj.raw.type != '') {
          this.$message.warning('Certificate signing request file mime type is invalid')
          return false
        }        

        let form_data = new FormData()
        form_data.append('ca', this.form.issuer.ca)
        form_data.append('valid_year', this.form.issuer.valid_year)
        form_data.append('hash_alg', this.form.issuer.hash_alg)
        form_data.append('is_ca', this.form.issuer.is_ca)
        form_data.append('req', file_obj.raw)   

        let filename = file_obj.name.split('.')[0]+'.cer'
        this.$http.sign_crt_file(form_data)
        .then(response => {
          this.$store.commit({type: 'update_component_name', data: ''})      
          this.blob(filename, response.crt)   
        })
        .catch(error => {
          this.$alert(error.message.content, error.message.title, {confirmButtonText: 'OK'})  
        })
      }

      else {
        let json_data = this.form
        if (json_data.subject.basic_information.common_name === '') {
          this.$message.warning('Certificate common name must be provided')
          return false
        }
        if (json_data.subject.basic_information.province === '') {
          this.$message.warning('Certificate province must be provided')
          return false
        }
        if (json_data.subject.basic_information.locality === '') {
          this.$message.warning('Certificate locality must be provided')
          return false
        }
        if (json_data.subject.basic_information.organization === '') {
          this.$message.warning('Certificate organization must be provided')
          return false
        }
        if (json_data.subject.basic_information.unit === '') {
          this.$message.warning('Certificate unit must be provided')
          return false
        }
        if (json_data.subject.key.password === '') {
          this.$message.warning('Certificate private key\'s password must be provided')
          return false
        }
                                               
        let crt_filename = this.form.subject.basic_information.common_name + '.cer'  
        let key_filename = this.form.subject.basic_information.common_name + '.key'        
        this.$http.make_crt_file(json_data)
        .then(response => {
          this.$store.commit({type: 'update_component_name', data: ''})      
          this.blob(crt_filename, response.crt)             
          this.blob(key_filename, response.key)               
        })
        .catch(error => {
          this.$alert(error.message.content, error.message.title, {confirmButtonText: 'OK'})  
        })
      }      
    }
  }
}
</script>
