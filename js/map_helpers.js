window.zoomToAnimationBounds = function(swLat, swLon, neLat, neLon) {
    const map = window.appMap;
    if (!map) {
        console.log("zoomToAnimationBounds: appMap missing");
        return;
    }

    const animBounds = L.latLngBounds(
        [swLat, swLon],
        [neLat, neLon]
    );

    map.fitBounds(animBounds, {
        padding: [20, 20]
    });
};

window.resetToIslandBounds = function(swLat, swLon, neLat, neLon) {
    const map = window.appMap;
    if (!map) {
        console.log("resetToIslandBounds: appMap missing");
        return;
    }

    const islandBounds = L.latLngBounds(
        [swLat, swLon],
        [neLat, neLon]
    );

    map.fitBounds(islandBounds, {
        padding: [10, 10]
    });
};