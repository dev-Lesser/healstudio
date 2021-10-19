<template>
    <v-layout wrap class="reply_page_layout">
        <v-flex xs12 sm8 md8>
            <v-card class="ma-3 pa-3" :min-height="400" color="grey lighten-4">
            <v-card-title class="reply_page_title">
                자유게시판
            </v-card-title>
            <v-card-actions>
                작성자 : {{contents.user}}
            </v-card-actions>
            <v-card-actions>
                작성일 : {{contents.created_at}}
            </v-card-actions>
            <v-divider />
                <Contents :data="contents" />
            </v-card>
            <v-card class="ma-3 pa-3">
                <v-card-actions>
                    댓글
                </v-card-actions>
            <v-divider />
            <v-list class="reply_list">  
                <div style="display:flex; justify-contents:center;">
                    <v-textarea
                    v-model="replyContents"
                    class="ma-3"
                    auto-grow
                    outlined
                    rows="1"
                    dense
                    color="#96AFDD"
                    :rules="limitLetters"
                    ></v-textarea>
                    <v-btn class="ma-3" dark @click="createReply"> 댓글작성 </v-btn>
                </div> 
                <v-progress-linear
                indeterminate
                color="black"
                class="mt-1"
                height="1"
                rounded
                ></v-progress-linear>
                <div v-if="replies.length>0">
                    <div v-for="reply, key in replies" :key="key">
                        <v-list-item  v-if="key%2" dense >
                            <div class="reply_contents">{{reply.contents}}</div>
                            <div class="reply_user">{{reply.user}}
                                <div v-if="reply.user == contents.user" class="same_user">{{sameUser}}</div>
                            </div>
                            <div class="reply_new" >{{isNew(reply.created_at)}}</div>
                        </v-list-item>
                        <v-list-item class="reply_block_line" v-else dense >
                            <div class="reply_contents">{{reply.contents}}</div>
                            <div class="reply_user">{{reply.user}}
                                <div v-if="reply.user == contents.user" class="same_user">{{sameUser}}</div>
                            </div>
                            <div class="reply_new" >{{isNew(reply.created_at)}}</div>
                        </v-list-item>
                        <v-divider/>
                    </div>
                </div>
                <div v-else>
                    😮‍💨 등록리뷰가 없습니다
                </div>
            </v-list>
            </v-card>
        </v-flex>
    </v-layout>
</template>
<script>
import {
    get_board
} from '@/assets/board'
import Contents from '@/components/board/Contents'
export default {
    components:{
        Contents
    },
    data() {
        return {
            sameUser: '<작성자>',
            skip:0,
            limit: 15,
            replies: null,
            contents: null,
            now: new Date(),
            limitLetters: [v => v.length <= 50 || '최대 50자'],
            replyContents: null
        }
    },
    async mounted(){
        await this.getBoard(this.$route.params.id, this.$route.query.user, this.skip, this.limit)
    },
    methods:{
        async getBoard(id, user, skip, limit){
            const [success, res] = await get_board(id, user, skip, limit);
            success;
            this.contents = res.contents
            this.replies = res.replies
        },
        isNew(date){
            const dateDiff =  this.now.getTime() - new Date(date).getTime()
            const diff = dateDiff/(1000*60)
            if (parseInt(diff)==0) return '방금✨'
            if (0< diff < 60) return parseInt(diff) + '분전✨'
            else return date.split()[0]
        },
        async createReply(){
            console.log(this.replyContents)
        }
    }
}
</script>
<style scoped>
.reply_page_layout{
    display: flex;
    justify-content: center;
    font-family:'Jeju Gothic', sans-serif;
}
.reply_page_title{
    font-size: 24px;
    font-family:'Jeju Gothic', sans-serif;
}
.reply_block_line{
    background-color: #FAFAFA;
}
.reply_id_header{
    width: 5%;
}
.reply_id{
    width: 5%;
    font-size: 10px;
}
.reply_contents_header{
    width: 70%;
}
.reply_contents{
    width: 70%;
    font-size: 14px;
}
.reply_user_header{
    width: 15%;
}
.reply_user{
    width: 15%;
    font-size: 12px;
}
.reply_new_header{
    width: 10%;
}
.reply_new{
    width: 10%;
    font-size: 12px;
}
.same_user {
    font-size: 10px;
    color: rgb(235, 151, 151)
}
</style>