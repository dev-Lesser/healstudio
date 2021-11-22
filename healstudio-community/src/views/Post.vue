<template>
    <v-layout wrap class="board_page_layout">
        <v-flex xs12 sm12 md12>
            <Meta :meta="meta" />
        </v-flex>
        <v-flex xs12 sm8 md8>
            <v-card class="ma-3 pa-3">
                <v-card-title class="board_page_title">
                    글 작성
                </v-card-title>
                <v-card-actions>
                    작성자 : {{user}}
                </v-card-actions>
                <v-divider />
                <v-text-field v-model="title" 
                :rules="rules"
                label="제목" 
                outlined 
                clearable 
                dense></v-text-field>
                <tiptap-vuetify v-model="contents" :extensions="extensions" />
                <v-btn block class="mt-3" color="primary" @click="createBoard">작성하기</v-btn>
            </v-card>
        </v-flex>
    </v-layout>
</template>
<script>
    import {
        create_board
    } from '@/assets/board'
    import Meta from '@/components/board/Meta'
    import {
        TiptapVuetify,
        Heading,
        Bold,
        Italic,
        Strike,
        Underline,
        BulletList,
        OrderedList,
        ListItem,
        Link,
        History,
        Image
    } from 'tiptap-vuetify'
    export default {
        components: {
            Meta,
            TiptapVuetify,
        },
        data() {
            return {
                title: null,
                contents: null,
                limitLetters: [v => v.length <= 500 || '최대 500자'],
                user: window.localStorage.getItem('user_id'),
                uuid: window.localStorage.getItem('token'),
                rules: [value=> (!!value&& value.length <= 30) || '최대 30자'],
                extensions: [
                    History,
                    Link,
                    Underline,
                    Strike,
                    Italic,
                    ListItem,
                    BulletList,
                    OrderedList,
                    [Heading, {
                        options: {
                        levels: [1, 2, 3]
                        }
                    }],
                    Bold,
                    Image
                    ],
            }
        },
        async mounted() {
            if (!this.user) {
                alert('로그인이 필요한 기능입니다.')
                this.$router.push('/login')
            }
        },
        methods: {
            async createBoard() {
                if (this.title.length > 30 || this.title.length < 3) return
                const success = await create_board(this.user, this.uuid, this.title, this.contents);
                if (!success) return
                else {
                    this.$store.state.current = 1
                    this.$router.push('/boards?page=1')
                }
            }
        },
        computed: {
            meta() {
                return this.$store.state.meta;
            }
        },
        watch: {
            contents() {
                console.log(this.contents)
            },
        }
    }
</script>

<style scoped>
.board_page_layout {
    display: flex;
    justify-content: center;
    font-family: 'Jeju Gothic', sans-serif;
}
.board_page_title {
    font-size: 24px;
    font-family: 'Jeju Gothic', sans-serif;
}
.v-btn__content{
    display: none;
}
.tiptap-vuetify-editor__content div  p  img {
    width: 100%;
}
.tiptap-vuetify-editor,
.tiptap-vuetify-editor__content {
    min-height: 500px;
}
</style>