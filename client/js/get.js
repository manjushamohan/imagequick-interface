function get()
{
$.ajax({
            url:'https://itunes.apple.com/search?term==LUKE BRYAN',
            type:'GET',
            crossDomain:true,
            beforeSend: function(x) {
                if(x && x.overrideMimeType) {
                    x.overrideMimeType("application/j-son;charset=UTF-8");
                }
            },
            success:function(data){
                console.log("Success");
                console.log(data)
        }
        });
}