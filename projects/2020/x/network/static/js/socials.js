function post_edit(tweet_id) {

    fetch ('/edit', {
        method: 'POST',
        body: JSON.stringify({
            post_content: document.querySelector('#post_content'+tweet_id).value,
            post_id: tweet_id
        })
    })
    document.querySelector('#container'+tweet_id).style.display = 'block';
    document.querySelector('#divedit'+tweet_id).style.display = 'none';
    document.querySelector('#body'+tweet_id).innerHTML=body;
 
}

function edit(tweet__id){
    body = document.querySelector('#body'+tweet__id).innerHTML;
    document.querySelector('#container'+tweet__id).style.display = 'none';
    document.querySelector('#divedit'+tweet__id).innerHTML='<p></p><div class="form-group"><textarea id="post_content'+tweet_id+'" name="post-content" cols="30" rows="3" class="form-control">' + body + '</textarea><p></p><input onclick="post_edit('+tweet__id+')" type="Submit" value="Update" class="btn btn-primary"><p></p></div>';
    event.preventDefault();
    document.querySelector('#divedit'+tweet__id).style.display = 'block';
}

function like_unlike(tweet_id) {
    //like/unlike to API

    fetch('/likes', {
        method: 'POST',
        body: JSON.stringify({
            post_id: tweet_id,
        })
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector('#icon'+tweet_id).className = 'bi '+data['icon_value']
        document.querySelector('#number_of_likes'+tweet_id).innerHTML = data['likes_count']
    })
}
