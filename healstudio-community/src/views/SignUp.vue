<template>
    <div class="login">
        <div class="login-card">
            <div id="menu_logo" style="cursor: default">
                <div id="menu_logo_letter">
                    HEALSTUDIO
                </div>
                <div id="menu_logo_circle" />
                
            </div>
            <v-divider />
            <div class="intro_box" >
                HEALSTUDIO 는 전국에 있는 헬스장과 관련하여 정보를 제공하고 사용자간의 대화를 통해 정보교환을 할 수 있는 커뮤니티 사이트 입니다.
            </div>
            <v-form class="signup-form">
                <v-text-field v-model="id" 
                :rules="[rules.required, rules.counterIdMin, rules.counterIdMax]"
                color="#52abc4" dense outlined label="아이디*" @keyup.enter="signUp" />
                <v-text-field v-model="pw" 
                :rules="[rules.required, rules.counterPwMin, rules.counterPwMax, rules.checkPw]"
                color="#52abc4" dense outlined label="비밀번호*" type="password" @keyup.enter="signUp" />
                <v-text-field v-model="pwCheck" 
                :rules="[rules.required, rules.same]"
                color="#52abc4" dense outlined label="비밀번호 확인*" type="password" @keyup.enter="signUp" />
                <v-btn class="login-btn-submit" color="#52abc4" dark @click="signUp">
                    회원가입
                </v-btn>
                
            </v-form>
        </div>
    </div>
</template>
<script>
import {signup} from '@/assets/auth'
export default {
    data() {
        return {
            id: null,
            pw: null,
            pwCheck: null,
            reg: /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,20}$/,
            rules: {
                required: value => !!value || '필수항목입니다.',
                counterIdMin: value => (!!value&&value.length >= 6 ) || '너무 짧습니다 (6자이상)',
                counterIdMax: value => (!!value&&value.length <= 20 ) || '너무 깁니다 (20자이하)',
                counterPwMin: value => (!!value&&value.length >= 8) || '너무 짧습니다 (8자이상)',
                counterPwMax: value => (!!value&& value.length <= 20) || '너무 깁니다 (20자이하)',
                same: () => this.pw==this.pwCheck || '비밀번호가 일치하지 않습니다',
                checkPw: ()=> (this.reg.test(this.pw) && this.pw.search(/\s/) == -1) || '숫자+영대소문자+특수문자 | 공백은 빼주세요'

            },
        }
    },
    mounted(){

    },
    methods:{
        async signUp(){
            if (this.id==null || this.pw == null || this.pwCheck == null){
                alert("입력란이 비었습니다")
                return
            }
            if (this.pw!==this.pwCheck){
                alert("비밀번호가 일치하지 않습니다")
                return
            }
            const [success, res] = await signup(this.id, this.pw);
            success;
            if (success) {
                window.localStorage.setItem('user_id', res.user_id)
                window.localStorage.setItem('token', res.token)
                this.$router.push('/')
            }
            else alert('아이디가 중복되었습니다.')

            
        }
    }
}
</script>
<style scoped>
.intro_box{
    font-family:'Jeju Gothic', sans-serif;
    color: rgb(184, 184, 184);
    padding: 50px;
}
</style>