<template>
<div id="crt_make">
  <el-col :span="12">
    <el-form ref="form" :model="form" label-width="180px" class="demo-dynamic">
      <h3>Issuer</h3>
      <div class="issuer">      
        <el-form-item label="Certificate Authority">
          <el-select v-model="form.issuer.ca">
            <el-option label="wenca-rootca" value="wenca-rootca"></el-option>
            <el-option label="wenca-subca" value="wenca-subca"></el-option>
            <el-option label="wenca-grandca" value="wenca-grandca"></el-option>            
            <el-option label="self sign" value="SelfSign"></el-option>
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

      <h3>Basic Information</h3>
      <div class="subjectBasic">
        <el-form-item label="Common Name">
          <el-input v-model="form.basic_information.common_name" clearable></el-input>
        </el-form-item>

        <el-form-item label="Country Name">
          <el-input v-model="form.basic_information.country" clearable></el-input>
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
  name: 'CertificateMaking',
  data () {
		return {
      form: {
				issuer: {
					ca: 'wenca-rootca',
					valid_year: 1,
					hash_alg: 'sha256',
					is_ca: false
        },
        basic_information: {
					common_name: 'test.com',
					country: 'CN',
					province: 'Shanghai',
					locality: 'Xuhui',
					organization: 'Cisco',
					unit: 'Voice'
        },
        extensions: {
          alias_names: [
            {type: 'IPv4', value: '1.1.1.1'},
            {type: 'IPv6', value: '2001::1:1:1'},
            {type: 'DNS', value: 'ha.test.com'}
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
          key_length: 2048
        },
      },
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
			let data = this.form

      this.$http.crt_make(data, 'application/json')
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
