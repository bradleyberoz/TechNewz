
const fetchNews = async (page, q)=>{
    console.log("Fetching news...");
    var url = 'https://newsapi.org/v2/everything?' +
          'q=' +q+
          '&from=2023-08-02&' +
          'pageSize=20&' +
          'language=en&' +
          'page=' +page+
          '&sortBy=popularity&' +
          'apiKey=1fcf667ddcf54e5db3bb887e60be09a6';

    var req = new Request(url);
    
    let a = await fetch(req)
    let response = await a.json()
    console.log(JSON.stringify(response))
        console.log(response)
    let str = ""
    resultCount.innerHTML = response.totalResults
    for (let item of response.articles){
      str = str + `<div class="card my-4 mx-2" style="width: 18rem;">
            <img src="${item.urlToImage}" class="card-img-top" alt="...">
            <div class="card-body">
              <h5 class="card-title">${item.title}</h5>
              <p class="card-text">${item.description}</p>
              <a href="${item.url}" target="_blank" class="btn btn-primary">Go somewhere</a>
            </div>
          </div>`
    }
    document.querySelector(".content").innerHTML = str

    }
    fetchNews(1, "sports")