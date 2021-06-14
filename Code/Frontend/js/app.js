const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

let activeDrinks = [];

const init = () => {
    if(document.querySelector('.js-temp-sensors')){
        handleData(`http://${lanIP}/api/v1/latestdata`, showSensorData, null, "GET", null)
        handleData(`http://${lanIP}/api/v1/get20history`, showLastHistory, null, "GET", null)
        handleData(`http://${lanIP}/api/v1/getdaily`, showDailyCocktails, null, "GET", null)
    }
    
}

const startCleaning = () => {
    
    socket.emit("F2B_start_cleaning");
}

const showLastHistory = (data) => {
    const $historyTable = document.querySelector(".js-historyTable");
    let content = "";
    data.history.forEach(element => {
        let date = element.timestamp
        content += `<tr>
            <td>${element.name}</td>
            <td>${element.timestamp}</td>
        </tr>`;
    });
    $historyTable.innerHTML += content;
}

const showSensorData = (data) => {
    const $sensor = document.querySelector('.js-temp-sensors')
    const length = data.sensordata.length / 2
    for (let i = 0; i < length; i++) {
        $sensor.innerHTML += `<div class="js-sensor__display o-layout__item u-1-of-2 mb-5">
            <div
                class="c-tempdisplay o-layout o-layout--gutter o-layout--align-center o-layout--justify-center">
                <!-- <div class="u-1-of-1">&nbsp;</div> -->
                <div class="c-tempdisplay__container">
                    <p class="js-temp o-layout__item u-1-of-1">15°c</p>
                    <p class="js-drink o-layout__item u-1-of-1">Limoncello</p>
                    <p class="js-amount o-layout__item u-1-of-1">20%</p>
                </div>
            </div>
        </div>`;
    }
    let temps = [];
    let ultrasone = [];
    let dranken = [];
    const $sensors = document.querySelectorAll('.js-sensor__display');
    data.dranken.forEach(element => {
        dranken.push(element.naam)
        activeDrinks.push(element.id)
    })
    data.sensordata.forEach(element => {
        if (element.sensor_type == "temp") {
            temps.push(element.value.toFixed(2))
        } else {
            ultrasone.push(element.value.toFixed(2))
        }
    });
    let sensorIndex = 0;
    $sensors.forEach(element => {
        const $temp = element.querySelector('.js-temp');
        const $amount = element.querySelector('.js-amount');
        const $drink = element.querySelector('.js-drink');
        $temp.innerHTML = temps[sensorIndex] + '°c';
        $amount.innerHTML = ultrasone[sensorIndex] + 'L';
        $drink.innerHTML = dranken[sensorIndex];
        sensorIndex++;
    })
    const jsonobject = {
        dranken: activeDrinks
    };
    handleData(`http://${lanIP}/api/v1/getcocktails`, showPossibleCocktails, null, "POST", JSON.stringify(jsonobject))
}

const showPossibleCocktails = (data) => {
    let cid = 0;
    const $table = document.querySelector('.js-cocktailTable');
    let dranken = [];
    let content = "";
    let name = "";
    data.cocktails.forEach(element => {
        if (cid == 0) {
            cid = element.id
            name = element.cocktailnaam
        }
        if (cid != element.id) {
            content += `<tr>
                                    <td>${name}</td><td><ul>`;
            dranken.forEach(element => {
                content += `<li>${element}</li>`;
            });
            content += `</ul></td><td><button onclick="makeCocktail(${cid})" class="o-button">Maken</button></td></tr>`;
        } else {
            name = element.cocktailnaam
            dranken.push(`${element.dranknaam} (${element.percentage.toFixed(0)}%)`);
        }
    })
    content += `<tr>
                            <td>${name}</td><td>`;
    dranken.forEach(element => {
        content += `<li>${element}</li>`;
    });
    content += `</td><td><button onclick="makeCocktail(${cid})" class="o-button">Maken</button></td></tr>`;
    console.log(content)
    $table.innerHTML += content;
}

const makeCocktail = (id) => {
    socket.emit("F2B_make_cocktail", { cocktail_id: id });
}

const stopDispense = () => {
    socket.emit("F2B_emergency_stop")
}

const listenToSocket = function () {
    socket.on("connected", function () {
        console.log("verbonden met socket webserver");
    });

    socket.on("B2F_cocktail_error", function (jsonObject) {
        console.log(jsonObject.message);
    });
    socket.on("B2F_cocktail_history", function (jsonObject) {
        jsonObject = JSON.parse(jsonObject.cocktails);
        console.log(jsonObject)
        const $historyTable = document.querySelector(".js-historyTable");
        let content = `<tbody><tr>
                            <th>Cocktail</th>
                            <th>Datum</th>
                        </tr>`;
        jsonObject.forEach(element => {
            let date = element.timestamp
            content += `<tr>
                <td>${element.name}</td>
                <td>${element.timestamp}</td>
            </tr>`;
        });
        content += "</tbody>";
        console.log(content)
        $historyTable.innerHTML = content;
        handleData(`http://${lanIP}/api/v1/getdaily`, showDailyCocktails, null, "GET", null)
        
    });
    socket.on("B2F_sensor_update", function(jsonObject){
        let temps = []
        let usone = []

        jsonObject.temps.forEach(element => {
            temps.push(element.toFixed(2))
        });
        jsonObject.usone.forEach(element => {
            usone.push(element.toFixed(2))
        })

        const $temps = document.querySelectorAll('.js-temp');
        const $usone = document.querySelectorAll('.js-amount');
        let i = 0;
        $temps.forEach(element => {
            element.innerHTML = `${temps[i]}°c`;
            i++;
        })
        i = 0;
        $usone.forEach(element => {
            element.innerHTML = `${usone[i]}L`;
            i++
        })
    })
    socket.on("B2F_cocktail_started", function (jsonObject) {
        console.log(jsonObject)
        if (jsonObject.status == "started") {
            document.querySelector(".o-button--danger").classList.remove("o-button--hidden")
        } else if (jsonObject.status == "stopped") {
            document.querySelector(".o-button--danger").classList.add("o-button--hidden")
        }
    });

    /* socket.on("B2F_status_lampen", function (jsonObject) {
      console.log("alle lampen zijn automatisch uitgezet");
      console.log("Dit is de status van de lampen");
      console.log(jsonObject);
      for (const lamp of jsonObject.lampen) {
        const room = document.querySelector(`.js-room[data-idlamp="${lamp.id}"]`);
        if (room) {
          const knop = room.querySelector(".js-power-btn");
          knop.dataset.statuslamp = lamp.status;
          clearClassList(room);
          if (lamp.status == 1) {
            room.classList.add("c-room--on");
          }
        }
      }
    });
  
    socket.on("B2F_verandering_lamp", function (jsonObject) {
      console.log("Er is een status van een lamp veranderd");
      console.log(jsonObject.lamp.id);
      console.log(jsonObject.lamp.status);
  
      const room = document.querySelector(`.js-room[data-idlamp="${jsonObject.lamp.id}"]`);
      if (room) {
        const knop = room.querySelector(".js-power-btn"); //spreek de room, als start. Zodat je enkel knop krijgt die in de room staat
        knop.dataset.statuslamp = jsonObject.lamp.status;
  
        clearClassList(room);
        if (jsonObject.lamp.status == 1) {
          room.classList.add("c-room--on");
        }
      }
    }); */
};

const showDailyCocktails = (data) => {
    document.querySelector("#chart").innerHTML = "";
    let amount = [];
    let dates = [];
    data.daily.forEach(element => {
        date = new Date(element.datum);
        let dd = date.getDate();
        let mm = date.getMonth() + 1;
  
        let yyyy = date.getFullYear();
        if (dd < 10) {
            dd = '0' + dd;
        }
        if (mm < 10) {
            mm = '0' + mm;
        }
        date = dd + '/' + mm + '/' + yyyy;
        amount.push(element.aantal);
        dates.push(date)
    })
    amount.reverse();
    dates.reverse();
    var options = {
        series: [{
        name: 'Aantal cocktails',
        data: amount
      }],
        chart: {
        type: 'bar',
        height: 350
      },
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: '55%',
          endingShape: 'rounded'
        },
      },
      dataLabels: {
        enabled: false
      },
      stroke: {
        show: true,
        width: 2,
        colors: ['transparent']
      },
      xaxis: {
        categories: dates,
      },
      yaxis: {
        title: {
          text: '# cocktails'
        }
      },
      fill: {
        opacity: 1
      },
      tooltip: {
        y: {
          formatter: function (val) {
            return val + " cocktails"
          }
        }
      }
      };
    
      var chart = new ApexCharts(document.querySelector("#chart"), options);
      chart.render();
}



document.addEventListener("DOMContentLoaded", function () {
    init();
    listenToSocket();
})