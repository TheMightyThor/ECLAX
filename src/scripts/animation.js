var deg = 0;
var negDeg = 0;
var looper;
var speed = 15;
	function spinWheels(){
		var bigW = document.getElementById("bigWheel");
		var topW = document.getElementById("topWheel");
		var bottomW = document.getElementById("bottomWheel");
		bigW.style.WebkitTransform="rotate("+deg+"deg)";
		topW.style.WebkitTransform="rotate("+negDeg+"deg)";
		bottomW.style.WebkitTransform="rotate("+negDeg+"deg)";
		deg++;
		negDeg--;
		if(deg > 359){
			deg = 1;
		}
		
		if(negDeg < -359){
			nedDeg = -1;
		}
		looper = setTimeout('spinWheels()',speed);
		}
	
