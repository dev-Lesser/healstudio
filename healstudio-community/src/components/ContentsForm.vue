<template>
    <v-overlay :value="overlay" light  >
        <v-card class="ma-3 pa-3" :width="500"
        :height="400" light>
            <v-card-title>
                리뷰
                <v-card-actions>
                    <div><v-chip outlined>{{metaData.name}}</v-chip></div>
                </v-card-actions>
            </v-card-title>
            <v-divider />
                
                <v-card-actions>
                    <div>
                        평점 : 
                    </div>
                    <v-rating
                        v-model="point"
                        :value="contents"
                        background-color="grey"
                        hover
                        length="5"
                        color="yellow accent-4"
                        dense
                        half-increments
                        size="25"
                        
                        ></v-rating> 
                    <v-spacer />
                    <div>{{point}} 점</div>
                </v-card-actions>
                
            
            
            
            <v-divider class="mt-6" />
            <v-textarea
            v-model="contents"
            clearable	
            outlined
            dense
            class="ma-1 pa-2"
            label="한줄평 50자"
            height=100
            color="grey"
            rounded
            :rules="limitLetters"
            ></v-textarea>
            <v-card-actions>
                <v-btn v-if="!isUpdateClick" @click="createReview">작성하기</v-btn>
                <v-btn v-else @click="editReview">수정하기</v-btn>
                
                
                <v-spacer/>
                <v-btn @click="closeReview">취소</v-btn>
            </v-card-actions>
        </v-card>
    </v-overlay>
</template>
<script>
import {
    create_review, 
    update_review,
} from '@/assets/api'

export default {
    props: {
        overlay: Boolean,
        metaData: Object,
        point: Number,
        contents: String,
        isUpdateClick: Boolean,
        updateId: Number,

    },
    data(){
        return {
            limitLetters: [v => v.length <= 50 || '최대 50자'],
            current_user: window.localStorage.getItem('user_id')
        }
    },
    methods:{
        async init(){
            this.$store.state.overlay = false
            // this.point = 5
            // this.isUpdateClick = false
        },
        async closeReview(){
            await this.init();
        },
        async createReview(){
            if (this.contents.length > 50){
                alert("리뷰 길이가 50을 넘었습니다.")
                return
            }
            const [success, res] = await create_review(
                this.$route.params.id,
                this.current_user,
                this.contents,
                this.point
                );
                if (!success) {
                    this.status = -1;
                    alert(res)
                }
                else {
                    await this.init();
                    this.$router.go()
                }
                this.loading = false;
        },
        async editReview(){
            console.log(this.contents, this.point, this.updateId)
            const [success, res] = await update_review(
                this.updateId,
                this.$route.params.id,
                this.current_user,
                this.contents,
                this.point
                );
                console.log(success, res)
                if (!success) {
                    this.status = -1;
                    alert(res)
                }
                else {
                    await this.init();
                    this.$router.go();
                }
                
                this.loading = false;
        },
    },
    
}
</script>