document.addEventListener("DOMContentLoaded", function () {
    if (typeof QWebChannel === "undefined") { 
        console.error("QWebChannel is not loaded. (JS Side)"); // Adding (JS Side) to all errors in this file for easier debugging since its a pain
        return;
    }

    new QWebChannel(qt.webChannelTransport, function (channel) {
        window.bridge = channel.objects.bridge;
        findAndHookMap();
    });
});

function findAndHookMap() {
    // Search window for Leaflet map instance
    var mapInstance=null;
    
    for (var key in window) {
        if (window[key] instanceof L.Map) {
            mapInstance = window[key];
            break;
        }
    }

    if (!mapInstance) return;

    window.leafletMap = mapInstance;

    mapInstance.on('click', function (e ) {
        if (window.bridge){ 
            window.bridge.sendCoordinates(e.latlng.lat, e.latlng.lng);
        }
    });
}

// State traccker
window.currentVideoElement =null;
// added swlat/lon, nelat/lon
window.playVideoOverlay = function(swLat, swLon, neLat, neLon ,videoUrl) {
    // Play/resume vid function
    try {
        if (!window.leafletMap) return;

        // Resume (paused and exiting)
        if (window.currentVideoElement && window.currentVideoElement.paused) {
            window.currentVideoElement.play();
            return;
        }

        // Fresh clean state if video new
        if (window.currentVideoLayer){
            window.leafletMap.removeLayer(window.currentVideoLayer);
            window.currentVideoElement = null;
        }
	// changed to swlatlon, nelatlon to account for boundary boxes
        var bounds = [
            [swLat, swLon], 
            [neLat, neLon]
        ];

        window.currentVideoLayer = L.videoOverlay(
            videoUrl,
            bounds,
            { autoplay: true, loop: true, opacity: 0.8, interactive: false }
        ).addTo(window.leafletMap);
        
        // Get elemnt (for control)
        setTimeout(function() {
            var videoTags = document.getElementsByTagName('video');
            if (videoTags.length > 0) {
                window.currentVideoElement =videoTags[videoTags.length - 1];
            }
        }, 100);

    } catch (error) {
        console.error("Video Error (JS Side):", error);
    }
};

window.pauseVideoOverlay = function() {
    // Pause the video
    try {
        if (window.currentVideoElement) {
            window.currentVideoElement.pause();
        } else {
            var videoTags=document.getElementsByTagName('video');
            if (videoTags.length>0) {
                videoTags[videoTags.length - 1].pause();
            }
        }
    } catch (error) {
        console.error("Pause Error (JS Side):", error);
    }
};

window.removeVideoOverlay = function() {
    // Remove video layer
    try{
        if (window.currentVideoLayer && window.leafletMap) {
            console.log("Removing video overlay. (JS Side)");
            window.leafletMap.removeLayer(window.currentVideoLayer);
        }
        window.currentVideoLayer = null;
        window.currentVideoElement = null;
        
    } catch(error){
        console.error("Remove Error (JS Side):", error);
    }
};