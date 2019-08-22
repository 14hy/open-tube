const fetchCommentPage = require('youtube-comment-api')
const videoId = '-DsnqeY1bkc'

fetchCommentPage(videoId)
  .then(commentPage => {
    console.log(commentPage.comments)
    return fetchCommentPage(videoId, commentPage.nextPageToken)
  })
  .then(commentPage => {
    console.log(commentPage.comments)
  })