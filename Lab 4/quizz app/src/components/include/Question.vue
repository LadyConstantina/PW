<template>
    <h1>{{ quiz_title }}</h1>
    <div class="question_box flex_center flex_column">
        <h3 id="score">Score:  {{ score }} | {{ quiz.length }}  </h3>
        <h3 id="question">{{question}}</h3>
        <div class="choice_container">
            <p class="choice_nr">A</p>
            <input type='button' id='resp0' class="choice_text" :value=answers[0] >
        </div>
        <div class="choice_container">
            <p class="choice_nr">B</p>
            <input type='button' id='resp1' class="choice_text" :value=answers[1] >
        </div>
        <div class="choice_container">
            <p class="choice_nr">C</p>
            <input type='button' id='resp2' class="choice_text" :value=answers[2] >
        </div>
        <div class="choice_container">
            <p class="choice_nr">D</p>
            <input type='button' id='resp3' class="choice_text" :value=answers[3] >
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import emitter from 'tiny-emitter/instance';

export default{
  name:'Question',
  emits:['status_quiz'],
  data(){
        return {
            quiz_id: 0,
            user_id: 0,
            question_id: 0,
            quiz_title:'',
            quiz:[],
            question:'',
            answers:[],
            score: 0,
            quiz_finished: false,
            answer: null,
            correct_answer:'',
            correct_status:null
        }
  },
  methods: {
    getQuiz(){
        axios.get(`https://late-glitter-4431.fly.dev/api/v54/quizzes/${this.quiz_id}`,
        {
          headers:{
            'X-Access-Token': '96acd180b7f8052903adfa55eb9f03a9d63bf4a2d29677c8cac0bb0a8ec6ae3f'
          }, 
          params:{
            "user_id": String(this.user_id)
          }
        })
        .then(response=>{
                this.quiz = response.data.questions
                this.quiz_title = response.data.title
                this.question = this.quiz[this.question_id].question
                this.answers = this.quiz[this.question_id].answers
        }
        )
    },
    submitAnswer(){
        if (this.answer != '') {
            axios.post(`https://late-glitter-4431.fly.dev/api/v54/quizzes/${this.quiz_id}/submit`,
            {
                "data": {
                    "question_id": this.quiz[this.question_id].id,
                    "answer": this.answer,
                    "user_id": this.user_id
                }
            },{
                headers:{'X-Access-Token': '96acd180b7f8052903adfa55eb9f03a9d63bf4a2d29677c8cac0bb0a8ec6ae3f'}
            }
            )
            .then(response =>{
                this.correct_answer = response.data.correct_answer
                this.correct_status = response.data.correct
                if (response.data.correct){
                    this.score += 1
                }
                this.showAnswer()
            }
            )
        }
    },
    setAnswer(){
        if (this.quiz_finished){
            this.$emit("status_quiz",true)
        }else{
        this.answer = String(event.target.value)
        this.submitAnswer()
        }
    },
    sleep(time){
        return new Promise((resolve) => setTimeout(resolve, time));
    },
    showAnswer(){
        const id_answer_user = this.answers.indexOf(this.answer)
        const id_answer_correct = this.answers.indexOf(this.correct_answer)
        const elm = document.getElementById("resp"+String(id_answer_correct)).classList.add('correct_answer')
        if (id_answer_correct != id_answer_user) {
            const elm = document.getElementById("resp"+String(id_answer_user)).classList.add('wrong_answer')
        }
        this.sleep(800).then(() => {
            const elm = document.getElementById("resp"+String(id_answer_correct)).classList.remove('correct_answer')
            if (id_answer_correct != id_answer_user) {
                const elm = document.getElementById("resp"+String(id_answer_user)).classList.remove('wrong_answer')
            }
            if(this.question_id == (this.quiz.length -1)){
                const elm = document.getElementById("question").classList.add('congratulations')
                this.question="Congratulations! You just finished the Quiz '"+this.quiz_title+"' with score "+String(this.score)+"!"
                this.answers=["Click Me!","Click Me!","Click Me!","Click Me!"]
                this.quiz_finished = true
            }else{
                this.answer = ''
                this.question_id += 1
                this.question = this.quiz[this.question_id].question
                this.answers = this.quiz[this.question_id].answers
            }
        }); 
    }
  },
  mounted(){
    const ref = localStorage.getItem('Quiz');
    if (ref) {
      let data = JSON.parse(ref);
      this.quiz_id = data[0];
      this.user_id = data[1];
    }
    this.getQuiz()
    let el = document.getElementById("resp0");
    el.addEventListener('click',this.setAnswer);
    el = document.getElementById("resp1");
    el.addEventListener('click',this.setAnswer);
    el = document.getElementById("resp2");
    el.addEventListener('click',this.setAnswer);
    el = document.getElementById("resp3");
    el.addEventListener('click',this.setAnswer);
  }
}
</script>

<style>
.question_box {
    padding: 2rem 3rem;
    width: 100%;
    background-color: white;
    text-align: center;
    border-radius: 2rem;
}

.correct_answer{
    background-color: rgb(119, 241, 110);
}
.wrong_answer{
    background-color: rgb(219, 93, 93);
    color: white;
}
#score{
    font-family: 'Barlow';
    font-size: 4rem;
    background-image: linear-gradient(#7928CA, #FF0080);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.congratulations{
    background-image: linear-gradient(#7928CA, #FF0080);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>