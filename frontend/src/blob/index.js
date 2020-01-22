function blob(filename, file) {
  var blob = new Blob([file])
  
  if (window.navigator.msSaveOrOpenBlob) {
    navigator.msSaveBlob(blob, filename)
  }
  
  else {
    var a = document.createElement('a')
    a.download = filename
    a.href = window.URL.createObjectURL(blob)
    a.click()
  } 
}

export {blob}