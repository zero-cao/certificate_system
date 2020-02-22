<template>
<div id="remove">
</div>  
</template>

<script>
export default {
  name: 'DialogRemove',
  created () {
    let filename = this.$store.state.selected_file.filename
    this.$confirm(filename, 'Delete Certificate File ?', {
      confirmButtonText: 'Sure',
      cancelButtonText: 'Cancel',
      type: 'warning'
    })
    .then(() => {
      this.$http.remove_crt_file(filename)
      .then(() => {
        this.$router.go(0)
      })
      .catch(error => {
        this.$alert(error.message.content, error.message.title, {confirmButtonText: 'OK'})           
      })          
    })
    .catch(() => {}) 
  }
}
</script>

<style>

</style>