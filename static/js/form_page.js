function togglefileupload() {
    var checkbox = document.getElementById('PDFSerachTool');
    var input_file = document.getElementById('pdf-file');

    if (checkbox.checked) {
      input_file.style.display = 'inline';
      input_file.required = true;
    } else {
      input_file.style.display = 'none';
    }
  }