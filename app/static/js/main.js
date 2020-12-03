// GLOBAL VARS
var seedString;
var player;
var start = 0;
var end = start + 60;

var id_list = new Array();
var song_num = 0;
var event_trigger = 1;
var first_played = false;
var lastSong;

function onYouTubeIframeAPIReady() {
    console.log("youtube api installed");
}

function onPlayerStateChange(event) {
    if (event.data != YT.PlayerState.PLAYING && first_played){
        console.log("beer image");
    }
    console.log("player state: ", event.data);
    if (event.data == YT.PlayerState.PLAYING && first_played == false){
        first_played = true;
    }

    if (event.data == YT.PlayerState.ENDED){
        if (event_trigger == 0){
            event_trigger = 1;
            console.log("double fire");
            return;
        }
        else {
            console.log(id_list.length, " big boy");
            console.log("first fire");
            event_trigger = 0;
        }
        //if (player.videoId == lastSong){
        //console.log("we outtie");
        //console.log(lastSong);
        //player.destroy();
        //}
        if (song_num >= id_list.length) {
        //  console.log("end player");
            //console.log(song_num);
            song_num = 0;
            id_list = new Array();
            player.destroy();
        }
        //loads and plays next video
        //player.loadVideoById(id);
        console.log("player ended");
        player.loadVideoById({videoId:id_list[song_num], endSeconds:60});
        song_num += 1;
        console.log(song_num);
    }
}

function stopVideo() {
    player.stopVideo();
}

function SelectQueryType(clicked_id){
    document.getElementsByClassName("chooseOne")[0].innerHTML = clicked_id;
    document.getElementsByClassName("searchQuery")[0].disabled = false;
    seedString = clicked_id;
}

function SearchInput(){
    document.getElementById("power_hour").disabled = false;
}

function MakePowerHour() {
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
        response.json().then( data => {//function(data) {
            console.log(data);

            document.getElementById("loading").setAttribute("max", data.tracks.length)
            document.getElementById("loading_label").removeAttribute("hidden");
            document.getElementById("loading").removeAttribute("hidden");

            let promises = []
            for (track of data.tracks) {
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
            Promise.all(promises).then(function() {
                console.log(id_list);

                document.getElementById("loading_label").setAttribute("hidden", true);
                document.getElementById("loading").setAttribute("hidden", true);            
        
                if (id_list.length > 0) {
                    lastSong = id_list[id_list.length - 1];
                    
                    player = new YT.Player('player', {
                        height: '100%',
                        width: '100%',
                        videoId: id_list[0],
                        // videoId: 'M7lc1UVf-VE',
                        playerVars: {
                            start: start,
                            end: end,
                            controls: 0,
                            disablekb: 1,
                            fs: 1
                        },
                        events: {
                            //'onReady': onPlayerReady,
                            'onStateChange': onPlayerStateChange
                        }
                    });
                    song_num += 1;
                }
            })
        });
    })
    .catch(console.error);
    //if id_list is not empty then load the youtube player
}

function DestroyPowerHour() {
   // document.getElementById("deactivate").disabled = true;
    player.destroy();
    id_list = new Array();
    song_num = 0;
}