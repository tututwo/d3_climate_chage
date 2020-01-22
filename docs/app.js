async function drawmap(){

      const countryShapes = await d3.json('./../world-geojson.json')

      const dataset = await d3.csv("../country_year_temp.csv")
//*////////////////?       /////////////////////////////////////////////////////////////////////////////////
//!////////////? Data Manipulation//////////////////////////////////////////////////////////////////////////
//*////////////////?       /////////////////////////////////////////////////////////////////////////////////

      //TODO we want an easy to look up forest using country names
      const countryNameAccessor = d => d.properties["NAME"]
      const countryIdAccessor = d => d.properties["ADM0_A3_IS"]
     // const metric = "20"

      let metricDataByCountry = {}
      
      dataset.forEach(d => {
            if (d['Year'] == 2000)
            return metricDataByCountry[d['Country Code']] = +d['Mean_temp_per_year'] || 0
      })  // making an object
//*////////////////?       /////////////////////////////////////////////////////////////////////////////////
//!////////////? Define Dimensions /////////////////////////////////////////////////////////////////////////
//*////////////////?       /////////////////////////////////////////////////////////////////////////////////

      let dimensions ={
            width:window.innerWidth*0.9,
            margin:{
                  top:10, right:10, bottom:10, left:10
            }
      }
      dimensions.boundedWidth = dimensions.width - dimensions.margin.left - dimensions.margin.right



      }

      

      drawmap()