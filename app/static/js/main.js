        function SelectQueryType(clicked_id){
            document.getElementsByClassName("chooseOne")[0].innerHTML = clicked_id;
            document.getElementsByClassName("searchQuery")[0].disabled = false;
            seedString = clicked_id;
        }

        function SearchInput(){
            document.getElementById("power_hour").disabled = false;
        }
        function MakePowerHour() {
            var id_list = new Array();
            var song_list = new Array();            
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
                console.log(response);
                response.json().then( data => {
                    console.log(data);
                   
                    document.getElementById("loading").setAttribute("max", data.tracks.length)
                    document.getElementById("loading_label").removeAttribute("hidden");
                    document.getElementById("loading").removeAttribute("hidden");

                    let promises = []
                    var song_num = 1;
                    for (track of data.tracks) {
                        var trackCount = 1;
                        var song_name = track;
                        var new_songname = song_name.replace("-", "by")
                        song_list.push(song_num + ". " + new_songname);
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
                                console.log(data.video_id);
                                id_list.push(data.video_id);
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
                        if (id_list.length > 0) {
                            console.log(id_list);

                            document.getElementById("loading_label").setAttribute("hidden", true);
                            document.getElementById("loading").setAttribute("hidden", true); 
                            
                            //now move to new page with power hour
                            
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