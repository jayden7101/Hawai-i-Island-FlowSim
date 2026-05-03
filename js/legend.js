
// this is the legend for the lava hazard zone numbers values
// it will only show when the lava hazard zone overlay is visible.
window.showLavaLegend = function() {
    try {
        var existing = document.getElementById('lava-zone-legend');
        if (existing) existing.remove();

        var mapContainer;
        if(window.appMap) {
            mapContainer = window.appMap.getContainer();
        }
        else {
            mapContainer = document.body;
        }
        mapContainer.style.position = 'relative';
        
        var legend = document.createElement('div');
        legend.id = 'lava-zone-legend';
        legend.style.cssText = `
            position: absolute;
            bottom: 30px;
            right: 10px;
            z-index: 9999;
            background: rgba(255,255,255,0.92);
            border: 1px solid #999;
            border-radius: 7px;
            padding: 10px 14px;
            font-family: Verdana,serif;
            font-size: 12px;
            color: #333;
            min-width: 180px;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.3);`;

        var zones = [
            ['#C461C4', 'Zone 1 - Highest Risk'],
            ['#FF9393', 'Zone 2'],
            ['#FFC4C4', 'Zone 3'],
            ['#FFB061', 'Zone 4'],
            ['#FFE9A6', 'Zone 5'],
            ['#FFFFCE', 'Zone 6'],
            ['#BAFFBA', 'Zone 7'],
            ['#E0FFB0', 'Zone 8'],
            ['#FFFFE2', 'Zone 9 - Lowest Risk']
        ];

        var title = document.createElement('div');
        title.style.cssText = 'font-weight:bold;margin-bottom:6px;font-size:13px;';
        title.textContent = 'Lava Hazard Zones';
        legend.appendChild(title);

        zones.forEach(function(zone) {
            var row = document.createElement('div');
            row.style.marginBottom = '3px';

            var swatch = document.createElement('span');
            swatch.style.cssText = `
                display: inline-block;
                width: 14px;
                height: 14px;
                border: 1px solid #000;
                margin-right: 6px;
                vertical-align: middle;
                background: ${zone[0]};`;

            var label = document.createTextNode(zone[1]);

            row.appendChild(swatch);
            row.appendChild(label);
            legend.appendChild(row);
        });

        mapContainer.appendChild(legend);

    } catch(error) {
        console.error("Legend inject error (JS Side):", error);
    }
};

// this function is to hide the lava zone hazard when the overlay is not
// current visible
window.hideLavaLegend = function() {
    try {
        var el = document.getElementById('lava-zone-legend');
        if (el) el.remove();
    }
    catch (error) {
        console.error("Legend remove error (JS Side): , error");
    }
};

window.showLavaDepthLegend = function(){};