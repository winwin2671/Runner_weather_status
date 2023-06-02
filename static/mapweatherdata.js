const applicationName = 'mapweatherdata'
const applicationVersion = '1.0.0'
const tomTomApiKey = document.currentScript.getAttribute('tomTomApiKey')
const htmlDivId = 'graph'

//Initializing the Application
tt.setProductInfo(applicationName, applicationVersion)

const tomTomMap = tt.map({
  key: tomTomApiKey,
  container: htmlDivId,
})

//Searching for a Location
fetch('/api/city')
  .then((response) => response.json())
  .then((data) => {
    const queryText = data.city
    console.log('Query Text:', queryText)

    // Perform the fuzzy search with the retrieved query text
    tt.services
      .fuzzySearch({
        key: tomTomApiKey,
        query: queryText,
      })
      .go()
      .then(centerAndZoom)
      .catch((error) => {
        alert('Could not find location (' + queryText + '). ' + error.message)
      })
  })

function centerAndZoom(response) {
  tomTomMap.flyTo({
    center: response.results[0].position,
    zoom: 0,
  })
}
