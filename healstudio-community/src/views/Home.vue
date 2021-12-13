<template>
    <div>
        <l-map style="height: 100vh" :zoom="zoom" :center="center">
            <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
        </l-map>
        
        <gym-detail />
        
        
    </div>
</template>
<script>
import "leaflet/dist/leaflet.css"
import { LMap, LTileLayer } from "vue2-leaflet";
import GymDetail from "@/components/GymDetail"
export default {
    components: {
        LMap,
        LTileLayer,
        GymDetail
    },
    data(){
        return {
            drawer: true,
            sheet: false,
            url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            attribution: '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
            zoom: 12,
            center: [37.555, 127.019],
            markerLatLng: [51.504, -0.159]
        }
    },
    
    async beforeMount() {
    // HERE is where to load Leaflet components!
        // const { circleMarker } = await import("leaflet/dist/leaflet-src.esm");

        // And now the Leaflet circleMarker function can be used by the options:
        // this.geojsonOptions.pointToLayer = (feature, latLng) =>
        // circleMarker(latLng, { radius: 8 });
        // this.mapIsReady = true;
    },
}
    
</script>
<style scoped>

</style>