// extended by Vadim @eighonet Porvatov, special thanks to author of original template -- @lasjorg
$(document).ready(function () {
    var clbButton = document.getElementById('submit');
    clbButton.addEventListener('click', function (event) {

        let formData = new FormData()
        formData.append('organizations', JSON.stringify($('#survey-form').serializeArray()[0]["value"]))
        formData.append('keywords', JSON.stringify($('#survey-form').serializeArray()[1]["value"]))
        formData.append('description', JSON.stringify($('#survey-form').serializeArray()[2]["value"]))
        localStorage.setItem("formData", JSON.stringify(formData));

        fetch("/demo").then(r => {});

        event.preventDefault();
    });
});
