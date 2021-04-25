function searchText() {
    // Declare variables
    var input, filter, ul, li, p, txtValue;
    input = document.getElementById('myInput');
    filter = input.value.toUpperCase();
    li = document.getElementsByClassName('item');

    // Loop through all list items, and hide those who don't match the search query
    for (let i = 0; i < li.length; i++) {
        let description = li[i].getElementsByClassName("desc")[0];
        p = description.getElementsByTagName("p")[0];
        txtValue = p.textContent || p.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
    window.dispatchEvent(new Event('resize'));
}



function filterThemes(cath) {
//    alert(cath)
    let menu = document.getElementById('myDropdown');
    let li = document.getElementsByClassName('item');
    for (let i = 0; i < li.length; i++) {
        let description = li[i].getElementsByClassName("title")[0];
        let h3 = description.getElementsByTagName("h3")[0];
        let txtValue = h3.textContent || h3 .innerText;
        if (txtValue.indexOf(cath) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
    window.dispatchEvent(new Event('resize'));
}


document.addEventListener('click', function(e) {
    e = e || window.event;
    let target = e.target || e.srcElement;
    let text = target.textContent || target.innerText;
    if ((target.className == "books") || (target.className == "events") || (target.className == "org") || (target.className == "gen")) {
        if (target.className == "gen") {
            filterThemes("");
        } else {
            filterThemes(text);
        }
    }
/*    if (target.className == "title") {
       alert(target.parentElement.querySelector(".desc").className);

        $(target.parentElement.querySelector(".desc")).hide();
    }
 */
}, false);

document.getElementsByClassName("logout")[0].addEventListener('click', function(e) {
    window.location.href = 'index.html';
});


(function() {
    let username = localStorage.getItem("key")
    const proxyurl = 'https://cors-anywhere.herokuapp.com/' + 'http://135.181.109.111/items/get/' + username;
//    alert(proxyurl);
    fetch(proxyurl).then((response) => {
        return response.json();
    }).then((data) => {
//        alert(JSON.stringify(data));

//        alert(JSON.stringify(data.data));

        for (let i = 0; i < data.data.length; i++) {

            let val = JSON.stringify(data.data[i].metatype).toString();
            alert('Meta: ' + val);
            let datatype;
            if (val == "Book") {
                datatype = "Книга";
            }
            if (val == "Club") {
                datatype = "Организация";
            }
            if (val == "Event") {
                datatype = "Мероприятие";
            }
            let divClass = 'item Book';
            alert(divClass);
            let newItem =
            '<div class=' + divClass + '>' +
            '<div class="content">' +
            '<div class="title">' +
            '<h3>' + datatype + '</h3>' +
                '<div class = "name">' + data.data[i].title.toString() + '</div>'
                +'</div>' +
            '<div class="desc">' +
            '<div class = "org_stock"></div>' +
            '<p>' + data.data[i].description.toString() + '</p>' +
            '</div>' +
            '</div>' +
            '</div>';

                let gridlist = document.getElementsByClassName("grid")[0];
                gridlist.insertAdjacentHTML('afterbegin',  newItem);
        }
    });
})();

var coll = document.getElementsByClassName("title");

for (let i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = this.parentElement.querySelector(".desc");
        if (content.style.display === "block") {
            content.style.display = "none";
        } else {
            content.style.display = "block";
        }
        window.dispatchEvent(new Event('resize'));
    });
}
