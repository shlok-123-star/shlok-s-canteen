document.addEventListener("DOMContentLoaded", function () {

    const searchBox = document.getElementById("searchBox");

    if (!searchBox) return;

    searchBox.addEventListener("keyup", function () {

        let value = this.value.toLowerCase();

        let items = document.querySelectorAll(".menu-item");

        items.forEach(function(item){

            let name = item.querySelector(".item-name").innerText.toLowerCase();

            if(name.includes(value)){
                item.style.display = "";
            }else{
                item.style.display = "none";
            }

        });

    });

});