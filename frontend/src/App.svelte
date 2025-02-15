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
  let newPostImageFile = null;
  let newPostImageInput;
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
              window.sessionStorage.setItem("token", token);
              window.sessionStorage.setItem("username", data.username);
              window.sessionStorage.setItem("userId", data.user_id);
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

  async function fetchMyPosts() {
    try {
          const res = await fetch(`http://localhost:5000/api/posts/${window.sessionStorage.getItem("userId")}`, {
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
      const formData = new FormData();
      formData.append("title", newPostTitle);
      formData.append("description", newPostDesc);
      formData.append("image", newPostImageInput.files[0]);

      try {
          const res = await fetch('http://localhost:5000/api/posts', {
              method: 'POST',
              headers: {
                  'Authorization': 'Bearer ' + token,
                  // 'Content-Type': 'multipart/form-data'
              },
              body: formData
          });
          if(res.status === 201) {
              newPostTitle = "";
              newPostDesc = "";
              newPostImageFile = null;
              fetchPosts();
          }

          alert('Post succesfully added!')
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

      token = window.sessionStorage.getItem("token") || "";
  });
</script>

<svelte:head>
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
</svelte:head>

<nav class="blue darken-3">
  <div class="nav-wrapper container">
    <a href="/" class="brand-logo">PC-Party</a>
    <ul id="nav-mobile" class="right hide-on-med-and-down">
      <li><a on:click={() => {fetchPosts() ; view = 'home'}}>Home</a></li>
      {#if !token}
        <li><a on:click={() => view = 'login'}>Login</a></li>
        <li><a on:click={() => view = 'register'}>Register</a></li>
      {/if}
      {#if !!token}
        <li><a on:click={() => { if (token) view = 'addPost' }}>Add post</a></li>
        <li><a on:click={() => {fetchMyPosts(); view = "myPosts"}}>My posts</a></li>
        
        <li><a on:click={() => {
          view = "home";
          window.sessionStorage.removeItem("token");
          window.sessionStorage.removeItem("username");
          window.sessionStorage.removeItem("userId");
          token = "";
        }}>Logout</a></li>
      {/if}
    </ul>
  </div>
</nav>

<!-- {#if view === 'home'}
  <div class="container" style="margin-top:20px;">
    <div class="card">
      <div class="card-content">
        <span class="card-title">Home</span>
        <p>{message}</p>
      </div>
    </div>
  </div>
{/if} -->

{#if view === 'register'}
  <div class="container" style="margin-top:20px;">
    <div class="card">
      <div class="card-content">
        <span class="card-title">Register</span>
        {#if authError}<p class="red-text">{authError}</p>{/if}
        <div class="input-field">
          <input id="username" type="text" bind:value={username}>
          <label for="username">Username</label>
        </div>
        <div class="input-field">
          <input id="email" type="email" bind:value={email}>
          <label for="email">Email</label>
        </div>
        <div class="input-field">
          <input id="password" type="password" bind:value={password}>
          <label for="password">Password</label>
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
          <input id="login-username" type="text" bind:value={username}>
          <label for="login-username">Username</label>
        </div>
        <div class="input-field">
          <input id="login-password" type="password" bind:value={password}>
          <label for="login-password">Password</label>
        </div>
      </div>
      <div class="card-action">
        <button class="btn blue" on:click={login}>Login</button>
      </div>
    </div>
  </div>
{/if}

{#if view === 'home'}
  <div class="container" style="margin-top:20px;">
    <div class="section">
      <h5>Posts</h5>
      {#each posts as post}
        <div class="card">
          <div class="card-content">
            <span class="card-title">{post.title}</span>
            <p class="grey-text">{post.author}, {post.date_created}</p>
            <p>{post.description}</p>
            <p>
              <img src={`http://localhost:5000/api/image/${post.filename}`} alt={post.description}/>
            </p>
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

{#if view === 'addPost'}
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
        <input id="newPostImage" type="file" bind:value={newPostImageFile} bind:this={newPostImageInput}>
        <!-- <label for="newPostImage">Image</label> -->
      </div>
    </div>
    <div class="card-action">
      <button class="btn blue" on:click={addPost}>Add Post</button>
    </div>
  </div>
{/if}
{#if view === 'myPosts'}
    <div class="section">
      <h5>My posts</h5>
      {#each posts as post}
        <div class="card">
          <div class="card-content">
            <span class="card-title">{post.title}</span>
            <p class="grey-text">{post.author}, {post.date_created}</p>
            <p>{post.description}</p>
            <p>
              <img src={`http://localhost:5000/api/image/${post.filename}`} alt={post.description}/>
            </p>
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
{/if}

<style>
  /* Custom Material Design overrides */
  body {
    font-family: 'Roboto', sans-serif;
  }
</style>
