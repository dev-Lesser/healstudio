<template>
    <v-layout wrap class="reply_page_layout" v-if="!!contents">
        <v-flex xs12 sm12 md12>
            <Meta :meta="meta"/>
        </v-flex>
        
        <v-flex xs12 sm8 md8 >
            <edit-board v-if="isEdit" @isEdit="handleEdit" @changeTitle="changeTitle" @changeContents="changeContents" :meta-contents="contents" />
            
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
                <v-card-actions v-if="user_id==contents.user && !contents.isDeleted">
                    <v-spacer></v-spacer>
                    <v-btn @click="editPost">수정하기</v-btn>
                    <v-btn @click="deletePost" color="error">삭제하기</v-btn>
                </v-card-actions>
            <v-divider />
                <Contents :data="contents" :isFavorite="isFavorite"/>
            </v-card>
            <v-card class="ma-3 pa-3">
                <v-card-actions>
                    댓글
                </v-card-actions>
            <v-divider />
            <v-list class="reply_list" two-line>  
                <v-system-bar
                    color="primary"
                    v-if="replyCreated"
                    dark
                    class="mb-5"
                    >
                    댓글을 등록하였습니다.
                    </v-system-bar>
                <div style="display:flex; justify-contents:center;">
                    <v-text-field
                    v-model="replyContents"
                    :rules="ruleReply"
                    label="내용" outlined clearable dense
                    hide-details style="display:flex;align-items:center;"> </v-text-field>
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
                <v-btn block @click="loadReply" v-if="!isEnd&&replies.length==15" height="65" outlined> 이전 댓글 더보기 </v-btn>
                <div v-if="replies.length>0" >
                    <div v-for="reply, key in replies" :key="key">
                        <v-list-item  v-if="key%2" dense >
                            <div class="reply_new" >{{isNew(reply.created_at)}}</div>
                            <div class="reply_user">{{reply.user}}
                                <div v-if="reply.user == contents.user" class="same_user">{{sameUser}}</div>
                            </div>
                            <div class="reply_contents">{{reply.contents}}</div>
                            
                            
                            <div class="reply_new" v-if="user_id==reply.user">
                                <v-icon small
                                color="rgb(216, 116, 116)"
                                @click="openReplyDelete(reply.id)">
                                mdi-delete
                                </v-icon>
                            </div>
                        </v-list-item>
                        <v-list-item class="reply_block_line" v-else dense >
                            <div class="reply_new" >{{isNew(reply.created_at)}}</div>
                            <div class="reply_user">{{reply.user}}
                                <div v-if="reply.user == contents.user" class="same_user">{{sameUser}}</div>
                            </div>
                            <div class="reply_contents">{{reply.contents}}</div>
                            
                            
                            <div class="reply_new" v-if="user_id==reply.user">
                                <v-icon small
                                color="rgb(216, 116, 116)"
                                @click="openReplyDelete(reply.id)">
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
            isFavorite: false,
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
            replyCreated: false,
            replyContents: '',
            user_id: window.localStorage.getItem('user_id'),
            uuid: window.localStorage.getItem('token'),
            deleteItemId : null,
        }
    },
    async mounted(){
        await this.getBoard(this.$route.params.id, this.$route.query.user, this.user_id, this.skip, this.limit)
    },
    methods:{
        async getBoard(id, user, login_user, skip, limit){
            const [success, res] = await get_board(id, user, login_user, skip, limit);
            success;
            this.contents = res.contents
            this.replies = res.replies
            this.isFavorite = res.isFavorite
        },
        isNew(date){
            const dateDiff =  this.now.getTime() - new Date(date).getTime()
            const diff = dateDiff/(1000*60)
            if (parseInt(diff)==0) return '방금✨'
            if (0<= diff&& diff< 60) return parseInt(diff) + '분전✨'
            if(60<= diff&& diff< 60*24) {
                return date.split(' ')[1].split(':').slice(0,2).join(':')
            }
            else return date.split(' ')[0]
        },
        async editPost(){
            this.isEdit = true
        },
        async handleEdit(isEdit){
            this.isEdit = isEdit
        },
        async changeTitle(title){
            this.contents.title = title
        },
        async changeContents(contents){
            this.contents.contents = contents
        },
        async deletePost(){
            this.$store.state.boardDeleteOveray = true
        },
        async createReply(){
            if (!this.user_id && !this.uuid){
                alert('로그인이 필요한 서비스입니다')
                this.$router.push('/login')
            }
            if (this.replyContents.length<5){
                alert('5자 이상 적어주세요')
                return;
            }
            if (this.replyContents.length>50){
                alert('50자 이하로 적어주세요')
                return;
            }
            this.loading = true
            const [success, id] = await create_reply(this.user_id, this.uuid, this.$route.params.id, this.replyContents)
            if (success) {
                this.loading=false
                const date = new Date()
                const now = date.getFullYear() + "-" + ("0" + (date.getMonth() + 1)).slice(-2) 
                        + "-" + ("0" + date.getDate()).slice(-2) + " " + ("0" + date.getHours() ).slice(-2) + ":" + ("0" + date.getMinutes()).slice(-2) + ":" +("0" + date.getSeconds()).slice(-2)
                this.replyCreated = true
                this.replies.push({id: id,created_at: now, user: this.user_id, contents: this.replyContents})
                this.replyContents = '내용을 입력하세요'
                setTimeout(()=>{this.replyCreated= false}, 3000);

            }
        },
        async deleteReply(){
            this.loading = true
            const success = await delete_reply(this.user_id, this.uuid, this.deleteItemId)
            if (success) {
                this.loading = false
                this.isReplyDelete=false; 
                this.replies = this.replies.filter(item => item.id!=this.deleteItemId)
            }
        },
        async openReplyDelete(reply_id){
            this.deleteItemId = reply_id
            console.log(reply_id)
            this.isReplyDelete = true;
        },
        async closeReply(){
            this.isReplyDelete = false;
        },
        async loadReply(){
            this.loading = true
            this.current = this.current +1
            this.skip = (this.current-1)*this.limit
            const [success, res] = await get_board(this.$route.params.id, this.$route.query.user, this.user_id, this.skip, this.limit);
            success;
            // this.contents = res.contents
            this.replies = res.replies.concat(this.replies)
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