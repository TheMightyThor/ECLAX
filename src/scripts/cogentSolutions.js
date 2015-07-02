
function validateForm()
{
var x=document.forms["loginform"]["email"].value;
var y=document.forms["loginform"]["user_name"].value;
var atpos=x.indexOf("@");
var dotpos=x.lastIndexOf(".");
if (atpos<1 || dotpos<atpos+2 || dotpos+2>=x.length)
  {
  alert("Please provide a valid email address");
  return false;
  }
  else if (y === "greatsite"){
	  setCookie('profLogin', .1);
  }
   else if (y ==="friend"){
	  setCookie('login', .1) 
	  }
   else {
	   alert("Invalid user name");
	   return false;
   }
  }


function setCookie(cname,exdays)
{
var d = new Date();
d.setTime(d.getTime()+(exdays*24*60*60*1000));
var expires = "expires="+d.toGMTString();
var cvalue = document.forms["loginform"]["user_name"].value;
document.cookie = cname + "=" + cvalue + "; " + expires;
}

function getCookie(cname)
{
var name = cname + "=";
var ca = document.cookie.split(';');
for(var i=0; i<ca.length; i++) 
  {
  var c = ca[i].trim();
  if (c.indexOf(name)==0) return c.substring(name.length,c.length);
  }
return "";
}

function checkCookie()
{
var profUser = getCookie("profLogin");
var regUser = getCookie("login");

if (profUser!=""){
  $("#nonProfBody").remove();
  }
else if (regUser != "") 
  {
  $("#profBody").remove();
  }
else{
	window.location.assign("/");
}
}
var looper;
var degrees = 0;
function spinWheels(topW, bigW, bottomW, speed)
{
	var topWheel = document.getElementById(topW);
	var middleWheel = document.getElementById(bigW);
	var bottomWheel = document.getElementById(bottomW);
	
	middleWheel.style.WebKittransform = "rotate("+degrees+"deg)";
	looper = setTimeout('rotateAnimation(\''+bigW+'\','+speed+')',speed);
	degrees++;
	if(degrees > 259){
		degrees = 1;
	}
	}
	
	
