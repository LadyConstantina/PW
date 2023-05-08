<template>
    <div class="container">
      <div id="game" class="flex_center flex_column">
        <div v-if="user_not_logged">
            <User @user="captureUserData"/>
        </div>
        <div v-else-if="quiz_begin">
            <Question @status_quiz="captureQuizStatus"/>
        </div>
        <div v-else>
            <Quiz :user="user" @quiz_start="captureQuizData"/>
        </div>
      </div>
    </div>
</template>

<script>
import Question from './include/Question.vue'
import Quiz from './include/Quiz.vue'
import User from './include/CreateUser.vue'


export default{
  name:'Main',
  emits:['user','status_quiz','quiz_start'],
  components:{
    Question, Quiz, User
  },
  data(){
    return{
        user_not_logged: true,
        quiz_begin: false,
        user: null,
        quiz_data: null
    }
  },
  methods:{
    captureUserData(data){
        this.user = data;
        this.user_not_logged=false;
    },
    captureQuizData(data){
        this.quiz_data=data;
        this.quiz_begin = true;
    },
    captureQuizStatus(finished){
        if(finished){
            this.quiz_begin=false;
        }
    }
  }
}
</script>

<style>

</style>