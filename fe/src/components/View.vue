<template>
  <div class="hello">
      {{msg}}
      {{view}}
  </div>
</template>

<script>

import {
  hello
} from '@/requests/request';

export default {
  mounted() {
    this.get();

  },
  name: 'HelloWorld',
  data: () =>({
      msg: 'Welcome to 中文',
      view: ""
  }),
  methods: {
    get() {
      hello().then((res) => {
        this.view = res;
      }).catch((error) => {
        this.view = error;
      });
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
