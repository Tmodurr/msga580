
const basemaps = {

    "esriWorldStreetmap": {
                                "id": "esri-world-streetmap", 
                                "name": "ESRI World Streetmap 2D",
                                "url": "http://server.arcgisonline.com/arcgis/rest/services/ESRI_StreetMap_World_2D/MapServer"
                            },
    "usTopoMaps": {
                                "id": "us-topo-maps", 
                                "name": "US Topo Maps",
                                "url": "http://server.arcgisonline.com/arcgis/rest/services/USA_Topo_Maps/MapServer"
                            },
    "usPopChange": {
                                "id": "us-pop-change", 
                                "name": "US Pop Change (1990-2000)",
                                "url": "http://server.arcgisonline.com/arcgis/rest/services/Demographics/USA_1990-2000_Population_Change/MapServer"
                            },
};

var currentResponse;

var xmin, 
    xmax, 
    ymin, 
    ymax; 

var currentXmin, 
    currentXmax, 
    currentYmin, 
    currentYmax;

var description; 



// FUNCTIONS ----------------------------------------------------------------------------------------------------------------------------------------

function init(){

    updateTitle(basemaps.esriWorldStreetmap);
    addBasemapOptions(basemaps);
    let basemap = document.getElementById('map-selector').value;
    let basemapURL = getBaseURL(basemap);
    let basemapMetadataURL = encodeURI(basemapURL + "?f=pjson"); 
    sendHttpRequest(basemapMetadataURL);  
    setTimeout(function(){
        zoomToFullExtent();
     }, 1000);


}

function addBasemapOptions(basemaps){

    let basemapOptionControl = document.getElementById('map-selector');

    for (var key in basemaps) {
        if (basemaps.hasOwnProperty(key)) {
            let basemap = basemaps[key];

            let basemapChoice = document.createElement("option");
                basemapChoice.value = basemap.id;
                basemapChoice.text = basemap.name;
                basemapChoice.className = "map-selector-option";
                
            basemapOptionControl.appendChild(basemapChoice);
        }
    }
}

function updateTitle(basemap){

    let title = document.getElementById('map-title');

    if (basemap.id === "esri-world-streetmap"){
        title.innerHTML = 'ESRI World Street Map (2D)';
        return
    }
    else if (basemap.id === "us-topo-maps"){
        title.innerHTML = 'USA Topo Maps';
        return
    }
    else if (basemap.id === "us-pop-change"){
        title.innerHTML = "USA Population Change (1990-2000)";
        return
    }
  
}

function getBaseURL(basemapId){

    for (var key in basemaps) {
            if (basemaps.hasOwnProperty(key)) {
                let basemap = basemaps[key];
                if(basemap.id === basemapId){
                    return basemap.url;
                    
                }
            }
        }

}

// MAP ACTIONS
function zoomIn(){
    console.log('Zoom in brah');

    //get currentURL of basemap

    //bring in local xmin
    let length = currentXmax - currentXmin; 
    let height = currentYmax - currentYmin; 

    let newXmin = (length * .25) + currentXmin;
    let newXmax =  currentXmax - (length * .25);
    let newYmin = currentYmin + (height *.25);
    let newYmax = currentYmax - (height *.25);

    let basemap = document.getElementById('map-selector').value;
    let basemapURL = getBaseURL(basemap);

    let img = basemapURL + '/export?bbox=' + newXmin + '%2C' + newYmin + '%2C' + newXmax + '%2C' + newYmax + '&bboxSR=4326&layers=&layerDefs=&size=800%2C+400&imageSR=4326&format=png&transparent=false&dpi=&time=&layerTimeOptions=&dynamicLayers=&gdbVersion=&mapScale=&f=image';
    let map = document.getElementById('map');
    map.src = img;

    currentXmin = newXmin;
    currentXmax = newXmax;
    currentYmax = newYmax;
    currentYmin = newYmin; 
    
}

function zoomOut(){
    console.log('Zoom out brah');
}

function handleResponseData(response){
    currentResponse = JSON.parse(response);
    //Set description based on service metadata

    descriptionResponse = currentResponse.description
    description = document.getElementById('map-description');
    description.innerHTML = descriptionResponse;

    //Set initial extent of map based on service metadata.
    let initialExtent = currentResponse.fullExtent; 
    xmin = initialExtent.xmin;
    xmax = initialExtent.xmax;
    ymin = initialExtent.ymin;
    ymax = initialExtent.ymax; 


    currentXmin = xmin; 
    currentXmax - xmax;
    currentYmin = ymin;
    currentYmax = ymax; 

}


function zoomToFullExtent(){
    
    let basemap = document.getElementById('map-selector').value;
    let basemapURL = getBaseURL(basemap);

    let img = basemapURL + '/export?bbox=' + xmin + '%2C' + ymin + '%2C' + xmax + '%2C' + ymax + '&bboxSR=4326&layers=&layerDefs=&size=800%2C+400&imageSR=4326&format=png&transparent=false&dpi=&time=&layerTimeOptions=&dynamicLayers=&gdbVersion=&mapScale=&f=image';
    let map = document.getElementById('map');
    map.src = img;
    
}















init();

