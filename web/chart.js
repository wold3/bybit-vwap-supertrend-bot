//////////////////////////////////////////////////////
// VWAP SUPERTREND BOT
// BYBIT V5 CANDLE CHART
//////////////////////////////////////////////////////


// ==================================================
// GLOBAL
// ==================================================

let candleChart = null;





// ==================================================
// LOAD CANDLES
// ==================================================

async function loadChart(){


    try{


        const response = await fetch(

            "/api/candles"

        );


        const json = await response.json();



        if(
            !json.result ||
            !json.result.list
        ){

            console.log(
                "NO CANDLE DATA"
            );

            return;

        }



        let list =

            json.result.list;



        list = list.reverse();



        let candles = [];



        list.forEach(c=>{


            candles.push({


                x:Number(c[0]),


                o:Number(c[1]),


                h:Number(c[2]),


                l:Number(c[3]),


                c:Number(c[4])


            });


        });




        console.log(

            "CANDLES",

            candles.length

        );



        drawChart(

            candles

        );



    }


    catch(error){


        console.log(

            "CANDLE ERROR",

            error

        );


    }


}









// ==================================================
// DRAW CHART
// ==================================================

function drawChart(data){



    const canvas =

        document.getElementById(

            "chart"

        );



    if(!canvas)

        return;






    if(candleChart){



        candleChart.data.datasets[0].data = data;



        candleChart.update();



        return;


    }







    candleChart = new Chart(

        canvas,


        {


        type:"candlestick",



        data:{


            datasets:[{


                label:

                "BTCUSDT",



                data:data,



                borderWidth:1



            }]


        },





        options:{


            responsive:true,


            maintainAspectRatio:false,



            animation:false,



            parsing:false,



            plugins:{


                legend:{


                    display:true


                }


            },





            scales:{



                x:{


                    type:"time",



                    time:{


                        unit:"minute"


                    },



                    ticks:{


                        maxTicksLimit:12


                    }



                },




                y:{


                    position:"right",



                    ticks:{


                        callback:function(value){


                            return value.toFixed(0);


                        }


                    }



                }



            }



        }



        }


    );



}









// ==================================================
// AUTO UPDATE
// ==================================================

setInterval(

    loadChart,

    5000

);



loadChart();
