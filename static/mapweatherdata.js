//Initializing the Application
tt.setProductInfo('mapweatherdata', '1.0.0')

const tomTomMap = tt.map({
  key: 'l5iRb3wJ9UOSekmviI5BVAdbxGbNfJo7',
  container: 'graph',
})

//Searching for a Location
tt.services
  .fuzzySearch({
    key: tomTomApikey,
    query: queryText,
  })
  .go()
  .then(centerAndZoom)
  .catch(function (error) {
    alert('Could not find location (' + queryText + '). ' + error.message)
  })

function centerAndZoom(response) {
  tomTomMap.flyTo({
    center: response.results[0].position,
    zoom: zoomLevel,
  })
}
