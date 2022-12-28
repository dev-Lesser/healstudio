<template>
<v-flex xs12 sm12 md12 >

    <v-card  class="ma-3 pa-3" height="600">
        <v-card-title>
            {{metaData.name}}
            
        </v-card-title>
        <v-chip outlined class="box-hashtag-content ma-2" small v-for="keyword, i in metaData.keywords" :key="`keyword--${i}`">#{{keyword}}</v-chip>
        <v-list
            two-line
            class="review_list"
            v-if="data.length>0"
        >
        <div class="trainer-header">
            <v-list-item>
                <div class="trainer-user">
                    선생님
                </div>
                <div class="trainer-rating">
                    별점
                </div>
                <div class="trainer-content">
                    키워드
                </div>
                
            </v-list-item>
        </div>
        <div v-for="trainer, i in data" :key="i">
            <v-divider />
            <v-list-item :key="trainer.id" class="review_list_item">
        
                <div class="trainer-user">
                    <v-avatar class="mr-3" color="indigo" size="36">
                        <v-icon dark>
                            mdi-account-circle
                        </v-icon>
                    </v-avatar>
                    
                    <div>
                    {{trainer.name}}
                    </div>
                </div>
                <div class="trainer-rating">
                <v-rating
                    v-model="trainer.point"
                    background-color="white"
                    color="yellow accent-4"
                    dense
                    half-increments
                    size="18"
                    readonly
                    ></v-rating>
                </div>
                <div v-for="keyword, ikey in trainer.keywords" :key="`keyword--`+ikey">
                    <v-chip outlined small class="trainer-keywords ma-2">
                        #{{keyword}}
                    </v-chip>
                </div>
                
                
            </v-list-item>

        </div>
        </v-list>
        <v-list
            two-line
            
            class="review_list"
            v-else
        >
        <no-data />
        </v-list>
    </v-card>
</v-flex>
</template>
<script>
import NoData from '@/components/NoData'

export default {
    components: {
        NoData
    },
    props:{
        metaData: Object,
        data: Array,
    },
    data(){
        return {
            listWidth: window.innerWidth - 602,
            listHeight: Math.round((window.innerHeight - 483) / 100) * 100,
        }
    },
    mounted(){
        console.log(this.$route.name)
    }
}
</script>
<style scoped>
.review_list_item{
    font-size: 13px;
}
.trainer-header{
    font-size: 15px;
}
.trainer-user {
    display: flex;
    justify-content: left;
    align-items: center;
    width: 15%;
}
.trainer-rating {
    width: 15%;
    text-align: center;
}
.review_list_item{
    font-size: 13px;
}
.review-header{
    font-size: 15px;
}
.review-user {
    display: flex;
    justify-content: left;
    align-items: center;
    width: 10%;
}
.review-rating {
    width: 130px;
    text-align: center;
}
.review-content {
    width: 45%;
}
.review-created{
    width: 15%;
}
.review-updated{
    width: 15%;
}

</style>