<template>
  <div id="app">
    <!-- <img alt="Vue logo" src="./assets/logo.png" /> -->
    <!-- <HelloWorld msg="Welcome to Your Vue.js App" /> -->

    <div class="container">
      <div class="row">
        <div class="col-8 mb-4 mx-auto">
          <form class="border px-2 py-3" v-on:submit="addPlaylist">
            <div class="form-group mb-3">
              <label for="playlistID float-left">Informe o ID da playlist</label>
              <input type="text" class="form-control" id="playlistID" v-model="playlist_id">
            </div>
            <button type="submit" class="btn btn-primary btn-block">Confirmar</button>
          </form>
        </div>
      
      <div class="" v-if="info">
        <div class="col-8 mb-4 mx-auto" v-for="(item, index) in info.data" :key="`item-${index}`">
          <b-card
            :title="item.titulo"
          >
            <youtube :video-id="getVideoId(item.link)" player-width="100%" player-height="300px"></youtube>

            <b-card-text>
              Publicado em: {{ formatDate(item.publicacao) }}
            </b-card-text>

            <b-card-text>
              Tags: {{ item.tags.join(', ') }}
            </b-card-text>
          </b-card>
        </div></div>
    </div>
    <div class="alert col-md-6 mb-4 mx-auto" role="alert" v-if="error_message">
      <p class="text-danger">{{ error_message }}</p>
    </div>
    <div class="alert col-md-6 mb-4 mx-auto" role="alert" v-if="loading">
      <p class="text-info">Aguarde...</p>
    </div>

  </div>
</div>
</template>

<script>
// import HelloWorld from "./components/HelloWorld.vue";
import axios from 'axios'
import moment from 'moment'
import VueYouTubeEmbed from 'vue-youtube-embed';

import Vue from "vue"
Vue.use(VueYouTubeEmbed)

var optionAxios = {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        }

export default {
  name: "App",
  data () {
    return {
      loading: false,
      info: null,
      playlist_id: null,
      error_message: ""
    }
  },
  methods: {
    formatDate: function(value) {
      return moment(String(value)).format('DD/MM/YYYY hh:mm')
    },
    getVideoId: function (url) {
      return this.$youtube.getIdFromURL(url)
    },
    getData: function() {

      playlist_id = this.playlist_id;
      if (this.isValidHttpUrl(this.playlist_id)) {
        var url_string = this.playlist_id;
        var url = new URL(url_string);
        var playlist_id = url.searchParams.get("list");
      }
      
      axios
        .get("api/videos/" + playlist_id, optionAxios)
        .then(response => {
          if (response.status == '200') {
            this.info = response;
            this.loading = false
          }
        }).catch(error => {
            this.error_message = "Ocorreu um erro, verifique se a URL ou Código da playlist está correta!" + error;
            this.loading = false
        })
    },
    addPlaylist: function(e){
      e.preventDefault()
      this.error_message = ""
      this.info = null
      this.loading = true
      this.getData()
    },
    isValidHttpUrl: function (string) {
      let url;
      
      try {
        url = new URL(string);
      } catch (_) {
        return false;  
      }

      return url.protocol === "http:" || url.protocol === "https:";
    }
  },
  // watch: {
  //     playlist_id: function(val) {
  //         if (val) {
  //             this.getData();
  //         }
  //     }
  // }
};


</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
