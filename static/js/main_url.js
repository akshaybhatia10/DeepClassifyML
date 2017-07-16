var img=document.getElementById("img");
img.style.display='none';
var table=document.getElementById("table");
table.style.display='none';
var loading=document.getElementById("loading");
loading.style.display='none';
var btn=document.getElementById("btn_search");
btn.addEventListener("click", classify_url);
var img_url=document.getElementById("img_url");
function classify_url() {
    table.innerHTML="";
    img.style.display='block';
    loading.style.display='block';
    img.src=img_url.value;
    var url="classify_url?imageurl=" + img_url.value;
    $.get(url, function(data, status){
      table.style.display='block';
      loading.style.display='none';
      for(var i=data.results.length-1;i>=0;i--){
        var row = table.insertRow(0);
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        cell1.innerHTML = data.results[i].class_name;
        cell2.innerHTML = data.results[i].score;
      }
      var row = table.insertRow(0);
      var cell1 = row.insertCell(0);
      var cell2 = row.insertCell(1);
      cell1.innerHTML = "<b>Class Name</b>";
      cell2.innerHTML = "<b>Score</b>";
    });
}
