<script>
  import { onMount } from 'svelte';
  let view = 'home';
  let message = "Loading...";
  let token = "";
  let authError = "";
  let username = "", password = "", email = "";
  let posts = [];
  let newPostTitle = "";
  let newPostDesc = "";
  let newPostImage = "";
  let commentText = "";
  let selectedPostId = null;
  let comments = [];

  async function fetchHome() {
      try {
          const res = await fetch('http://localhost:5000/');
          const data = await res.json();
          message = data.message;
      } catch (e) {
          message = "Error fetching backend message";
      }
  }

  async function register() {
      authError = "";
      try {
          const res = await fetch('http://localhost:5000/api/register', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ username, email, password })
          });
          const data = await res.json();
          if(res.status === 201) {
              view = 'login';
          } else {
              authError = data.error || 'Registration failed';
          }
      } catch (e) {
          authError = "Error during registration";
      }
  }

  async function login() {
      authError = "";
      try {
          const res = await fetch('http://localhost:5000/api/login', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ username, password })
          });
          const data = await res.json();
          if(data.token) {
              token = data.token;
              view = 'posts';
              fetchPosts();
          } else {
              authError = data.error || 'Login failed';
          }
      } catch (e) {
          authError = "Error during login";
      }
  }

  async function fetchPosts() {
      try {
          const res = await fetch('http://localhost:5000/api/posts', {
              headers: {
                  'Authorization': 'Bearer ' + token
              }
          });
          posts = await res.json();
      } catch (e) {
          console.error(e);
      }
  }

  async function addPost() {
      try {
          const res = await fetch('http://localhost:5000/api/posts', {
              method: 'POST',
              headers: {
                  'Authorization': 'Bearer ' + token,
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({ title: newPostTitle, description: newPostDesc, image_url: newPostImage })
          });
          if(res.status === 201) {
              newPostTitle = "";
              newPostDesc = "";
              newPostImage = "";
              fetchPosts();
          }
      } catch (e) {
          console.error(e);
      }
  }

  async function fetchComments(postId) {
      selectedPostId = postId;
      try {
          const res = await fetch('http://localhost:5000/api/comments/' + postId, {
              headers: { 'Authorization': 'Bearer ' + token }
          });
          comments = await res.json();
      } catch (e) {
          console.error(e);
      }
  }

  async function addComment(postId) {
      try {
          const res = await fetch('http://localhost:5000/api/comments', {
              method: 'POST',
              headers: {
                  'Authorization': 'Bearer ' + token,
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({ content: commentText, post_id: postId })
          });
          if(res.status === 201) {
              commentText = "";
              fetchComments(postId);
          }
      } catch (e) {
          console.error(e);
      }
  }

  onMount(() => {
      fetchHome();
  });
</script>

<svelte:head>
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
</svelte:head>

<nav class="blue darken-3">
  <div class="nav-wrapper container">
    <a href="#" class="brand-logo">My App</a>
    <ul id="nav-mobile" class="right hide-on-med-and-down">
      <li><a on:click={() => view = 'home'}>Home</a></li>
      <li><a on:click={() => view = 'login'}>Login</a></li>
      <li><a on:click={() => view = 'register'}>Register</a></li>
      <li><a on:click={() => { if (token) view = 'posts' }}>Posts</a></li>
    </ul>
  </div>
</nav>

{#if view === 'home'}
  <div class="container" style="margin-top:20px;">
    <div class="card">
      <div class="card-content">
        <span class="card-title">Home</span>
        <p>{message}</p>
      </div>
    </div>
  </div>
{/if}

{#if view === 'register'}
  <div class="container" style="margin-top:20px;">
    <div class="card">
      <div class="card-content">
        <span class="card-title">Register</span>
        {#if authError}<p class="red-text">{authError}</p>{/if}
        <div class="input-field">
          <input id="username" type="text" placeholder="Username" bind:value={username}>
        </div>
        <div class="input-field">
          <input id="email" type="email" placeholder="Email" bind:value={email}>
        </div>
        <div class="input-field">
          <input id="password" type="password" placeholder="Password" bind:value={password}>
        </div>
      </div>
      <div class="card-action">
        <button class="btn blue" on:click={register}>Register</button>
      </div>
    </div>
  </div>
{/if}

{#if view === 'login'}
  <div class="container" style="margin-top:20px;">
    <div class="card">
      <div class="card-content">
        <span class="card-title">Login</span>
        {#if authError}<p class="red-text">{authError}</p>{/if}
        <div class="input-field">
          <input id="username" type="text" placeholder="Username" bind:value={username}>
        </div>
        <div class="input-field">
          <input id="password" type="password" placeholder="Password" bind:value={password}>
        </div>
      </div>
      <div class="card-action">
        <button class="btn blue" on:click={login}>Login</button>
      </div>
    </div>
  </div>
{/if}

{#if view === 'posts'}
  <div class="container" style="margin-top:20px;">
    <div class="card">
      <div class="card-content">
        <span class="card-title">Add Post</span>
        <div class="input-field">
          <input id="newPostTitle" type="text" bind:value={newPostTitle}>
          <label for="newPostTitle">Title</label>
        </div>
        <div class="input-field">
          <input id="newPostDesc" type="text" bind:value={newPostDesc}>
          <label for="newPostDesc">Description</label>
        </div>
        <div class="input-field">
          <input id="newPostImage" type="text" bind:value={newPostImage}>
          <label for="newPostImage">Image URL</label>
        </div>
      </div>
      <div class="card-action">
        <button class="btn blue" on:click={addPost}>Add Post</button>
      </div>
    </div>

    <div class="section">
      <h5>Post Listings</h5>
      {#each posts as post}
        <div class="card">
          <div class="card-content">
            <span class="card-title">{post.title}</span>
            <p>{post.description}</p>
            <p class="grey-text">{post.date_created}</p>
          </div>
          <div class="card-action">
            <button class="btn grey darken-2" on:click={() => fetchComments(post.id)}>View Comments</button>
          </div>
          {#if selectedPostId === post.id}
            <div class="card-panel">
              <h6>Comments</h6>
              {#each comments as comment}
                <p>{comment.content} <span class="grey-text">({comment.date_created})</span></p>
              {/each}
              <div class="input-field">
                <input id="commentText" type="text" bind:value={commentText}>
                <label for="commentText">Add Comment</label>
              </div>
              <button class="btn blue" on:click={() => addComment(post.id)}>Add Comment</button>
            </div>
          {/if}
        </div>
      {/each}
    </div>
  </div>
{/if}

<style>
  /* Custom Material Design overrides */
  body {
    font-family: 'Roboto', sans-serif;
  }
</style>
