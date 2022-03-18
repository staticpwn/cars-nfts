response_desplay = document.getElementById("response")
input_val = document.getElementById("yo")
token = document.getElementsByName("csrfmiddlewaretoken")[0]
// roller = document.getElementById("roller")




function send()
{

    if (window.confirm("login?"))
    {
    
      


      var get_hash = new XMLHttpRequest();

      get_hash.open("GET", 'http://127.0.0.1:8000/cars/test')
      get_hash.addEventListener("load", () =>
      {
        hash = get_hash.responseText
        
        params = {
          "input": input_val.value,
          "hash" : hash
        }


        var send_signed = new XMLHttpRequest();
    
        send_signed.open( "POST", 'http://127.0.0.1:8000/cars/test'+formatParams( params ), false); // false for synchronous request // + formatParams( params )
        send_signed.setRequestHeader("X-CSRFToken", getCookie("csrftoken")); 
        send_signed.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
        send_signed.addEventListener("load", () => {
          
          
          alert(JSON.parse(send_signed.responseText));
          location.reload();
        })
        send_signed.send( null );
        
      })
      
      get_hash.send( null )

    } else {
      response_desplay.innerHTML = "User rejected the login request."
    }
}



function formatParams( params ){
    return "?" + Object
          .keys(params)
          .map(function(key){
            return key+"="+encodeURIComponent(params[key])
          })
          .join("&")
  }

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

  function get_time(){
    console.log(+ new Date());
  }
  


  