document.addEventListener('DOMContentLoaded', function () {
	chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
    var newsurl = tabs[0].url;
//    alert(newsurl);
    $.ajax({
    url: "http://35.201.242.38:5000",   //後端的URL
    type: "POST",   //用POST的方式
    dataType: "text",   //response的資料格式
    cache: false,   //是否暫存
    data: newsurl, //傳送給後端的資料
    success: function(returnData){
        var data= JSON.parse(returnData);
        $("#blue").text(data[0]);
        $("#green").text(data[1]);
        $("#red").text(data[2]);
        $("#yellow").text(data[3]);
        $("#white").text(data[4]);
        
        $('#progress span').css('width',data[0]*2);
        $('#progress2 span').css('width',data[1]*2);
        $('#progress3 span').css('width',data[2]*2);
        $('#progress4 span').css('width',data[3]*2);
        $('#progress5 span').css('width',data[4]*2);
        
        console.group("Authentication phase");
//        alert("great!");
        console.log(data);
    },
    error: function(xhr, ajaxOptions, thrownError){
        console.group("Authentication phase");
        console.log(xhr.status);
        console.log(thrownError);
        alert("fucked!");
            }
        });
    });
});
