<template>
  <div class="init">
    <div class="flexbox-container">
      <div class="small-info-column" @click="toggleLeftColumn" v-if="show_left_column">
        <div class='flexbox-item greeting'>{{greeting}}</div>
        <div id='clock' class='flexbox-item small-info'>
           <div v-if=showTimer>
             <button @click="stopTimer">STOP</button>
           <b @click="swapClockMode"> {{timer_count}} </b>
           </div>
           <b v-else @click="swapClockMode"> {{clock_str}} </b>          
        </div>
        <div class='flexbox-item small-info'>
          {{weather}}º
        </div>
        <div id='calendar' class='flexbox-item small-info'>
          {{clock.getDate()}}/{{clock.getMonth()+1}}/{{clock.getFullYear()}}
        </div>
          <!-- <button @click="getFeed()"> REFRESH </button> -->
      </div>
      <div v-if="!show_left_column" style="width: 250px;"  @click="show_left_column = true"></div>
      <!-- <div class="flexbox-container" style="width: 50px; background-color: red"></div> -->
        <div class='news-feed'>
          <ul>
            <li class=" article" v-for="article in result" :key="article.name">
              <b>{{article.source}} </b><br>
              <a :href=article.link>{{article.name}}</a>
              <a v-if=article.summary @click="showSummary(article.summary)">   [+]</a>
              <div v-if=show_summary @click="hideSummary()"> 
                <div v-if='article.summary==shown_summary' class="summary">
                {{shown_summary}}
                </div>
                </div>
            </li>
          </ul>

      </div>
    </div>
    <!-- <div>
      <a href="https://www.radio-ao-vivo.com/cbn-sp">CBN</a>
    </div> -->
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data(){
    return{
      showTimer: false,
      show_left_column: true,
      result_temp: [],
      result: [],
      clock: new Date(),
      clock_str: '',
      weather: '...',
      timer_start: new Date(),
      timer_count: '---',
      current_timer: '',
      shown_summary: '',
      show_summary: false,
      feed_started: false,

      intervalFunc: setInterval(() => {
        const now = new Date()
        const interval = now.getTime() - this.timer_start.getTime()
        this.timer_count = interval
      }, 1000),
    }
  },
  created(){
    this.getFeed();
    this.getWeather();
    this.getGreeting();
  },

  mounted() {
    this.updateClock();
    this.updateFeed();
    this.updateWeather();
    this.updateGreeting();
  },

  methods: {
    toggleLeftColumn(){
      this.show_left_column = !this.show_left_column
    },

    showSummary(content){
      this.shown_summary = content
      this.show_summary = true
    },

    hideSummary(){
      this.show_summary = false
    },

    swapClockMode(){
      this.showTimer = !this.showTimer
      this.stopTimer();
      this.startTimer();
      this.current_timer = this.intervalFunc();
    },
    
    getGreeting() {
      const now = new Date()
      const hour = now.getHours()
      if(hour > 4 && hour < 12){
        this.greeting = 'Bom dia, Piero.'
      } else if (hour >= 12 && hour <= 18){
        this.greeting = 'Boa tarde, Piero.'
      } else if (hour > 18 || hour == 0){
        this.greeting = 'Boa noite, Piero.'
      } else {
        this.greeting = 'Vai dormir, caralho.'
      }
    },

    getWeather(){
      fetch("http://192.168.100.112/weather", {
          "method": "GET",
        }).then(response => { 
          if(response.ok){
              return response.json()    
          } else{
              alert("Server returned " + response.status + " : " + response.statusText);
          }                
      })
      .then(response => {
        this.weather = response
      })
    },

    getFeed() {
      this.responseAvailable = false;
      fetch("http://192.168.100.112/news", {
          "method": "GET",
        })
        .then(response => { 
          if(response.ok){
              return response.json()    
          } else{
              alert("Server returned " + response.status + " : " + response.statusText);
          }                
      })
      .then(response => {
        console.log(response)
        for (var i = 0; i < response.length; i++){
          this.result_temp.push({
            source: response[i].source,
            name: response[i].title,
            link: response[i].link,
            summary: response[i].summary
          }); 
          
        }
          this.responseAvailable = true;
      })
      .catch(err => {
          console.log(err);
      });
      this.result = this.result_temp;
      console.log(this.result_temp)
      // I'm not sure why this is needed, but it doesn't work the
      // oubvious way... so there's that.
      if (this.feed_started){
        this.result_temp = []
      } else {
        this.feed_started = true
      }
      console.log(this.result_temp)
    },

    updateGreeting(){
      setInterval(this.getGreeting, 60000);
    },

    updateFeed(){
      setInterval(this.getFeed, 2 * 60 * 1000)
    },

    updateWeather(){
      setInterval(this.getWeather, 60000)
    },

    updateClock(){
      setInterval(() => {
        this.clock = new Date()
        this.clock_str = ('0' + this.clock.getHours()).slice(-2) + ':'
             + ('0' + (this.clock.getMinutes())).slice(-2) + ':'
             + ('0' + this.clock.getSeconds()).slice(-2)
      }, 1000)
    },

    startTimer(){
      this.timer_start = new Date()
    },
    
    countTimer(){
      setInterval(() => {
        const now = new Date()
        const interval = now.getTime() - this.timer_start.getTime()
        this.timer_count = interval
        // this.timer_count = ('0' + (now-this.timer_start).getHours()).slice(-2) + ':'
        //      + ('0' + ((now-this.timer_start).getMinutes()+1)).slice(-2) + ':'
        //      + ('0' + (now-this.timer_start).getSeconds()).slice(-2)
      }, 1000)
    },

    stopTimer(){
      clearInterval(this.intervalFunc)
      this.timer_count = 0
    }

  } 
}

</script>

<style scoped>
.init{
  /* width: 100% */
  display: flex;
  flex-direction: column;
}

.small-info-column {
  display: flex;
  flex-direction: row;
  width: 250px;
  flex-wrap: wrap;
} 

.flexbox-container {

  display: flex;
  color: white;
  justify-content: flex-start;
  min-height: 200px;
  flex-shrink: 1;
  /* height: 80vh; */
}

.flexbox-item {
  flex-grow: 1;
  width: 250px;
  margin: 10px;
  flex-shrink: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.greeting {
  /* min-height: 50px; */
  text-align: center;
}

.small-info {
  
  /* min-height: 50px; */
  font-size: 300%;
  text-align: center;
}

.news-feed {
  display: flex;
  min-width: 300px;
  width: 2000vh;
  height: 95vh;
  flex-basis: 1;
  margin: 0px;
  flex-shrink: 1;
  overflow-y: auto;
  /* scrollbar-width: none; /* Firefox */
  /* -ms-overflow-style: none;  IE and Edge */ 
}

.article {
  margin: 22px 0px 0px 0px;
  text-align: left;
  font-weight:100;
  padding: 10px;
  /* width: 90%; */
}

.summary {
  font-size: 150%;
  border: 4px solid rgb(0, 120, 156);
  border-radius: 15px;
  padding: 25px;
  /* width: 85%; */
}

/* 
.news-feed::-webkit-scrollbar {
  display: none;
} */

/* width */
::-webkit-scrollbar {
  width: 10px;
}

/* Track */
::-webkit-scrollbar-track {
  box-shadow: inset 0 0 5px grey; 
  border-radius: 10px;
}
 
/* Handle */
::-webkit-scrollbar-thumb {
  background: rgba(0, 4, 255, 0.418); 
  border-radius: 10px;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #006bb3; 
}

h3 {
  margin: 40px 0 0;
}
ul {
  /* display: inline; */
  list-style-type: none;
  padding: 0;
}
li {
  /* display: inline-block; */
  margin: 0 10px;
}
a {
  color: #ffffff;
  
}
a:link{
  text-decoration: none;
  font-size: 150%;
}

</style>
