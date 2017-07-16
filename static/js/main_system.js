window.onload = doStuff;

    function doStuff() {
      var table=document.getElementById("table");
      table.style.display='none';
      var loading=document.getElementById("loading");
      loading.style.display='none';

        }

    function previewFile(){
       var preview = document.querySelector('img'); //selects the query named img
       var file    = document.querySelector('input[type=file]').files[0]; //same as here
       var reader  = new FileReader();

               reader.onloadend = function () {
                   image_url = reader.result 
                   preview.src = image_url;
                   console.log(image_url)
               }

               if (file) {
                   reader.readAsDataURL(file); //reads the data as a URL
               } else {
                   preview.src = "";
               }
          }

    function classify_system() {
              console.log("Clicked")
              table.innerHTML = "" ;
              loading.style.display='block';
              var url="classify_system?imageurl=" + image_url;
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

       previewFile();