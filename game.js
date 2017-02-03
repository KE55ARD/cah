var state = "justplayed"; //What's going on
var timer = 5000; //Time between js refresh of the game
var interval;
var lastblack = 0;
var lastmsg = "";
var xml;

function drawcard(card)
{
  var cardclass = ' '+card.colour;
  if(card.state == 'played') { cardclass+=' selectedcard'; }
  var html="<div class='gamecard"+cardclass+"' title='"+card.card+"' card='"+card.card+"' state='"+card.state+"' colour='"+card.colour+"'>";
  if(card.text != undefined) {
    html+=card.text;
  }
  html+="</div>";
  //clog(html);
  return html;
}

//Reload all game data and update page
function refresh(refreshcards)
{
  $.ajax({url: "getgame.cgi?game="+game, dataType: "xml", success: function(data) {
    xml = $.xml2json(data,true);
    var temphtml = "";
    var gstate = xml.gamestatus[0];
    var inplay = eval(((gstate.invites-1) * gstate.pick)+1);
    var chatfocus = $("input[name='msg']").is(":focus");
    var scrollpos = $(window).scrollTop();
    var blackpos = $("#blackdiv").scrollLeft();
    var whitepos = $("#whitediv").scrollLeft();
    var handpos = $("#handdiv").scrollLeft();
    $("#refreshtimer").val(gstate.refresh);

    //Create card html
    var html = "";
    if(gstate.blacks != 0) {
      //Black card
      if(xml.blackcard[0].card != undefined) {
        html+=drawcard(xml.blackcard[0].card[0]);
        if(lastblack != xml.blackcard[0].card[0].card) {
          lastblack = xml.blackcard[0].card[0].card;
          if($("#speak").is(":checked")) {
            temphtml+="<audio autoplay=''>";
            temphtml+="<source src='saycard.cgi?ID="+lastblack+"&type=ogg' type='audio/ogg'></source>";
            temphtml+="<source src='saycard.cgi?ID="+lastblack+"&type=mp3' type='audio/mpeg'></source>";
            temphtml+="Your browser does not support the audio element.</audio>";
          }
        }
      }
    } else {
      var score = 0;
      var winner = 0;
      for(var i = 0; i < xml.invite.length; i++) {
        var invite = xml.invite[i];
        if(invite.won > score) {
          score = invite.won;
          winner = i;
        }
      }
      html+="<h2>Game over!</h2><h3>"+xml.invite[winner].text+" wins!</h3>";
      $("#invite").show();
    }
    //html+="<hr>";
    $("#blackdiv").html(html).scrollLeft(blackpos);

    //White cards in play
    var mhtml = "";
    if(xml.whitecards[0].card != undefined) {
      var cardlength = xml.whitecards[0].card.length;
      for(var c = 0; c < cardlength; c++) {
        var pcard = xml.whitecards[0].card[c-1];
        var card = xml.whitecards[0].card[c];
        var ncard = xml.whitecards[0].card[c+1];
        if( gstate.pick == 1 || (c == 0 && gstate.pick > 1) || (gstate.pick > 1 && card.user != pcard.user) ) { mhtml+="<div class='cardcell'>"; }
        mhtml+=drawcard(card);
        if(c == cardlength-1 || gstate.pick == 1 || (gstate.pick > 1 && card.user != ncard.user) ) { mhtml+="</div>"; }
      }
      mhtml+="<hr>";
    }
    $("#whitediv").html(mhtml).scrollLeft(whitepos);

    //Cards in my hand
    if(xml.mycards[0].card != undefined) {
      var mhtml="<div class='cardrow' id='handdiv'>";
      //mhtml+="<div class='fadein'></div>";
      for(var m = 0; m < xml.mycards[0].card.length; m++) {
        var card = xml.mycards[0].card[m];
        mhtml+=drawcard(card);
      }
      //mhtml+="<div class='fadeout'></div>";
      mhtml+="</div><hr>";
      $("#mycards").html(mhtml).show();
      $("#handdiv").scrollLeft(handpos);
    }

    //Create player box html
    var ihtml="<ul class='list-group'>";
    if(xml.invite != undefined) {
      for(var i = 0; i < xml.invite.length; i++) {
        var invite = xml.invite[i];
        var myturn = "";
        if(invite.myturn == 'true') { myturn = " active"; }
        if(invite.user == userid) { myturn+=" list-group-item-action"; }
        ihtml+="<li class='list-group-item"+myturn+"' player='"+invite.user+"'>";
        if(invite.won != 0) { ihtml+="<span class='tag tag-default tag-pill float-xs-right' title='"+invite.won+" rounds won'>"+invite.won+"</span>"; }
        ihtml+=invite.text;
        ihtml+="</li>";
      }
    }
    ihtml+="</ul>";
    ihtml+="</div>";
    $("#invitediv").html(ihtml);
    $("li[player="+userid+"]").click(function() { leave(); }).attr("title","Click to leave this game").addClass("clickable");
    if(gstate.owner == userid) {
      $("#inviteusername").unbind("keyup").keyup(function() {
        $("#invitesubmit").val("Invite");
        var thisval = $(this).val();
        for(var i = 0; i < xml.invite.length; i++) {
          var invite = xml.invite[i];
          var name = invite.text;
          if(name.toLowerCase() == thisval.toLowerCase()) { $("#invitesubmit").val("Kick "+name); clog("NAMES MATCH"); }
        }
      });
    }

    //Create chat html
    var chtml="<br>";
    if(xml.msg != undefined) {
      for(var m = 0; m < xml.msg.length; m++) {
        var msg = xml.msg[m];
        var sent = xml.sent[m].text;
        var cardclass = "";
        if(msg.username == '') { cardclass = " bg-faded"; }
        chtml+="<div class='card"+cardclass+"'>";
        if(msg.username != '') { chtml+="<div class='card-header'><b>"+msg.username+"</b><span class='floatright'>"+sent+"</span></div>"; }
        chtml+="<div class='card-block'>"+msg.text+"</div>";
        chtml+="</div>";
      }
    }
    else { chtml+="<li class='list-group-item italic'>No messages yet</li>"; }
    chtml+="</ul>";
    $("#chatdiv").html(chtml);


    //___Decide game state___

    //If you haven't picked enough cards for this round
    if(gstate.turn != userid && gstate.myhand != eval(gstate.limit-gstate.pick)) {
      if(state != 'inhand' && state != "justplayed" && xml.invite.length > 2) { notify("It's your turn to pick a card","images/cahw-icon.png","","yourturn"); }
      state = "inhand";
    }

    //If you have picked enough cards and you're waiting to be judged
    if(gstate.turn != userid && gstate.myhand == eval(gstate.limit-gstate.pick)) { state = "whitewaiting"; }

    //If all of the cards have been picked, it's time for you to judge
    if(gstate.turn == userid && gstate.inplay == eval(((gstate.invites-1) * gstate.pick)+1) && xml.invite.length > 2 ) {
      if(state != 'inplay' && state != "justplayed") { notify("It's your turn to judge the winner","images/cahw-icon.png","","yourturn"); }
      state = "inplay";
    }

    //If you're waiting to judge but not everyone has picked yet
    if(gstate.turn == userid && gstate.inplay != inplay ) { state = "blackwaiting"; }

    //TESTING
    //clog("Should be inplay: "+inplay);
    //clog("Actually inplay: "+gstate.inplay);
    //clog(gstate.turn+" | "+userid);
    clog(state);

    //Apply on click event based on game state
    if(state != 'whitewaiting' && state != 'blackwaiting' && xml.invite.length > 2) {
      $("div.gamecard[colour='white'][state='"+state+"']").unbind("click").click(function() {
        var card = $(this);
        selectcard(card.attr("card"));
        card.addClass("selectedcard");
        $("div.gamecard").unbind("click");
      }).addClass("clickable");
    }

    //Hide my cards when it's my turn to judge (to make it more obvious it's my turn)
    if(gstate.turn == userid && xml.invite.length > 2) {
      $("#mycards").hide();
    }

    //Clicking the black card should also read it out
    $("div.gamecard[colour='black']").click(function() {
      var speak="<audio autoplay=''>";
      speak+="<source src='saycard.cgi?ID="+lastblack+"&type=ogg' type='audio/ogg'></source>";
      speak+="<source src='saycard.cgi?ID="+lastblack+"&type=mp3' type='audio/mpeg'></source>";
      speak+="Your browser does not support the audio element.</audio>";
      temp(speak);
      clog(speak);
    });

    //Some temporary invisible stuff, like audio alerts
    if(temphtml != "") {
      temp(temphtml);
    }

    //Change the title to tell you who won the last round
    var newmsg = xml.msg[0];
    if(lastmsg != "" && lastmsg != newmsg.text) {
      var ttext = "<span>";
      if(newmsg.username != "") { ttext+=newmsg.username+": "; }
      ttext+=newmsg.text+"</span>";
      $("#gametitle").html(ttext);
      setTimeout(function() { $("#gametitle").html(xml.gamestatus[0].text); }, timer);
    }
    lastmsg = xml.msg[0].text;

  }});
}

function selectcard(card)
{
  $.ajax({url: "selectcard.cgi?card="+card+"&game="+game, success: function() {
    state = "justplayed";
    refresh("card");
  }});
}

//Send a notification to the browser
function notify(title,icon,text,id,url)
{
  $("#gametitle").html("<span class='gameinfo'>"+title+"</span>");
  setTimeout(function() { $("#gametitle").html(xml.gamestatus[0].text); }, timer);
  temp("<audio autoplay=''><source src='click.ogg' type='audio/ogg'></source><source src='click.mp3' type='audio/mpeg'></source>Your browser does not support the audio element.</audio>");

  if (!("Notification" in window)) {
    clog(title+": "+text+"\n(Desktop notifications not available in your browser.)");
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

function leave()
{
  location.href="leavegame.cgi?game="+game;
}

function temp(temphtml)
{
  $("#temp").append(temphtml).css({top: $(document).height()+"px"});
}

$(document).ready(function() {
  refresh("card");
  startrefresh();
  $("#refreshtimer").change(function() {
    timer = $(this).val();
    $.ajax({url: "setrefresh.cgi?timer="+timer, success: function() {
      startrefresh();
    }});
  });
  $("#invite").hide();
  $("#inviteform").ajaxForm(function() {
    $("#invite").hide();
    $("#inviteusername").val("");
    $("#invitesubmit").val("Invite");
    refresh();
  });
  $("#invitebutton").click(function() {
   if($("#invite").is(":hidden")) { $("#invite").show(); $("#invite input[type='text']").select(); }
   else { $("#invite").hide(); }
  });

  //Set chat box submit function
  $("#chatform").ajaxForm(function() { refresh(); $("input[name='msg']").val(""); });
});
