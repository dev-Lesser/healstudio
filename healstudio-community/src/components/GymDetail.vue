<template>
<v-navigation-drawer v-if="selected" 
    class="sheet" 
    absolute 
    left 
    floating 
    hide-overlay 
    width="350px">
        <v-icon class="pl-3 mb-2" @click="$store.state.selected = !$store.state.selected">mdi-close</v-icon>
        <div class="box-title-wrap">
                <div class="box-title">
                    {{selectedData.name}}
                </div>
                <v-rating
                    v-model="rating"
                    background-color="white"
                    color="yellow accent-4"
                    dense
                    half-increments
                    size="18"
                    readonly
                    ></v-rating>
                    <div class="rate-content">
                        {{ rating }} 
                    </div>
                <div class="box-category">
                    <v-chip small>{{selectedData.category}}</v-chip>
                </div>
        </div>
            <v-divider />
            <v-img :src="selectedData.imageUrl" height="200"></v-img>
            <v-card-subtitle class="box-hashtag-title">
                    해시태그
                <div class="box-keywords">
                    
                    <v-chip outlined class="ma-2" small v-for="keyword, i in selectedData.keywords" :key="`keyword--${i}`">#{{keyword}}</v-chip>
                </div>
            </v-card-subtitle>
            <v-divider />
            <div class="box-address" to="">
                {{selectedData.roadAddress}}<br/>
                {{selectedData.fullAddress}}
            </div>
            
            <v-btn 
            :href="selectedData.bookingUrl" 
            outlined
            small
            color="green"
            > 
                예약 
            </v-btn> 
            <div class="box-phone">
                {{selectedData.phone}}<br/>
                {{selectedData.virtualPhone}}
            </div>
            <div class="box-businesshour" >
                <div class="box-businesshour-title">  영업 시간</div>
                <v-spacer/>
                <v-menu v-model="info" offset-x open-on-hover>
                    <template v-slot:activator="{ on, attrs }">
                    <v-btn v-bind="attrs" v-on="on" text icon>
                        <v-icon>mdi-information-outline</v-icon>
                    </v-btn>
                    </template>
                    <v-card width="300px" class="pa-3">
                    <div class="box-businesshour-sheet-title">영업 시간</div>
                    <div class="box-businesshour-content ma-1" v-for="data, ikey in selectedData.businessHours.split('|')" :key="ikey">{{data}}<v-divider /></div>
                    </v-card>
                </v-menu>
                
            </div>
            <!-- <p class="box-description" v-html="desc"></p> -->
            
            <div v-for="url, i in selectedData.urlList" :key="`url--${i}`"> 
                <div class="box-hompage">
                    <div  class="box-url-list" v-if="url.type == 'normal' | url.type =='modoo'">

                        <v-icon>mdi-home</v-icon>
                        <div class="box-url ml-3"><a :href="url.url">{{url.url}}</a></div>
                    </div>
                    <div class="box-url-list"  v-else-if="url.type == 'instagram' ">
                        <v-icon>mdi-instagram</v-icon>
                        <div class="box-url ml-3"><a :href="url.url">{{url.url}}</a></div>
                    </div>
                    <div class="box-url-list"  v-else-if="url.type == 'facebook' ">
                        <v-icon>mdi-facebook</v-icon>
                        <div class="box-url ml-3"><a :href="url.url">{{url.url}}</a></div>
                    </div>
                    <div class="box-url-list"  v-else-if="url.type == 'blog' ">
                        <v-icon> mdi-blogger</v-icon>
                        <div class="box-url ml-3"><a :href="url.url">{{url.url}}</a></div>
                    </div>
                    <div class="box-url-list"  v-else>
                        <v-icon>mdi-facebook</v-icon>
                        <div class="box-url ml-3"><a :href="url.url">{{url.url}}</a></div>
                    </div>
                    <!-- <v-chip v-if="url.type == 'blog'" label outlined>{{url.type}}</v-chip>
                    <v-chip v-else-if="url.type == 'instagram'" color='red'>{{url.type}}</v-chip>
                    <v-chip v-else-if="url.type == 'normal'" color='blue'>{{url.type}}</v-chip>
                    <v-chip v-else-if="url.type == 'modoo'" color='green'>{{url.type}}</v-chip>
                    <v-chip v-else-if="url.type == 'cafe'" color='purple'>{{url.type}}</v-chip>
                    <v-chip v-else-if="url.type == 'facebook'" dark>{{url.type}}</v-chip>
                    <v-chip v-else-if="url.type == 'storefarm'" dark>{{url.type}}</v-chip>
                    <v-chip v-else-if="url.type == 'reservation'" dark>{{url.type}}</v-chip> -->
                    
                    <!-- <v-chip v-else dark small>{{url.type}}</v-chip> -->
                </div>
            </div>
            <div v-for="url, i in selectedData.imgList" :key="`img--${i}`">
                <!-- {{url}}.jpg {{selectedData.imageUrl}} -->
                
            </div>
    </v-navigation-drawer>
</template>
<script>
    export default {
        data() {
            return {
                rating: 5,
                desc: null,
            }
        },
        computed: {
            selected() {
                return this.$store.state.selected;
            },
            selectedData() {
                return this.$store.state.selectedData;
            }
        },
        watch: {
            selectedData(data) {
                var desc = this.$store.state.selectedData.desc;
                this.desc = desc.replace(/\n/g, '<br/>');
                console.log(data, this.desc)
            }
        },
    }
</script>
<style scoped>
.sheet {
    padding: 20px;
    position: absolute;
    z-index: 1000;
    border-width: 1px;
    display: block;
    -ms-overflow-style: none; /* IE and Edge */
    -webkit-transition:width 2s, height 2s, background-color 2s, -webkit-transform 2s;
    transition: all ease 2s 0s;
}
.sheet::-webkit-scrollbar {
    display: none; /* Chrome, Safari, Opera*/
}
.box-hashtag-title{
     font-size: 15px;
    font-family:'Jeju Gothic', sans-serif;
}
.box-title-wrap {
    display: flex;
    justify-content: center;
    align-content: center;
}
.box-title {
   padding: 13px;
    font-size: 20px;
    font-family:'Jeju Gothic', sans-serif;
}
.box-category {
    font-family:'Jeju Gothic', sans-serif;
}
.box-address{
    padding: 20px;
    font-size: 13px;
    font-family:'Jeju Gothic', sans-serif;
}
.box-booking-url{
    font-size: 13px;
    font-family:'Jeju Gothic', sans-serif;
}
.box-phone {
    font-size: 13px;
    font-family:'Jeju Gothic', sans-serif;
}
.box-businesshour{
    display: flex;
    justify-content: left;
    align-items: center;
    padding: 10px;
    font-size: 13px;
    font-family:'Jeju Gothic', sans-serif;
}
.box-businesshour-sheet-title{
    font-size: 13px;
    font-family:'Jeju Gothic', sans-serif;
}
.box-businesshour-content{
    font-size: 13px;
    font-family:'Jeju Gothic', sans-serif;
}
.box-description{
    font-size: 13px;
    font-family:'Jeju Gothic', sans-serif;
    background-color: azure;
}
.box-keywords{
    width: 270px;
    height: 50px;
    overflow-x: scroll;
    overflow-y: hidden;
    white-space:nowrap;
    scrollbar-width: thin;
}
.box-keywords::-webkit-scrollbar {
    width: 4px;
    scrollbar-width: thin;
  }
.box-keywords::-webkit-scrollbar-thumb {
    background-color: #3A3B3D;
    border-radius: 15px;
    background-clip: padding-box;
    border: 2px solid transparent;
    scrollbar-width: thin;
  }
.box-keywords::-webkit-scrollbar-track {
    
    background-color: rgb(175, 174, 174);
    border-radius: 15px;
    box-shadow: inset 0px 0px 5px white;
    scrollbar-width: thin;
}
.box-hompage{
    display:flex;
}
.box-url-list{
    margin-top:5px;
    padding: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 5px;
    border: 1px dashed #bcbcbc;
}
.box-url {
    font-size: 13px;
    font-family:'Jeju Gothic', sans-serif;
    width: 245px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;  /* 말줄임 적용 */
}
</style>