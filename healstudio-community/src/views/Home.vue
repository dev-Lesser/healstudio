<template>
    <v-layout wrap>
        <side-nav-bar />
        <gym-detail :data="gyms"/>
        <l-map id="map" :zoom="zoom" :center="center">
            <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
        </l-map>
        
    </v-layout>
</template>
<script>
import "leaflet/dist/leaflet.css"
import { LMap, LTileLayer } from "vue2-leaflet";
import GymDetail from "@/components/GymDetail"
import SideNavBar from '@/components/SideNavBar'

export default {
    components: {
        LMap,
        LTileLayer,
        GymDetail,
        SideNavBar
        
    },
    data(){
        return {
            drawer: true,
            sheet: false,
            url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            attribution: '',
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
    async mounted(){
    },
    computed: {
        gyms(){
            return this.$store.state.selectedData
        }
    },
    watch:{
        gyms(){
            // console.log(this.$store.state.gyms)
        }
    }
}
    
</script>
<style scoped>
#map{
    height: calc(100vh - 64px);
    width: calc(100vw - 360px);
}
</style>