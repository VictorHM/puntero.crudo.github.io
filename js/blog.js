fetch('../blog/posts.json')
  .then(response => response.json())
  .then(posts => {
    const container = document.getElementById('post-list');
    posts.sort((a, b) => new Date(b.date) - new Date(a.date));

    posts.forEach(post => {
      const article = document.createElement('article');
      article.innerHTML = `
        <h3><a href="${post.url}">${post.title}</a></h3>
        <small>${post.date}</small>
        <p>${post.excerpt}</p>
      `;
      container.appendChild(article);
    });
  })
  .catch(error => {
    console.error("Error cargando posts.json:", error);
  });
