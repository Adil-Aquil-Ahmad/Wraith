function fetchNews(category) {
    document.getElementById("news-container").innerHTML = '<div class="loading-animation">' +
        '<div class="dot"></div>' +
        '<div class="dot"></div>' +
        '<div class="dot"></div>' +
        '<div class="dot"></div>' +
        '<div class="dot"></div>' +
    '</div>';

    $.get(`/data/${category}`, function(data) {
        let newsHTML = '';
        data.forEach(article => {
            newsHTML += `<div class="news-box">
                            ${article.image ? `<img src="${article.image}" alt="News Image">` :
                            '<div class="loading-animation">' +
                                '<div class="dot"></div>' +
                                '<div class="dot"></div>' +
                                '<div class="dot"></div>' +
                                '<div class="dot"></div>' +
                                '<div class="dot"></div>' +
                            '</div>'}
                            <h3>${article.title}</h3>
                            <a href="${article.link}" target="_blank">Read more</a>
                        </div>`;
        });
        document.getElementById("news-container").innerHTML = newsHTML;
    });
}

function shuffleNews() {
    let container = document.getElementById("news-container");
    let newsItems = Array.from(container.children);

    let positions = newsItems.map(item => item.getBoundingClientRect());

    for (let i = newsItems.length - 1; i > 0; i--) {
        let j = Math.floor(Math.random() * (i + 1));
        [newsItems[i], newsItems[j]] = [newsItems[j], newsItems[i]];
    }

    newsItems.forEach((item, index) => {
        let newPos = positions[index];
        let oldPos = item.getBoundingClientRect();
        
        let deltaX = newPos.left - oldPos.left;
        let deltaY = newPos.top - oldPos.top;

        item.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
        item.style.transition = "transform 0.5s ease-in-out";
    });

    setTimeout(() => {
        newsItems.forEach(item => {
            item.style.transform = "";
            item.style.transition = "";
            container.appendChild(item);
        });
    }, 500);
}

function filterNews() {
    let input = document.getElementById("news-search").value.toLowerCase();
    let newsBoxes = document.querySelectorAll(".news-box");

    newsBoxes.forEach(box => {
        let title = box.querySelector("h3").innerText.toLowerCase();
        if (title.includes(input)) {
            box.style.display = "block";
        } else {
            box.style.display = "none";
        }
    });
}
