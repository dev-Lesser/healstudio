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
                <v-btn block color="primary">작성하기</v-btn>
            </v-card>
        </v-flex>
    </v-layout>
</template>
<script> 
// import { Editor, EditorContent, EditorMenuBar } from 'tiptap'
// import { Bold, Italic, Link, HardBreak, Heading } from 'tiptap-extensions'
// import StarterKit from '@tiptap/starter-kit'
export default { 
    components: { 
        // EditorContent, 
        // EditorMenuBar
    }, 
    data() {
        return { 
            editor: null, 
            contents: null,
            limitLetters: [v => v.length <= 200 || '최대 200자'],
            user: window.localStorage.getItem('user_id')
        } 
    },
    async mounted() {
        // this.editor = new Editor({
        // extensions: [
        //     new Bold(),
        //     new Italic(),
        //     new Link(),
        //     new HardBreak(),
        //     new Heading(),
            
        // ],
        // })
    // console.log(this.editor)
    // console.log(this.contents)
    },
    async updated(){
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