
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

var currentCRS;

var description; 



// FUNCTIONS ----------------------------------------------------------------------------------------------------------------------------------------

function init(){

    updateTitle(basemaps.esriWorldStreetmap.id);
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

    if (basemap === "esri-world-streetmap"){
        title.innerHTML = 'ESRI World Street Map (2D)';
        return
    }
    else if (basemap === "us-topo-maps"){
        title.innerHTML = 'USA Topo Maps';
        return
    }
    else if (basemap === "us-pop-change"){
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
    //bring in local xmin
    let length = currentXmax - currentXmin; 
    let height = currentYmax - currentYmin; 

    let newXmin = (length * .25) + currentXmin;
    let newXmax =  currentXmax - (length * .25);
    let newYmin = currentYmin + (height *.25);
    let newYmax = currentYmax - (height *.25);

    let basemap = document.getElementById('map-selector').value;
    let basemapURL = getBaseURL(basemap);

    let img = basemapURL + '/export?bbox=' + newXmin + '%2C' + newYmin + '%2C' + newXmax + '%2C' + newYmax + '&bboxSR=' +  + currentCRS + '&layers=&layerDefs=&size=800%2C+400&imageSR=' + currentCRS + '&format=png&transparent=false&dpi=&time=&layerTimeOptions=&dynamicLayers=&gdbVersion=&mapScale=&f=image';
    let map = document.getElementById('map');
    map.src = img;

    currentXmin = newXmin;
    currentXmax = newXmax;
    currentYmax = newYmax;
    currentYmin = newYmin; 
    
}

function zoomOut(){

    let length = currentXmax - currentXmin; 
    let height = currentYmax - currentYmin; 
    
    let basemap = document.getElementById('map-selector').value;
    let basemapURL = getBaseURL(basemap);

    let newXmin =  currentXmin - (length * .5);
    let newXmax =  currentXmax + (length * .5);
    let newYmin = currentYmin - (height *.5);
    let newYmax = currentYmax + (height *.5);

    let img = basemapURL + '/export?bbox=' + newXmin + '%2C' + newYmin + '%2C' + newXmax + '%2C' + newYmax + '&bboxSR='  + currentCRS + '&layers=&layerDefs=&size=800%2C+400&imageSR='  + currentCRS + '&format=png&transparent=false&dpi=&time=&layerTimeOptions=&dynamicLayers=&gdbVersion=&mapScale=&f=image';
    let map = document.getElementById('map');
    map.src = img;

    currentXmin = newXmin;
    currentXmax = newXmax;
    currentYmax = newYmax;
    currentYmin = newYmin; 

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

    currentCRS = currentResponse.spatialReference.latestWkid;

    currentXmin = xmin; 
    currentXmax = xmax;
    currentYmin = ymin;
    currentYmax = ymax; 

    // let basemap = document.getElementById('map-selector').value;
    // let basemapURL = getBaseURL(basemap);

    // let img = basemapURL + '/export?bbox=' + currentXmin + '%2C' + currentYmin + '%2C' + currentXmax + '%2C' + currentYmax + '&bboxSR=4326&layers=&layerDefs=&size=800%2C+400&imageSR=4326&format=png&transparent=false&dpi=&time=&layerTimeOptions=&dynamicLayers=&gdbVersion=&mapScale=&f=image';
    // let map = document.getElementById('map');
    // map.src = img;
    // console.log(img)

}


function zoomToFullExtent(){
    
    let basemap = document.getElementById('map-selector').value;
    let basemapURL = getBaseURL(basemap);

    let img = basemapURL + '/export?bbox=' + xmin + '%2C' + ymin + '%2C' + xmax + '%2C' + ymax + '&bboxSR=' + currentCRS + '&layers=&layerDefs=&size=800%2C+400&imageSR=' + currentCRS + '&format=png&transparent=false&dpi=&time=&layerTimeOptions=&dynamicLayers=&gdbVersion=&mapScale=&f=image';
    let map = document.getElementById('map');
    map.src = img;
    
}


function mapChange(){
    
    let basemap = document.getElementById('map-selector').value;
    updateTitle(basemap);
    let basemapURL = getBaseURL(basemap);
    let basemapMetadataURL = encodeURI(basemapURL + "?f=pjson"); 
    let map = document.getElementById('map');
    map.src = "";
    sendHttpRequest(basemapMetadataURL);  
    setTimeout(function(){
        zoomToFullExtent();
     }, 1000);
}












init();

