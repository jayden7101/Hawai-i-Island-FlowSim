window.zoomToAnimationBounds = function(swLat, swLon, neLat, neLon, ventLat, ventLon) {
    const map = window.leafletMap || window.appMap;
    if (!map) {
        console.log("zoomToAnimationBounds: appMap missing");
        return;
    }

    const minLat = Math.min(swLat, neLat);
    const maxLat = Math.max(swLat, neLat);
    const minLon = Math.min(swLon, neLon);
    const maxLon = Math.max(swLon, neLon);

    const latPad = Math.max(Math.abs(ventLat - minLat), Math.abs(maxLat - ventLat));
    const lonPad = Math.max(Math.abs(ventLon - minLon), Math.abs(maxLon - ventLon));

    const centeredBounds = L.latLngBounds(
        [ventLat - latPad, ventLon - lonPad],
        [ventLat + latPad, ventLon + lonPad]
    );

    map.fitBounds(centeredBounds, {
        padding: [2, 2]
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