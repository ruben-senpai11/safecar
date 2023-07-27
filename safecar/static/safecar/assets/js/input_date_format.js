function dateToYMD(date) {
            
    var d = date.split('/')[0]+""
    var m = date.split('/')[1]+""
    var y = date.split('/')[2]+""
    return y + '-' + m+ '-' +d ;
  }
  window.onload = function(){
    my_dates= document.querySelectorAll("input[type=date]");
    my_dates.forEach(function(my_date,key,arr){
      dateStr =dateToYMD(my_date.getAttribute("value"))
      my_date.setAttribute('value',dateStr)
       
    })
  }
       