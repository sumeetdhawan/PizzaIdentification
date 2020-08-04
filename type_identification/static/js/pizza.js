// HOME.HTML MODAL
document.getElementById("imageupload").addEventListener("click", function(){
    document.querySelector(".bg-modal").style.display = "flex";
});
document.querySelector(".close").addEventListener("click", 
function(){
    document.querySelector(".bg-modal").style.display = "none"
})
// LOADS IMAGES FROM LOCAL FILE (home.html)
function previewFile() {
    const preview = document.querySelector('img');
    const file = document.querySelector('input[type=file]').files[0];
    const reader = new FileReader();
    reader.addEventListener("load", function () {
      // convert image file to base64 string
      preview.src = reader.result;
    }, false);
    if (file) {
      reader.readAsDataURL(file);
    }
  }
//IMAGES.HTML post request to app.py
function sendurl(){   
var img = document.getElementById('imageForm').src;
var xhr = new XMLHttpRequest();
xhr.open("POST", '/dbresult', true);
xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
xhr.onreadystatechange = function() { 
    if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
    }
}
xhr.send(img);
}
// // IMAGES.HTML MODAL
// images = [
//   'https://kafuitrainingimage.s3.us-east-2.amazonaws.com/14.jpg', 
//   'https://kafuitrainingimage.s3.us-east-2.amazonaws.com/67.jpg', 
//   'https://kafuitrainingimage.s3.us-east-2.amazonaws.com/129.jpg', 
//   'https://kafuitrainingimage.s3.us-east-2.amazonaws.com/86.jpg', 
//   'https://kafuitrainingimage.s3.us-east-2.amazonaws.com/5.jpg', 
//   'https://kafuitrainingimage.s3.us-east-2.amazonaws.com/117.jpg', 
//   'https://kafuitrainingimage.s3.us-east-2.amazonaws.com/89.jpg', 
//   'https://kafuitrainingimage.s3.us-east-2.amazonaws.com/8.jpg', 
//   'https://kafuitrainingimage.s3.us-east-2.amazonaws.com/118.jpg', 
//   'https://kafuitrainingimage.s3.us-east-2.amazonaws.com/11.jpg'
//   ]
// document.getElementById("upload-image").addEventListener("click", function(){
//     document.getElementById("imageForm").src = document.getElementById("upload-image").src;
//     console.log(document.getElementById("upload-image").src)
//     alert("smile")
// })
// function loadimage(e){
//     document.getElementById("imageForm").src = HTMLImageElement.src;
//     alert("smile")
// }
function loadimage(){
  // var modal = document.querySelector("the-modal")
  var images = document.querySelectorAll("display-image");
  var modalImg = document.getElementById("imageForm");
  for(let i = 0; i < images.length; i++){
     images[i].addEventListener("click",(e) =>{
       modalImg.src = e.target.src;
       alert("the new function worked")
     })
    }     
    // console.log(document.getElementById("upload-image").src)
    // alert("this is from loadimage function")
}
function push(event){
  var displayedImage = document.querySelector('.image-Form');
  displayedImage.src = event.target.src;
  console.log(displayedImage.src)
}