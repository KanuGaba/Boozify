// GLOBAL VARS
var seedString;
var genres = ['acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'anime', 'black-metal', 'bluegrass', 'blues', 'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop', 'chicago-house', 'children', 'chill', 'classical', 'club', 'comedy', 'country', 'dance', 'dancehall', 'death-metal', 'deep-house', 'detroit-techno', 'disco', 'disney', 'drum-and-bass', 'dub', 'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 'funk', 'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove', 'grunge', 'guitar', 'happy', 'hard-rock', 'hardcore', 'hardstyle', 'heavy-metal', 'hip-hop', 'holidays', 'honky-tonk', 'house', 'idm', 'indian', 'indie', 'indie-pop', 'industrial', 'iranian', 'j-dance', 'j-idol', 'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin', 'latino', 'malay', 'mandopop', 'metal', 'metal-misc', 'metalcore', 'minimal-techno', 'movies', 'mpb', 'new-age', 'new-release', 'opera', 'pagode', 'party', 'philippines-opm', 'piano', 'pop', 'pop-film', 'post-dubstep', 'power-pop', 'progressive-house', 'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'rainy-day', 'rap', 'reggae', 'reggaeton', 'road-trip', 'rock', 'rock-n-roll', 'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo', 'show-tunes', 'singer-songwriter', 'ska', 'sleep', 'songwriter', 'soul', 'soundtracks', 'spanish', 'study', 'summer', 'swedish', 'synth-pop', 'tango', 'techno', 'trance', 'trip-hop', 'turkish', 'work-out', 'world-music'];

function SelectQueryType(clicked_id) {
    // Update button text and enable power hour button
    document.getElementsByClassName("chooseOne")[0].innerHTML = clicked_id;
    document.getElementsByClassName("searchQuery")[0].disabled = false;
    seedString = clicked_id;

    // Autocomplete for Genre field
    if (clicked_id=="Genre") {
        autocomplete(document.getElementById("search"), genres, true);
    } else {
        autocomplete(document.getElementById("search"), genres, false);
    }
}

function autocomplete(inp, arr, isGenre) {
    var currentFocus;
    var _listener = function(e) {
        // Hacky fix to remove eventListener
        if (document.getElementsByClassName("chooseOne")[0].innerHTML != "Genre") {
            return;
        }
        var a, b, i, val = this.value;
        // close any already open lists of autocompleted values
        closeAllLists();
        if (!val) { return false; }
        currentFocus = -1;
        // create a DIV element that will contain the items (values):
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        // append the DIV element as a child of the autocomplete container:
        this.parentNode.appendChild(a);
        for (i = 0; i < arr.length; i++) {
            // check if the item starts with the same letters as the text field value:
            if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                // create a DIV element for each matching element:
                b = document.createElement("DIV");
                // make the matching letters bold:
                b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                b.innerHTML += arr[i].substr(val.length);
                // insert a input field that will hold the current array item's value:
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                // execute a function when someone clicks on the item value (DIV element):
                b.addEventListener("click", function(e) {
                    // insert the value for the autocomplete text field:*/
                    inp.value = this.getElementsByTagName("input")[0].value;
                    // close the list of autocompleted values
                    closeAllLists();
                });
                a.appendChild(b);
            }
        }
    }

    if (!isGenre) {
        inp.removeEventListener("input", _listener, true); // NOT WORKING??
    } else {
        inp.addEventListener("input", _listener);
        /*execute a function presses a key on the keyboard:*/
        inp.addEventListener("keydown", function(e) {
            var x = document.getElementById(this.id + "autocomplete-list");
            if (x) x = x.getElementsByTagName("div");
            if (e.keyCode == 40) {
                /*If the arrow DOWN key is pressed,
                increase the currentFocus variable:*/
                currentFocus++;
                /*and and make the current item more visible:*/
                addActive(x);
            } else if (e.keyCode == 38) { //up
                /*If the arrow UP key is pressed,
                decrease the currentFocus variable:*/
                currentFocus--;
                /*and and make the current item more visible:*/
                addActive(x);
            } else if (e.keyCode == 13) {
                /*If the ENTER key is pressed, prevent the form from being submitted,*/
                e.preventDefault();
                if (currentFocus > -1) {
                /*and simulate a click on the "active" item:*/
                if (x) x[currentFocus].click();
                }
            }
        });

        function addActive(x) {
            /*a function to classify an item as "active":*/
            if (!x) return false;
            /*start by removing the "active" class on all items:*/
            removeActive(x);
            if (currentFocus >= x.length) currentFocus = 0;
            if (currentFocus < 0) currentFocus = (x.length - 1);
            /*add class "autocomplete-active":*/
            x[currentFocus].classList.add("autocomplete-active");
        }

        function removeActive(x) {
            /*a function to remove the "active" class from all autocomplete items:*/
            for (var i = 0; i < x.length; i++) {
                x[i].classList.remove("autocomplete-active");
            }
        }

        function closeAllLists(elmnt) {
            /*close all autocomplete lists in the document,
            except the one passed as an argument:*/
            var x = document.getElementsByClassName("autocomplete-items");
            for (var i = 0; i < x.length; i++) {
                if (elmnt != x[i] && elmnt != inp) {
                    x[i].parentNode.removeChild(x[i]);
                }
            }
        }

        /*execute a function when someone clicks in the document:*/
        document.addEventListener("click", function (e) {
            closeAllLists(e.target);
        });
    }
}

function SearchInput() {
    // Disable power hour button if search value is empty
    if (document.getElementById('search').value == "") {
        document.getElementById("power_hour").disabled = true;
    }
    else {
        document.getElementById("power_hour").disabled = false;
    }
}

// Highlight text input red if bad input
function searchError() {
    var searchElem = document.getElementById("search");
    var delay = 100;
    var delayer = setInterval(function() {
        if(delay > 0){
            searchElem.style.backgroundColor = "#ff0000";
            delay--;
        }
        else{
            searchElem.value = "";
            searchElem.style.backgroundColor = "white";
            document.getElementById("power_hour").disabled = true;
            clearInterval(delayer);
        }
    }, 1);
}

function MakePowerHour() {
    // Check if genre input is in genres list
    if (seedString == "Genre") {
        if (!genres.includes(document.getElementById('search').value)) {
            searchError();
            return;
        }
    }

    // Disable power hour button and search input
    document.getElementsByClassName("searchQuery")[0].disabled = true;
    document.getElementById("power_hour").disabled = true;

    // Get all tracks from Spotify          
    fetch("/get-tracks", {
        method: "POST",
        headers: new Headers({
            "content-type": "application/json"
        }),
        body: JSON.stringify({
            "seed": seedString,
            "search": document.getElementById('search').value,
        })
    })
    .then(function(response) {
        response.json().then( data => {
            console.log("Tracks Found: " + data.tracks);

            // Check if Spotify API produced an error
            if (data.tracks.length == 0) {
                document.getElementsByClassName("searchQuery")[0].disabled = false;
                searchError();
                return;
            }

            // Unhide loading bar
            document.getElementById("loading").setAttribute("max", data.tracks.length);
            document.getElementById("loading_label").removeAttribute("hidden");
            document.getElementById("loading").removeAttribute("hidden");

            let promises = [];
            var song_num = 1;
            var song_list = new Array();
            for (track of data.tracks) {
                // Modify song name to make it user friendly
                var song_name = track;
                var new_songname = song_name.replace("-", "by")
                song_list.push(song_num + ". " + new_songname);
                song_num++;

                // Get video id for each track
                var trackCount = 1;
                promises.push(
                    fetch("/get-video-id", {
                        method: "POST",
                        headers: new Headers({
                            "content-type": "application/json"
                        }),
                        body: JSON.stringify({
                            "track": track,
                        })
                    })
                    .then((response) => {
                        return response.json();
                    })
                    .then(function(data) {
                        console.log("Video ID Found: " + data.video_id);

                        // Update loading bar
                        document.getElementById("loading").setAttribute("value", trackCount);
                        document.getElementById("loading").innerHTML = trackCount + "%";
                        ++trackCount;

                        // Return promise with video id
                        return Promise.resolve(data.video_id);
                    })
                    .catch(console.error)
                );
            }
            Promise.all(promises).then(function(id_list) {
                console.log("Video ID List: " + id_list);

                if (id_list.length > 0) {                   
                    // Move to new page with power hour, storing info
                    sessionStorage.setItem("id_list", JSON.stringify(id_list));
                    sessionStorage.setItem("song_list", JSON.stringify(song_list));
                    window.location = '/powerhour';
                } else {
                    // Reset searchQuery
                    document.getElementsByClassName("searchQuery")[0].disabled = false;
                    searchError();
                    return;
                }
            })
        });
    })
    .catch(console.error);
}