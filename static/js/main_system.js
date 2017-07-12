var img=document.getElementById("img");
      img.style.display='none';
      var table=document.getElementById("table");
      table.style.display='none';
      var loading=document.getElementById("loading");
      loading.style.display='none';
      var btn=document.getElementById("btn_search");
      btn.addEventListener("click", classify_system);

    function readURL(input) {
      if (input.files && input.files[0]) {
          var reader = new FileReader();
          reader.onload = function (e) {
              var img = document.getElementById("img");
              img.style.display='block';
              img.src=e.target.result;
              var bytes = new Uint2Array(img.src);
              console.log(bytes.)

              table.innerHTML="";
              loading.style.display='block';
              var url="classify_system?imageurl=" + bytes;
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

          };

          reader.readAsDataURL(input.files[0]);
      }
  }    