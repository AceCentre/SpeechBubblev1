var compareList;
$(document).ready(function (){ //Wait for the page to load.
	var product_class = $('.product').attr('name');
	// hide the static compare button if js is enabled
	$('input#comparebutton').addClass("hidden");
        $('.product').bind('click keypress', function (){
                updateCompareList(this, compareList, product_class);
        });
	// initialise a cookie that lives for the length of the
	// browser session
	$.Jookie.Initialise(product_class, -1);
	compareList = $.Jookie.Get(product_class, "compareList") || [];
	for (x in compareList) {
		// check items in compareList
		$("#" + compareList[x].slug).attr('checked', true); 
                disableCheckBox(
			compareList[x].slug, 
			compareList[x].name, 
			product_class
		);
	}
});

function updateCompareList(element, compareList, product_class){
        var slug = $(element).attr('id');
        var name = $(element).val();
	var obj = new Object;
        if ($(element).is(':checked')) {
		disableCheckBox(slug, name, product_class);
		obj.slug = slug;
		obj.name = name;
		compareList.push(obj);
		$.Jookie.Set(product_class, "compareList", compareList);
        }
        else {
		enableCheckBox(slug, name);
		for(var i = compareList.length-1; i >= 0; i--){
			if(compareList[i].slug == slug){
				compareList.splice(i,1);
			}
		}
		$.Jookie.Set(product_class, "compareList", compareList);
        }
};

function disableCheckBox(slug, name, product_class){
	$('#compareList').append('<li id="'+slug+'_li"></li>');
	if ($('#'+slug).length ) {
		$('#'+slug).appendTo('#'+slug+'_li');
	}
	else {
		$('#'+slug+'_li').append('<input id="'+slug+'" type="checkbox" class="product" name="'+product_class+'" value="'+name+'" />');
	        $('#'+slug).bind('click keypress', function (){
	                updateCompareList(this, compareList, product_class);
	        });
	}
	$('#'+slug).attr('checked', true);
	$('#'+slug+'_li').append(name);
	$('#'+slug+'_td').text("Added to comparison");
};

function enableCheckBox(slug, name){
	$('#'+slug+'_td').text("Add to COMPARE list ");
	$('#'+slug).appendTo('#'+slug+'_td');
	$('#'+slug+'_li').remove();
};
