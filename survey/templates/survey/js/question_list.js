// When the page has loaded
$(document).ready(function () {
  // Function to Post an answer
  $('.answer').click(function (e) {
    e.preventDefault()
    let url = '{% url "survey:question-answer" %}'
    let data = {
      question_pk: $(this).data('question'),
      value: $(this).data('value')
    }

    let headers = {
      'X-CSRFToken': '{{ csrf_token }}'
    }

    $.ajax({
      type: 'POST',
      url,
      data,
      headers,
      success: function (data) {
        window.location.reload()
      },
      error: function (data) {
        if (data.status === 401) {
          alert('Debe iniciar sesión para responder.')
          window.location.href = '{% url "login" %}'
        } else {
          alert('Error al guardar la respuesta.')
        }
      }
    })
  })

  // Function to Post a like or dislike
  function likeDislike(e) {
    e.preventDefault()
    let url = '{% url "survey:question-like" %}'
    // value en numero
    let value = $(this).data('value')
    let data = {
      question_pk: $(this).data('question'),
      value: $(this).data('value')
    }

    let headers = {
      'X-CSRFToken': '{{ csrf_token }}'
    }

    $.ajax({
      type: 'POST',
      url,
      data,
      headers,
      success: function (data) {
        window.location.reload()
      },
      error: function (data) {
        if (data.status === 401) {
          alert('Debe iniciar sesión para dar like o dislike.')
          window.location.href = '{% url "login" %}'
        } else {
          alert('Error al guardar la respuesta.')
        }
      }
    })
  }

  $('.like').click(likeDislike)
  $('.dislike').click(likeDislike)
})
