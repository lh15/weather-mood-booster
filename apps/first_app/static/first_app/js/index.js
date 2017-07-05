$(document).ready(function () {

    if ("geolocation" in navigator) { //check geolocation available 
        //try to get user current location using getCurrentPosition() method
        navigator.geolocation.getCurrentPosition(function (position) {

            var lat = position.coords.latitude;
            var lon = position.coords.longitude;
            console.log("Found your location \nLat : " + position.coords.latitude + " \nLang :" + position.coords.longitude);

            // $.post("/get_weather", { lat: position.coords.latitude, lon: position.coords.longitude });
            $.ajax({
                url: "/get_weather",
                type: "POST",
                data: { lat: position.coords.latitude, lon: position.coords.longitude },
                success: function (response) { },
                complete: function () { },
                error: function (xhr, textStatus, thrownError) {
                    alert("error doing something");
                }
            });

            // var url = "http://api.openweathermap.org/data/2.5/weather?lat=" + lat + "&lon=" + lon + "&APPID=91d2fecd81cd087af9adf3d373fd0276";

            // // make api request
            // $.get(url, function (res) {

            //     // collect data into variables and inject to DOM
            //     var kelvin = res.main.temp;
            //     var fahrenheit = Math.floor(((kelvin - 273.15) * 9 / 5) + 32) + "° F";
            //     var celsius = Math.floor(kelvin - 273.15) + "° C";
            //     var temperature = kelvin + "° K - " + fahrenheit + " - " + celsius;
            //     $("#display").html("<h1>" + res.name + "</h1><p>" + temperature + "</p>");

            // }, 'json');
            // // don't forget to return false so the page doesn't refresh
            // return false;

        });
    } else {
        console.log("Browser doesn't support geolocation!");
    }




});