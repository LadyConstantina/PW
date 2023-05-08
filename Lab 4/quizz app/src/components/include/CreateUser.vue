<template>
    <div id="home" class="flex_center flex_column">
        <h1>Quizz Time</h1>
        <input type="text" id="name" class="log_in" placeholder="Your name?">
        <input type="text" id="surname" class="log_in" placeholder="Your surname?">
        <input type="submit" class="btn" id='SignBtn' value="Sign In">
    </div>
</template>

<script>
import axios from 'axios';

export default{
  name:'User',
  emits:['user'],
  data(){
        return {
            user_id: null,
            user_name: null,
            user_surname: null,
            test: 0
        }
  },
  methods: {
    postUser(){
        axios.post('https://late-glitter-4431.fly.dev/api/v54/users',
        {
            "data": {
                "name": this.user_name,
                "surname": this.user_surname
            }
        },
        {
          headers:{
            'X-Access-Token': '96acd180b7f8052903adfa55eb9f03a9d63bf4a2d29677c8cac0bb0a8ec6ae3f'
          }
        })
        .then(response => {
            this.user_id = response.data.id,
            this.$emit("user",response.data)
        })
        .catch(error => {
            console.log(error.message)
        })
    }
  },
  mounted(){
    localStorage.setItem('Quiz', JSON.stringify([0,0,undefined]));
    const button=document.querySelector('#SignBtn');
    button.addEventListener('click', event=>{
        this.user_name=document.getElementById('name').value
        this.user_surname=document.getElementById('surname').value
        if(!this.user_name){
            this.user_name = 'Alexei'
        }
        if(!this.user_surname){
            this.test += 1;
            this.user_surname = 'Șerșun (try '+String(this.test)+' )'
        }
        this.postUser()
    })
  }
}
</script>

<style>
.log_in{
    width: 100%;
    font-size:3rem;
    padding: 1rem 1rem;
    margin-bottom: 2rem;
    border-radius: 2rem;
    border: 0.5rem solid white;
}
</style>