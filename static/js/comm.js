// JavaScript Document

$(function()
{
	//ie
	if ( $.browser.msie){
		 if(parseInt( $.browser.version )<=8){
			 $("body").prepend("<div class='ie6' style='display:block;'><span>å³é­</span>æ¬ç«ä¸åæ¯ææ¨çæµè§å¨ï¼360ãsogouç­æµè§å¨è¯·åæ¢å°æ¥éæ¨¡å¼ï¼æåçº§æ¨çæµè§å¨å° <a href='http://browsehappy.osfipin.com/' target='_blank' style='text-decoration:underline'>æ´é«ççæ¬</a>ï¼ä»¥è·å¾æ´å¥½çè§çææã</div>");
			 $(".ie6 span").click(function(){$(".ie6").slideUp()});
	}};



	////switch

	$(".content  ul.switch[datatarget]").each(function() {
	  $(".content  div[datasrc='"+$(this).attr("datatarget")+"']:gt(0)").hide();
    });

	var wt;
	$(".content  ul.switch[datatarget] > li").hover(function(){
						var _this=$(this),datatarget=$(this).parent("ul").attr("datatarget"),moretarget=$(this).parent("ul").attr("moretarget");
				wt=setTimeout(function(){
						$("#"+moretarget+"").attr("href",$(_this).attr("moredata"));
						$(".content ul.switch[datatarget='"+datatarget+"'] li").removeClass("current").removeClass("show");
						$(_this).addClass("current");
						$(".content div[datasrc='"+datatarget+"']").hide();
						$(".content div[datasrc='"+datatarget+"']").eq($(_this).index()).show();

					},200);
			},
			function(){
				clearTimeout(wt);
				}
			);
	////


	//menu
	var vNavWaitSlide,NavWaitSlide;
	  $('#nav > li').hover(
		  function(){
			  $(this).find('a:first').addClass("hover");
			  var current_li=$(this),targ=$(current_li).find('ul:first');
			  NavWaitSlide = setTimeout(function() {
				  if(!$(targ).is(':visible'))
				  {
						$(targ).slideDown(200);
				  }
			  },100)
		  },
		 function(){
			  clearTimeout(NavWaitSlide);
			  $(this).find('ul').hide();
			  $(this).find('a:first').removeClass("hover");
		  }
		);


	////å°å±å¹

	$("#smenu").bind("click",function(){
		if($("#header").is(".active")){
			$("#header").removeClass("active");
			$(".masklayer").hide();
			//$('body').css("overflow-y",'auto');
		}else{

			$("#header").addClass("active");
			$(".masklayer").fadeIn("fast");
			//$('body').css("overflow-y",'hidden');

		}
	});

	$(".masklayer").bind("click",function(){
			$("#header").removeClass("active");
			$(".masklayer").hide();
			$('body').css("overflow-y",'auto');
	});

	//search
	$("#search i").bind("click",function(){
			if($("#search").is(".active")){
			$("#search").removeClass("active");

		}else{
			$("#search").addClass("active");
		}
	});

	//éå±å¹

	$("#toup").bind("click",function(){$("html,body").animate({scrollTop: 0}, 500);})
	$("#share").bind("click",function(){
		$(".righttools .sharewrapper").slideToggle()
	})

	$(window).bind("scroll",function(){

		if($(window).scrollTop()>90)
		{
			if(!$("#header").is(".fixed")) $("#header").addClass("fixed");
			if(!$("#toup").is("hide")) $("#toup").fadeIn();
		}else
		{
			$("#header").removeClass("fixed");
			$("#toup").fadeOut();
		}

		$(".scrollfix").each(function(idx)
		{
			if($(window).scrollTop()<=$($(this).attr("overposition")).offset().top)
			{
				$(this).css({"top":"0"}).removeClass("start");
			}else if ($(window).scrollTop()+$(this).find(".contact").height()+$("#header").height()+15<$($(this).attr("endposition")).offset().top){
				$(this).css({"top":$(window).scrollTop()-$($(this).attr("overposition")).offset().top+$("#header").height()+15}).addClass("start");
			}

		})


	})


});

function scrollto(id)
{
	if($(id).length>0)
	{
		$("html,body").animate({scrollTop: $(id).offset().top}, 300);
	}
}

function onoff(src,id)
{
	if($(id).length>0)
	{
		$(id).toggle();
		$(src).toggleClass("on");
	}
}


function share_out(options)
{
	var url = options.url || window.location.href, pic = '';

	if (options.title)
	{
		var title = options.title ;
	}
	else
	{
		var title = $('title').text();
	}

	shareURL = 'http://www.jiathis.com/send/?webid=' + options.webid + '&url=' + url + '&title=' + title +'';

	if (options.content)
	{
		if ($(options.content).find('img').length)
		{
			shareURL = shareURL + '&pic=' + $(options.content).find('img').eq(0).attr('src');
		}
	}

	window.open(shareURL);
}


