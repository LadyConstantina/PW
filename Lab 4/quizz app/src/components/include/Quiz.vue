
<script>
import axios from 'axios';
import emitter from 'tiny-emitter/instance';

export default{
  name:'Quiz',
  props:{
      user: Object
  },
  emits:['quiz_start'],
  data(){
    return{
        quizes: [],
        quiz_id: null,
        quiz_nr:0,
        user_id: this.user.id,
        quiz_finished: []
    }
  },
  methods:{
    getQuizes(){
        axios.get('https://late-glitter-4431.fly.dev/api/v54/quizzes',
        {
          headers:{'X-Access-Token': '96acd180b7f8052903adfa55eb9f03a9d63bf4a2d29677c8cac0bb0a8ec6ae3f'}
        })
        .then(resp => {
          this.quizes = resp.data;
          this.quiz_nr = this.quizes.length;
          const ref = localStorage.getItem('Quiz');
          if(ref){
              let data = JSON.parse(ref);
              this.quiz_finished = data[2];
          }
          if(!this.quiz_finished){
              this.quiz_finished = Array(this.quizes.length).fill(false);
          }
          this.showQuizes()
        }
        )
    },
    showQuizes(){
      const box = document.getElementById('quizes');
      for (let index = 0; index < this.quiz_nr; index++) {
        if(this.quiz_finished[index] == false) {
          const node= document.createElement("div");
          node.setAttribute('class','quiz_item');
          node.innerHTML=`
          <div class="quiz_item">
            <p class="quiz_title"> ${this.quizes[index].title }</p>
            <input type="button" id="q${index}" class='play_btn' value="Play">
          </div>
          `
          box.append(node)
          node.addEventListener('click', event => this.playQuiz(event))
        }
      }
      if(box.hasChildNodes() == false){
        const node= document.createElement("div");
          node.innerHTML=`
          <h3>Ups! Looks like you played all the games. Congratulations!</h3>
          `
          box.append(node)
      }
    },
    playQuiz(event){
      const id = Number(event.target.id.charAt(1));
      this.quiz_finished[id] = true;
      localStorage.setItem('Quiz', JSON.stringify([this.quizes[id].id,this.user_id,this.quiz_finished]));
      this.$emit("quiz_start",this.quizes[id].id);
    }
  },
  mounted(){
    this.getQuizes()
  }
}
</script>

<template>
  <h1 class="welcome text_center">Let's Play, {{ user.name }} {{ user.surname }}!</h1>
  <div id="quizes">
  </div>
</template>

<style>
@import url('https://fonts.cdnfonts.com/css/waltograph');
.welcome{
  color:#d93bae;
  font-size: 8rem;
  padding: 2rem 2rem;
  margin-top:30%;
}
#quizes{
  padding: 2rem 3rem;
    width: 100%;
    background-color: white;
    text-align: center;
    border-radius: 2rem;
}
.quiz_title {
  color:white;
  font-size: 7rem;
  font-family: 'Waltograph', sans-serif;
  padding: 1rem 2rem;
}
.quiz_item{
  width: 100%;
    background-image: linear-gradient(25deg,#ff00d4, #00ddff);
    text-align: center;
    border-radius: 2rem;
    margin-bottom: 2rem;
}
.play_btn{
  cursor: pointer;
  padding: 0.7rem 0.8rem;
  margin-bottom: 1rem;
  margin-top: 1rem;
  font-size: 3rem;
  border: none;
  background-color: transparent;
  color: white;
  border-radius: 3rem;
}
.play_btn:hover {
  cursor: pointer;
  box-shadow: 0 1rem 4rem 1rem rgba(255, 255, 255, 1);
  transform: translateY(-0.1rem);
  transition: transform 150ms;
}
</style>