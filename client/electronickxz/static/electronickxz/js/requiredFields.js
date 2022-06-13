function formvalidate(){
    var flag;
    var Title = document.getElementById("songtitle").value;
    var Artist = document.getElementById("artist").value;
    var Date = document.getElementById("dateRelease").value;
    var Genre = document.getElementById("genre").value;

    flag = true;
    if(Title.trim() == ""){
        document.getElementById("reqSongTitle").innerHTML = "*Please enter the Song Title";
        flag = false;
    }
    if(Artist.trim() == ""){
        document.getElementById("reqArtist").innerHTML = "*Please write the name(s) of the Artist";
        flag = false;
    }
    if(Date.trim() == ""){
        document.getElementById("reqDate").innerHTML = "*Please enter a Date";
        flag = false;
    }
    if(Genre.trim() == ""){
        document.getElementById("reqGenre").innerHTML = "*Please enter the Song Genre";
        flag = false;
    }
    return flag;
}