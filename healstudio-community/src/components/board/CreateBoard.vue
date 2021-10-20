<template>
    <v-layout wrap class="board_page_layout">
        <v-flex xs12 sm8 md8>
            <v-card class="ma-3 pa-3" height=800>
            <v-card-title class="board_page_title">
                글 작성
            </v-card-title>
            <v-card-actions>
                작성자 : {{user}}
            </v-card-actions>
            <v-divider />
                <!-- <editor-menu-bar :editor="editor" v-slot="{ commands, isActive }">
                    <v-btn :class="{ 'is-active': isActive.bold() }" @click="commands.bold">
                        Bold
                    </v-btn>
                </editor-menu-bar>
                <editor-content v-model="contents" class="editor__content" :editor="editor" /> -->
                <v-textarea
                    v-model="contents"
                    class="mt-5"
                    height="500"
                    outlined
                    color="#96AFDD"
                    :rules="limitLetters"
                    ></v-textarea>
                <v-btn block color="primary" @click="createBoard">작성하기</v-btn>
            </v-card>
        </v-flex>
    </v-layout>
</template>
<script> 
// import { Editor, EditorContent, EditorMenuBar } from 'tiptap'
// import { Bold, Italic, Link, HardBreak, Heading } from 'tiptap-extensions'
// import StarterKit from '@tiptap/starter-kit'
import {
    create_board
} from '@/assets/board'
export default { 
    components: { 
        // EditorContent, 
        // EditorMenuBar
    }, 
    data() {
        return { 
            editor: null, 
            contents: null,
            limitLetters: [v => v.length <= 500 || '최대 500자'],
            user: window.localStorage.getItem('user_id'),
            uuid: window.localStorage.getItem('token')
        } 
    },
    async mounted() {

    },
    async updated(){
    },
    methods:{
        async createBoard(){
            if (this.contents.length >500) return
            console.log(this.user, this.uuid, this.contents)
            const [success,res] = await create_board(this.user, this.uuid, this.contents);
            console.log(success, res)
            if(!success) return
            else{
                this.$router.push('/boards')
            }
        }
    },
    beforeDestroy() {
        this.editor.destroy()
    },
    watch:{
        contents(){
            
        }
    }
}
</script>

<style scoped>
.board_page_layout{
    display: flex;
    justify-content: center;
    font-family:'Jeju Gothic', sans-serif;
}
.board_page_title{
    font-size: 24px;
    font-family:'Jeju Gothic', sans-serif;
}   
</style>