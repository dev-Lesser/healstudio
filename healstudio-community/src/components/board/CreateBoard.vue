<template>
    <v-layout wrap class="board_page_layout">
        <v-flex xs12 sm8 md8>
            <v-card class="ma-3 pa-3" height=800>
            <v-card-title class="board_page_title">
                글작성
            </v-card-title>
            <v-divider />
                <editor-menu-bar :editor="editor" v-slot="{ commands, isActive }">
                    <v-btn :class="{ 'is-active': isActive.bold() }" @click="commands.bold">
                        Bold
                    </v-btn>
                </editor-menu-bar>
                <editor-content class="editor__content" :editor="editor" />
                <v-btn>작성하기</v-btn>
            </v-card>
        </v-flex>
    </v-layout>
</template>
<script> 
import { Editor, EditorContent, EditorMenuBar } from 'tiptap'
import { Bold, Italic, Link, HardBreak, Heading } from 'tiptap-extensions'
export default { 
    components: { 
        EditorContent, 
        EditorMenuBar
    }, 
    data() {
        return { 
            editor: null, 
        } 
    },
    async mounted() {
        this.editor = await new Editor({
        extensions: [
            new Bold(),
            new Italic(),
            new Link(),
            new HardBreak(),
            new Heading(),
        ],
        })
    console.log(this.editor)
    },
    async updated(){
        console.log(this.editor)
    },

    async beforeDestroy() {
        await this.editor.destroy()
    },
}
</script>

<style scoped>
.board_page_layout{
    display: flex;
    justify-content: center;
}
.board_page_title{
    font-size: 24px;
    font-family:'Jeju Gothic', sans-serif;
}   
</style>