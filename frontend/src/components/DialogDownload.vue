<template>
<div id="download">
</div>  
</template>

<script>
export default {
  name: 'DialogDownload',
  created () {
    let filename = this.$store.state.selected_file.filename
    this.$http.download_crt_file(filename)
    .then(response => {
      this.blob(filename, response) 
      this.$store.commit({type: 'update_component_name', data: ''})      
    })
    .catch(error => {
      this.$alert(error.message.content, error.message.title, {confirmButtonText: 'OK'})                     
    })    
  }
}
</script>

<style>

</style>