<template>
    <v-layout wrap class="reply_page_layout" v-if="!!contents">
        <v-flex xs12 sm12 md12>
            <Meta :meta="meta"/>
        </v-flex>
        
        <v-flex xs12 sm8 md8 >
            <edit-board v-if="isEdit" :meta-contents="contents" />
            
            <v-card class="ma-3 pa-3" :min-height="400" v-else >
                <v-card-title class="reply_page_title">
                    * {{contents.title}}
                </v-card-title>
                <v-card-actions >
                    <v-spacer></v-spacer>
                    <div>작성자 : {{contents.user}}</div>
                </v-card-actions>
                <v-card-actions >
                    <v-spacer></v-spacer>
                    <div>작성일 : {{contents.created_at}}</div>
                </v-card-actions>
                <v-card-actions v-if="user_id==contents.user">
                    <v-spacer></v-spacer>
                    <v-btn @click="editPost">수정하기</v-btn>
                    <v-btn @click="deletePost" color="error">삭제하기</v-btn>
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
                    <v-text-field
                    v-model="replyContents"
                    :rules="ruleReply"
                    label="제목" outlined clearable dense></v-text-field>
                    <v-btn class="ma-3" dark @click="createReply"> 댓글작성 </v-btn>
                </div> 
                <v-progress-linear
                indeterminate
                color="black"
                class="mt-1"
                height="1"
                rounded
                v-if="loading"
                ></v-progress-linear>
                <v-progress-linear
                color="black"
                class="mt-1"
                height="1"
                rounded
                v-else
                ></v-progress-linear>
                <div v-if="replies.length>0">
                    <div v-for="reply, key in replies" :key="key">
                        <v-list-item  v-if="key%2" dense >
                            <div class="reply_contents">{{reply.contents}}</div>
                            <div class="reply_user">{{reply.user}}
                                <div v-if="reply.user == contents.user" class="same_user">{{sameUser}}</div>
                            </div>
                            <div class="reply_new" >{{isNew(reply.created_at)}}</div>
                            <div class="reply_new" v-if="user_id==reply.user">
                                <v-icon small
                                color="rgb(216, 116, 116)"
                                @click="openReplyDelete">
                                mdi-delete
                                </v-icon>
                            </div>
                        </v-list-item>
                        <v-list-item class="reply_block_line" v-else dense >
                            <div class="reply_contents">{{reply.contents}}</div>
                            <div class="reply_user">{{reply.user}}
                                <div v-if="reply.user == contents.user" class="same_user">{{sameUser}}</div>
                            </div>
                            <div class="reply_new" >{{isNew(reply.created_at)}}</div>
                            <div class="reply_new" v-if="user_id==reply.user">
                                <v-icon small
                                color="rgb(216, 116, 116)"
                                @click="openReplyDelete">
                                mdi-delete
                                </v-icon>
                            </div>
                        </v-list-item>
                        <v-divider/>
                    </div>
                </div>
                <div v-else>
                    😮‍💨 등록리뷰가 없습니다
                </div>
                <v-btn block dark @click="loadReply" v-if="!isEnd"> 댓글 더보기 </v-btn>
            </v-list>
            <v-overlay light v-if="isReplyDelete" >
                <v-card class="ma-3 pa-3" :width="500"
                light>
                <v-card-title>
                    정말로 삭제 하시겠습니까?
                </v-card-title>
                <v-divider />
            
                <v-card-actions>
                    <v-btn color="error" @click="deleteReply">삭제하기</v-btn>
                    <v-spacer />
                    <v-btn color="primary" @click="closeReply"> 취소 </v-btn>
                </v-card-actions>
                </v-card>
                
            </v-overlay>
            <delete-board v-if="boardDeleteOveray" :meta-contents="contents" />
            </v-card>
        </v-flex>
    </v-layout>
</template>
<script>
import {
    get_board,
    create_reply,
    delete_reply,
} from '@/assets/board'
import EditBoard from '@/components/board/EditBoard'
import DeleteBoard from '@/components/board/DeleteBoard'
import Contents from '@/components/board/Contents'
import Meta from '@/components/board/Meta'
export default {
    components:{
        Contents,
        EditBoard,
        DeleteBoard,
        Meta
    },
    data() {
        return {
            loading: false,
            sameUser: '<작성자>',
            skip:0,
            isEdit: false,
            isDelete: false,
            isReplyDelete:false,
            limit: 15,
            replies: null,
            contents: null,
            current: 1,
            isEnd: false,
            now: new Date(),
            limitLetters: [v => v.length <= 50 || '최대 50자'],
            ruleReply: [v => (v.length>=5 &&v.length <= 50) || '최소 5자 최대 50자'],
            replyContents: '',
            user_id: window.localStorage.getItem('user_id'),
            uuid: window.localStorage.getItem('token')
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
        async editPost(){
            this.isEdit = true
        },
        async deletePost(){
            this.$store.state.boardDeleteOveray = true
        },
        async createReply(){
            if (!this.user_id && !this.uuid){
                alert('로그인이 필요한 서비스입니다')
                this.$router.push('/login')
            }
            this.loading = true
            const success = await create_reply(this.user_id, this.uuid, this.$route.params.id, this.replyContents)
            if (success) this.$router.go()
        },
        async deleteReply(){
            this.loading = true
            const success = await delete_reply(this.user_id, this.uuid, this.$route.params.id)
            if (success) this.isReplyDelete=false; this.$router.go()
        },
        async openReplyDelete(){
            this.isReplyDelete = true;
        },
        async closeReply(){
            this.isReplyDelete = false;
        },
        async loadReply(){
            this.loading = true
            this.current = this.current +1
            this.skip = (this.current-1)*this.limit
            const [success, res] = await get_board(this.$route.params.id, this.$route.query.user, this.skip, this.limit);
            success;
            // this.contents = res.contents
            this.replies = this.replies.concat(res.replies)
            this.isEnd = res.isEnd
            this.loading = false
        },
    },
    computed:{
        meta() {
            return this.$store.state.meta;
        },
        boardDeleteOveray(){
            return this.$store.state.boardDeleteOveray;
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