// =====================================================
// VWAP SUPERTREND BOT
// CANDLE CHART
// =====================================================


let candleChart = null;



async function loadChart(){


try{


let response =
await fetch("/api/candles");



let data =
await response.json();



if(!data.result)

return;



let list =
data.result.list;



list.reverse();



let candles=[];



list.forEach(c=>{


candles.push({

x:
Number(c[0]),


o:
Number(c[1]),


h:
Number(c[2]),


l:
Number(c[3]),


c:
Number(c[4])


});


});






drawCandles(candles);



}

catch(e){

console.log(

"CHART ERROR",

e

);


}



}








function drawCandles(data){



let ctx =
document
.getElementById("chart");



if(!ctx)

return;






if(!candleChart){



candleChart =
new Chart(

ctx,

{


type:"candlestick",



data:{


datasets:[{


label:"BTCUSDT",


data:data



}]



},



options:{


responsive:true,


animation:false,



scales:{


x:{


type:"time",


time:{


unit:"minute"


}



},



y:{


beginAtZero:false


}



}



}



}



);



}


else{


candleChart.data.datasets[0].data=data;


candleChart.update();


}



}








setInterval(

loadChart,

5000

);


loadChart();
