<template>
    
    <v-menu v-model="info" offset-x open-on-hover>
        <template v-slot:activator="{ on, attrs }">
        <v-btn v-bind="attrs" v-on="on" text icon>
            
            <v-icon>mdi-information-outline</v-icon>
        </v-btn>
        </template>
        <v-card width="300px" class="pa-3">
        <div class="box-desc-title"> 한 마디 소개</div>
        <v-divider />
        <div class="box-desc-content" v-html=desc>

        </div>
        </v-card>
    </v-menu>
                
</template>
<script>
export default {
    props:{
        desc: String
    },
    data() {
        return {
            info: null,
        }
    },

}
</script>
<style scoped>
.box-desc-title{
    font-size: 15px;
    font-family:'Jeju Gothic', sans-serif;
}

.box-desc-content{
    font-size: 12px;
    font-family:'Jeju Gothic', sans-serif;
    padding: 10px;
}
</style>