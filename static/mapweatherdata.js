fetch('/api/city')
  .then((response) => response.json())
  .then((data) => {
    const lat = data.lat
    const lon = data.lon

    const tomTomApiKey = data.tomTomApiKey
    const api_key = data.api_key
    const applicationName = 'mapweatherdata'
    const applicationVersion = '6.4.0'
    const htmlDivId = 'graph'
    const openWeatherMapAttribution = 'Weather data provided by OpenWeatherMap'

    //Initializing the Application
    tt.setProductInfo(applicationName, applicationVersion)

    const tomTomMap = tt.map({
      key: tomTomApiKey,
      container: htmlDivId,
    })

    //Searching for a Location

    var city = { lng: lon, lat: lat }

    var map = tt.map({
      key: tomTomApiKey,
      container: htmlDivId,
      center: city,
      zoom: 13,
    })
    // adding layer

    var rainSource = {
      type: 'raster',
      tiles: [
        'https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid=' +
          api_key,
      ],
      tileSize: 256,
      minZoom: 0,
      maxZoom: 12,
      attribution: openWeatherMapAttribution,
    }

    var rainLayer = {
      id: 'rain_layer',
      type: 'raster',
      source: 'rain_source',
      layout: {
        visibility: 'visible',
      },
    }

    map.on('load', function () {
      map.addSource('rain_source', rainSource)
      map.addLayer(rainLayer)
    })
  })
