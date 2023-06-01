//Initializing the Application
tt.setProductInfo(mapweatherdata, applicationVersion)

const tomTomMap = tt.map({
  key: tomTomApiKey,
  container: htmlDivId,
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
