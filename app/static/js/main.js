// GLOBAL VARS
var seedString;
var genres = ['acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'anime', 'black-metal', 'bluegrass', 'blues', 'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop', 'chicago-house', 'children', 'chill', 'classical', 'club', 'comedy', 'country', 'dance', 'dancehall', 'death-metal', 'deep-house', 'detroit-techno', 'disco', 'disney', 'drum-and-bass', 'dub', 'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 'funk', 'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove', 'grunge', 'guitar', 'happy', 'hard-rock', 'hardcore', 'hardstyle', 'heavy-metal', 'hip-hop', 'holidays', 'honky-tonk', 'house', 'idm', 'indian', 'indie', 'indie-pop', 'industrial', 'iranian', 'j-dance', 'j-idol', 'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin', 'latino', 'malay', 'mandopop', 'metal', 'metal-misc', 'metalcore', 'minimal-techno', 'movies', 'mpb', 'new-age', 'new-release', 'opera', 'pagode', 'party', 'philippines-opm', 'piano', 'pop', 'pop-film', 'post-dubstep', 'power-pop', 'progressive-house', 'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'rainy-day', 'reggae', 'reggaeton', 'road-trip', 'rock', 'rock-n-roll', 'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo', 'show-tunes', 'singer-songwriter', 'ska', 'sleep', 'songwriter', 'soul', 'soundtracks', 'spanish', 'study', 'summer', 'swedish', 'synth-pop', 'tango', 'techno', 'trance', 'trip-hop', 'turkish', 'work-out', 'world-music'];

function SelectQueryType(clicked_id){
    document.getElementsByClassName("chooseOne")[0].innerHTML = clicked_id;
    document.getElementsByClassName("searchQuery")[0].disabled = false;
    seedString = clicked_id;
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
      if (!val) { return false;}
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

function SearchInput(){
    document.getElementById("power_hour").disabled = false;
}

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
            clearInterval(delayer);
        }
    }, 1);
}

function MakePowerHour() {
    if (seedString == "Genre") {
        if (!genres.includes(document.getElementById('search').value)) {
            searchError();
            return;
        }
    }

    document.getElementsByClassName("searchQuery")[0].disabled = true;
    document.getElementById("power_hour").disabled = true;

    var id_list = new Array();
    var song_list = new Array();   
    let song_location = new Map();      
    let id_map = new Map();   
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
        //console.log(response);
        response.json().then( data => {
            console.log(data);

            // Check if Spotify API produced an error
            if (data.tracks.length == 0) {
                document.getElementsByClassName("searchQuery")[0].disabled = false;
                document.getElementById("power_hour").disabled = false;
                searchError();
                return;
            }

            document.getElementById("loading").setAttribute("max", data.tracks.length)
            document.getElementById("loading_label").removeAttribute("hidden");
            document.getElementById("loading").removeAttribute("hidden");

            let promises = []
            var song_num = 1;
            for (track of data.tracks) {
                var trackCount = 1;
                var song_name = track;
                var new_songname = song_name.replace("-", "by")
                song_location.set(song_list.length, track);
                song_list.push(song_num + ". " + new_songname);
                console.log(song_location);
                song_num++;
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

                        console.log(data.video_id + " -> " + data.track);
                        //id_list.push(data.video_id);
                        id_map.set(data.track, data.video_id);
                        console.log(id_map);
                        document.getElementById("loading").setAttribute("value", trackCount);
                        document.getElementById("loading").innerHTML = trackCount + "%";
                        ++trackCount;
                        return Promise.resolve();
                    })
                    .catch(console.error)
                );
            }
            //! ************************************
            Promise.all(promises).then(function() {
                console.log(id_map);
                if (id_map.size > 0) {
                    for(var i = 0; i < song_list.length; i++){
                        id_list.push(id_map.get(song_location.get(i)));
                    }


                    //console.log(id_list);

                    document.getElementById("loading_label").setAttribute("hidden", true);
                    document.getElementById("loading").setAttribute("hidden", true); 
                    
                    //now move to new page with power hourg
                    
                    sessionStorage.setItem("id_list", JSON.stringify(id_list));
                    sessionStorage.setItem("song_list", JSON.stringify(song_list));
                    window.location = '/powerhour';
                }else{
                    throw "Search results empty";
                }
            })

        });
    })
    .catch(console.error);
}