// =====================================================
// VWAP SUPERTREND BOT
// CHART.JS MANAGER
// BYBIT V5
// =====================================================


let priceChart = null;



// =====================================================
// LOAD CANDLES
// =====================================================

async function loadChart(){


    try{


        const response = await fetch(
            "/api/candles"
        );


        const data = await response.json();



        if(
            !data.result ||
            !data.result.list
        ){

            return;

        }



        let candles =
            data.result.list;



        candles.reverse();



        let labels = [];

        let prices = [];

        let volumes = [];




        candles.forEach(c=>{


            labels.push(

                new Date(

                    Number(c[0])

                ).toLocaleTimeString()

            );



            prices.push(

                Number(c[4])

            );



            volumes.push(

                Number(c[5])

            );


        });





        drawChart(

            labels,

            prices

        );



    }


    catch(e){


        console.log(

            "CHART ERROR",

            e

        );


    }


}








// =====================================================
// DRAW
// =====================================================

function drawChart(

    labels,

    prices

){



    const canvas =

        document.getElementById(

            "chart"

        );



    if(!canvas)

        return;







    if(priceChart == null){



        priceChart = new Chart(

            canvas,

            {


            type:"line",



            data:{


                labels:labels,



                datasets:[{


                    label:"BTCUSDT",


                    data:prices,


                    borderWidth:2,


                    tension:0.2,


                    pointRadius:0



                }]



            },



            options:{


                responsive:true,


                animation:false,


                interaction:{


                    intersect:false,


                    mode:"index"


                },



                plugins:{


                    legend:{


                        display:true


                    }


                },



                scales:{


                    x:{


                        ticks:{


                            maxTicksLimit:10


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



        priceChart.data.labels = labels;



        priceChart.data.datasets[0].data = prices;



        priceChart.update();



    }



}








// =====================================================
// AUTO UPDATE
// =====================================================


setInterval(

    loadChart,

    5000

);



loadChart();
