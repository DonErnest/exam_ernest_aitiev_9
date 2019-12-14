const baseUrl = 'http://localhost:8000/api/v1/';

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function getFullPath(path) {
    path = path.replace(/^\/+|\/+$/g, '');
    path = path.replace(/\/{2,}/g, '/');
    return baseUrl + path + '/';
}

function makeRequest(path, method, data=null) {
    let settings = {
        url: getFullPath(path),
        method: method,
        dataType: 'json',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
    };
    if (data) {
        settings['data'] = JSON.stringify(data);
        settings['contentType'] = 'application/json';
    }
    return $.ajax(settings);
}

function setUpCommentAdd() {
    commentAdd.on('click', function (event) {
        event.preventDefault();
        data = {
            'text': commentText.val(),
            'author': commentAuthor.val(),
            'photo': commentPhoto.val(),
        };
        makeRequest('comments/', 'post', data).done(function(data, status, response) {
        console.log('Comment added');
        commentModal.modal('hide')

    }).fail(function(response, status, message) {
        console.log('Could not add comment');
        console.log(response);
    });
    })
}

function setUpLikeAdd() {
    addLike.on('click', function(event) {
        event.preventDefault();
        data = {
            'user': commentAuthor.val(),
            'photo': image.attr('data-info')
        };
        makeRequest('likes/', 'post', data).done (function(data, status, response) {
        console.log('Like added');
        getLikesTotal();

    }).fail(function(response, status, message) {
        console.log('Could not like');
        console.log(response);
    });
    })
}




function setUpRemoveLike() {
    removeLike.on('click', function(event) {
        event.preventDefault();
        data = {
            'user': commentAuthor.val(),
            'photo': image.attr('data-info')
        };
        makeRequest(`likes/${image.attr('data-info')}`, 'delete', data).done (function(data, status, response) {
            console.log('Like removed');
            getLikesTotal();

        }).fail(function(response, status, message) {
            console.log('Could not remove like');
            console.log(response);
        });
        checkLike();
    })
}

function getLikesTotal() {
    let likesList = makeRequest('likes', 'get').done(function (data, status, response) {
        console.log('List of likes received');
        console.log(likesList);
        likesTotal.text(data.length);
    }).fail(function (response, status, message) {
        console.log('Could not get list of likes');
        console.log(response);
    });
}

// function checkLike() {
//     let likesList = makeRequest('likes', 'get').done(function (data, status, response) {
//         console.log('List of likes received');
//         console.log(data);
//         if (data) {
//             for (let i = 0; i < data.length; i++) {
//                 if (data[i].user.toString() === commentAuthor.val().toString()) {
//                     addLike.hide();
//                     removeLike.show();
//                 } else {
//                     removeLike.hide();
//                     addLike.show();
//                 }
//             }
//         } else {
//             removeLike.hide();
//             addLike.show();
//         }
//
//     }).fail(function (response, status, message) {
//         console.log('Could not get list of likes');
//         console.log(response);
//     });
// }

function setUpDeleteComment(){
    let deleteButtons = commentList.find('.delete');
    console.log(deleteButtons);
    for (let i = 0; i < deleteButtons.length; i++) {
        let button =  $(deleteButtons[i]);
        button.on('click', function(event){
            event.preventDefault();
            makeRequest(`comments/${button.attr('id')}`, 'delete').done(function(data, status, response) {
                console.log('Comment deleted');
            }).fail(function(response, status, message) {
                console.log('Could not delete comment');
                console.log(response);
            });
        })
    }
}



let commentModal, commentText, commentAuthor, commentAdd, commentList, commentPhoto, image, likesTotal, dislikesTotal, addLike, removeLike;

function setUpGlobalVars() {
    image = $('#photo');
    commentModal = $('#commentModal');
    commentAuthor = $('#commentAuthor');
    commentPhoto = $('#commentPhoto');
    commentText = $('#commentText');
    commentAdd = $('#commentAdd');
    likesTotal = $('#likesTotal');
    dislikesTotal = $('#dislikesTotal');
    addLike = $('#addLike');
    removeLike = $('#removeLike');
    commentList = $('#commentsList');
}



$(document).ready(function() {
    setUpGlobalVars();
    // checkLike();
    setUpLikeAdd();
    setUpRemoveLike();
    setUpCommentAdd();
    setUpDeleteComment();
});

