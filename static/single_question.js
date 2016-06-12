
$(document).ready(function(){
  $(document).foundation();
  var askedIds = [];
  getNextQuestion();

  $('#answers').on('click', '.answer', function(){
    $('.answer').each(function(i, answer){
      if( $(answer).attr('data-correct') == "True"){
        $(answer).addClass('success');
      } else {
        $(answer).addClass('alert');
      }
    });
    if( $(this).attr('data-correct') == "True" ){
      alert("Correct!");
    } else {
      alert("Sorry, wrong answer");
    }
    getNextQuestion();
  })

})

var answer_elem =  function(body, correct){
  return "<div class='panel callout answer' data-correct='" + correct + "'>" + body + "</div>"
}

var getNextQuestion = function(askedIds){
  $('.answer').remove();
  data = {
    asked: askedIds
  }

  var request = $.ajax({
    url: "/new_question",
    data: "data",
    type: "GET"
  });
  request.done(function(response){
    console.log(response);
    response_obj = JSON.parse(response);
    $('#question').find('h3').text(response_obj["question"]);
    var answers = response_obj["answers"]
    shuffle(answers)
    answers.forEach(function(answer, i){
      elem = answer_elem(answer["answer"], answer["correct"] );
      $('#answers').append(elem);
    });

  })
}

function shuffle(a) {
    var j, x, i;
    for (i = a.length; i; i -= 1) {
        j = Math.floor(Math.random() * i);
        x = a[i - 1];
        a[i - 1] = a[j];
        a[j] = x;
    }
}
