var state = "justplayed"; //What's going on
var timer = 3000; //Time between js refresh of the game
var interval;

//Reload all game data and update page
function refresh()
{
  $.ajax({url: "getgame.cgi?game="+game, dataType: "xml", success: function(data) {
    var xml = $.xml2json(data,true);
    var gstate = xml.gamestatus[0];
    var inplay = eval(((gstate.invites-1) * gstate.pick)+1);
    var chatfocus = $("input[name='msg']").is(":focus");
    var scrollpos = $(window).scrollTop();

    //Construct game html
    var html = "<div class='row' style='flex-wrap: wrap; flex-direction: column;'>";
    html+="<div class='playarea col-xs-9'><div class='row'>";
    if(xml.gamestatus[0].blacks != 0) {
      if(xml.card != undefined) {
        for(var c = 0; c < xml.card.length; c++) {
          var card = xml.card[c];
          var ncard = xml.card[c+1];
          var pcard = xml.card[c-1];
          var cardclass = ' '+card.colour;
          if(card.state == 'played') { cardclass+=' selectedcard'; }
          html+="<div class='card row-sm-6 col-xs-4"+cardclass+"' title='"+card.card+"' card='"+card.card+"' state='"+card.state+"' colour='"+card.colour+"'>";
          html+=card.text;
          html+="</div>";
          if(ncard != undefined) {
            if( (card.state == 'inplay' && ncard.state != 'inplay') || (gstate.pick > 1 && card.user != ncard.user) ) {
              html+="</div><hr><div class='row'>";
            }
          }
        }
      }
    } else {
      html+="<h3>Game over!</h3>";
      $("#invite").show();
    }
    html+="</div></div>";
    html+="<div class='col-xs-3 pad5'>";
    html+="<h4>Players</h4>";
    html+="<ul class='list-group'>";
    if(xml.invite != undefined) {
      for(var i = 0; i < xml.invite.length; i++) {
        var invite = xml.invite[i];
        var myturn = "";
        if(invite.myturn == 'true') { myturn = " active"; }
        html+="<li class='list-group-item"+myturn+"'>";
        html+=invite.text;
        if(invite.won != 0) { html+="<span class='badge' title='"+invite.won+" rounds won'>"+invite.won+"</span>"; }
        html+="</li>";
      }
    }
    html+="</ul>";
    html+="</div>";
    html+="<div class='col-xs-3 pad5' id='chatdiv'>";
    html+="<h4>Chat</h4>";
    html+="<form action='chat.cgi' id='chatform'><div class='input-group'><input type='hidden' name='game' value='"+game+"'><input type='text' name='msg' placeholder='Chat' class='form-control' autofocus><span class='input-group-btn'><input type='submit' value='Send' class='btn btn-success'></span></div></form>";
    html+="<ul class='list-group'>";
    if(xml.msg != undefined) {
      for(var m = 0; m < xml.msg.length; m++) {
        var msg = xml.msg[m];
        html+="<li class='list-group-item msg' title='"+msg.username+"'>";
        if(msg.username != "") { html+="<span class='badge'>"+msg.username+"</span>"; }
        else { html+="<i>"; }
        html+=msg.text;
        if(msg.username == "") { html+="</i>"; }
        html+="</li>";
      }
    }
    html+="</ul></div>";
    html+="</div>";
    $("#game").html(html);
    //$("#game").css({minHeight: $("#game").height()+"px"});

    //Set chat box size and submit function
    $("input[name='msg']").width($("#chatdiv").width()-$("input[value='Send']").outerWidth()-25);
    if(chatfocus) { $("input[name='msg']").focus(); }
    $("#chatform").ajaxForm(function() { refresh(); $("input[name='msg']").val(""); });
    $(window).scrollTop(scrollpos);

    //___Decide game state___

    //If you haven't picked enough cards for this round
    if(gstate.turn != userid && gstate.myhand != eval(gstate.limit-gstate.pick)) {
      if(state != 'inhand' && state != "justplayed") { notify("It's your turn to pick a card!","images/cahw-icon.png","","yourturn"); }
      state = "inhand";
    }

    //If you have picked enough cards and you're waiting to be judged
    if(gstate.turn != userid && gstate.myhand == eval(gstate.limit-gstate.pick)) { state = "waiting"; }

    //If all of the cards have been picked, it's time for you to judge
    if(gstate.turn == userid && gstate.inplay == eval(((gstate.invites-1) * gstate.pick)+1) ) {
      if(state != 'inplay' && state != "justplayed") { notify("It's your turn to judge the winner!","images/cahw-icon.png","","yourturn"); }
      state = "inplay";
    }

    //If you're waiting to be the judge but not everyone has picked yet
    if(gstate.turn == userid && gstate.inplay != inplay ) { state = "waiting"; }

    //TESTING
    //console.log("Should be inplay: "+inplay);
    //console.log("Actually inplay: "+gstate.inplay);
    //console.log(gstate.turn+" | "+userid);
    console.log(state);

    //Apply on click event based on game state
    if(state != 'waiting') {
      $("div.card[colour='white'][state='"+state+"']").unbind("click").click(function() {
        var card = $(this);
        selectcard(card.attr("card"));
        card.addClass("selectedcard");
        $("div.card").unbind("click");
      }).addClass("clickable");
    }

  }});
}

function selectcard(card)
{
  $.ajax({url: "selectcard.cgi?card="+card+"&game="+game, success: function() {
    state = "justplayed";
    refresh();
  }});
}

//Send a notification to the browser
function notify(title,icon,text,id,url)
{
  if (!("Notification" in window)) {
    console.log(title+": "+text+"\n(Desktop notifications not available in your browser.)");
    return;
  }
  else if (Notification.permission !== "granted") {
    Notification.requestPermission();
  }
  else if (Notification.permission !== 'denied' && !$(window).is(":focus")) {
    var prevtitle = $(document).attr("title");
    $(document).attr("title",title);
    if(icon == '' || icon == undefined) { var icon = 'favicon.ico'; }

    //Create notification banner
    var notification = new Notification(title, {
      icon: icon,
      body: text,
      tag: id,
    });

    //What to do when you click the banner
    notification.onclick = function () {
      if(url != undefined && url != '') {
        window.open(url);
      }
      else {
        $(window).focus();
      }
      notification.close();
    };

    //Close notification when you focus the window that generated it
    $(window).focus(function() {
      notification.close();
      $(document).attr("title",prevtitle);
    });

  }
}

function startrefresh()
{
  clearTimeout(interval);
  interval = setInterval(function () { 
    if($("input[name='msg']").val() == "" && $("input[name='username']").val() == "") { refresh(); } 
  }, timer);
  refresh();
}

$(document).ready(function() {
  refresh();
  startrefresh();
  $("#refreshtimer").change(function() {
    timer = $(this).val();
    startrefresh();
  });
  $("#invite").hide();
  $("#inviteform").ajaxForm(function() {
    $("#invite").hide();
    refresh();
  });
  $("#invitebutton").click(function() {
   if($("#invite").is(":hidden")) { $("#invite").show(); $("#invite input[type='text']").select(); }
   else { $("#invite").hide(); }
  });
});
