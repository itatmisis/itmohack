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
        let txtValue = h3.textContent || h3.innerText;
        if (txtValue.indexOf(cath) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
    window.dispatchEvent(new Event('resize'));
}


document.addEventListener('click', function (e) {
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

(function () {
    let a = {}
    let formData = JSON.parse(localStorage.getItem("formData"));
    fetch("/send_profile", {
            method: 'POST',
            body: formData
        }).then(function (response) {
            return response.json();
        }).then(function (jsonData) {
            a = {"info": jsonData["data"] };
        });

    // let a = {
    //     "info": [
    //         {
    //             "title": "Manifolds Over Finite Fields",
    //             "author": "Philip Candelas, Xenia de la Ossa",
    //             "description": "We study Calabi-Yau manifolds defined over finite fields. These manifolds have parameters, which now also take values in the field and we compute the number of rational points of the manifold as a function of the parameters."
    //         },
    //         {
    //             "title": "Fusion in the W_3 algebra",
    //             "author": "G. M. T. Watts",
    //             "description": "We develop the notions of fusion for representations of the W_3 algebra along the lines of Feigin and Fuchs. We present some explicit calculations for a W_3 minimal model."
    //         },
    //         {
    //             "title": "Algebraic Structure in Non-Orientable Open-Closed String Field Theories",
    //             "author": "Naohito Nakazawa, Daiji Ennyu",
    //             "description": "We apply stochastic quantization method to real symmetric matrix-vector models for the second quantization of non-orientable strings, including both open and closed strings."
    //         }
    //     ]
    // }

//        alert(JSON.stringify(data.data));
    for (let i = 0; i < a.info.length; i++) {
        // alert(a.info[0].title)
        let val = JSON.stringify(a.info[i].title).toString();
        // alert('Meta: ' + val);
        let datatype;
        if (val != "Club") {
            datatype = "Организация";
        }
        let divClass = 'item Book';
        // alert(divClass);
        let newItem =
            '<div class=' + divClass + '>' +
            '<div class="content">' +
            '<div class="title">' +
            '<h3>' + a.info[i].title.toString() + '</h3>' +
            '<div class = "name">' + a.info[i].author.toString() + '</div>'
            + '</div>' +
            '<div class="desc">' +
            '<div class = "org_stock"></div>' +
            '<p>' + a.info[i].description.toString() + '</p>' +
            '</div>' +
            '</div>' +
            '</div>';

        let gridlist = document.getElementsByClassName("grid")[0];
        gridlist.insertAdjacentHTML('afterbegin', newItem);
    }
})();

var coll = document.getElementsByClassName("title");

for (let i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
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
