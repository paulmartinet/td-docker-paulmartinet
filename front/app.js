fetch("/api/items")
  .then(r => r.json())
  .then(data => {
    const ul = document.getElementById("items");
    data.forEach(i => {
      const li = document.createElement("li");
      li.textContent = i.name;
      ul.appendChild(li);
    });
  });
