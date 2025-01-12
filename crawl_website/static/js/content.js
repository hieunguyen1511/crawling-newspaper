function getData() {
  var title = localStorage.getItem("title");
  var content = localStorage.getItem("content");
  var img = localStorage.getItem("img");
  document.title = `Nội dung trang báo "${title}"`;
  document.querySelector;
  //   document.getElementById("head").innerHTML +=
  //     '<link rel="shortcut icon" href="imgs/icons/' + index + '.ico">';
  var h3 = document.getElementById("title-web");
  h3.innerHTML = `Nội dung bài báo "${title}"`;
  var p = document.getElementById("content-web");
  p.innerHTML = content;
  var image = document.getElementById("img-web");
  image.title = `Hình ảnh bài báo "${title}"`;
  image.src = img;
}

getData();
