fetch('/api/city')
  .then((response) => response.json())
  .then((data) => {
    const lat = document.querySelector('script[lat]').getAttribute('lat')
    const lon = document.querySelector('script[lon]').getAttribute('lon')

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

      // Set up event listener for moveend event
      map.on('moveend', function () {
        // Delay subsequent API requests by 1 second (1000 milliseconds)
        throttleAPIRequests()
      })

      // Initial API request
      throttleAPIRequests()
    })

    function throttleAPIRequests() {
      // Clear the previous timer, if any
      clearTimeout(throttleTimer)

      // Set a timer to make the API request after the specified delay
      throttleTimer = setTimeout(makeAPIRequest, 1000) // Delay in milliseconds
    }

    function makeAPIRequest() {
      // Fetch the tile from the API
      fetch(rainSource.tiles[0] + api_key)
        .then((response) => {
          if (!response.ok) {
            throw new Error('Network response was not ok')
          }
          return response.blob()
        })
        .then((tileBlob) => {
          // Store the tile in cache (localStorage)
          const tileCacheKey =
            'rain_tile_' +
            map.getZoom() +
            '_' +
            map.getCenter().lng +
            '_' +
            map.getCenter().lat
          localStorage.setItem(tileCacheKey, tileBlob)

          const tileUrl = URL.createObjectURL(tileBlob)

          // Update the rain layer tile URL
          rainSource.tiles = [tileUrl]

          // Update the map layer
          map.removeLayer('rain_layer')
          map.removeSource('rain_source')
          map.addSource('rain_source', rainSource)
          map.addLayer(rainLayer)
        })
        .catch((error) => {
          console.log('Error fetching tile:', error)
        })
    }
  })
