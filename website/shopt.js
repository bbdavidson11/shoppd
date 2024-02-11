document.getElementById('uploadBtn').addEventListener('click', function() {
    // Add your logic to upload the vision board
    alert('Upload functionality not implemented!');
});
document.getElementById('uploadBtn').addEventListener('click', function() {
    document.getElementById('fileInput').click(); // Simulate click on the actual file input
});

document.getElementById('fileInput').addEventListener('change', function() {
    // This function will run when the user selects a file
    const file = this.files[0];
    if (file) {
        console.log('File chosen:', file);
        // You can add code here to handle the file upload process
    }
});
