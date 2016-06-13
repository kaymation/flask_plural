$(document).ready(function(){
  page = 1
  sort = "created"
  getListing(page, sort)

  $("#pagination").on('click', '.clickable', function(){
    page = $(this).find("u").text();
    getListing(page, sort)
  });

  $("#sort").change(function() {
    sort = $(this).val()
    getListing(page, sort)
  });

  $("#list_area").on('click', '.edit', function(){
    $(".answers_space").slideUp();
    $(this).parent().find(".answers_space").slideDown();
  });

  $("#list_area").on('click', '.add_ans', function() {
    var fields = $(this).parent().parent().find('.answers');
    fields.append("<input>");
  });
});

var clickable_number = function(number){
  return "<span class='clickable'><a><u>" + number + "</u> |</a></span>"
}

var unclickable_number = function(number){
  return "<span>" + number + "| </span>"
}

var navline = function(page_num){
  pagination_numbers = $('#pagination')
  if(page_num < 7){
    for(var i = 1; i <= 10; i++){
      if(i == page_num){
        pagination_numbers.append(unclickable_number(i));
      }else{
        pagination_numbers.append(clickable_number(i));
      }
    }
  } else{
    for(var i = page_num - 5; i <= page_num + 5; i++){
      if(i == page_num){
        pagination_numbers.append(unclickable_number(i));
      }else{
        pagination_numbers.append(clickable_number(i));
      }
    }
  }
}

var getListing = function(page, sort) {
  $('#pagination').html("")
  $('#list_area').find("ul").html("")
  data = {
    page: page,
    sort: sort
  }
  var request = $.ajax({
    data: data,
    type: "GET",
    url: "/list"
  });
  request.done(function(response){
    response.forEach(function(question){
      // $("#list_area").find("ul").append(question_elem(question))
      $(question_elem(question)).appendTo('#list_area ul').hide().fadeIn('fast')
    });
    $('#pagination').html(navline(parseInt(page)));
  });
}

var question_elem = function(question){
  var open = "<li class='callout' id='" + question.id + "'>" + question.body + "<button class='button blue edit float-right'>Edit</button>";
  var hidden_part = "<div class='answers_space' style='display: none;'>";
  hidden_part += "<div class='answers'>"
  hidden_part += "<label for='" + question.answers[0].id + "'>Correct Answer:</label>";
  hidden_part += "<input id='" + question.answers[0].id + "'value='" + question.answers[0].body + "'>";
  hidden_part += "<label>Distractors</label>";
  question.answers.forEach(function(answer, i) {
    hidden_part += "<input id='" + answer.id + "' value='" + answer.body + "'>"
  });
  hidden_part += "</div>";
  hidden_part += "<div class='button-group'><button class='button add_ans'>Add</button><button class='button blue update'>Update!</button></div>";
  hidden_part += "</div>";
  return open + hidden_part + "</li>"
}
