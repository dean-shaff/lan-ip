var util = {
    requestData: function(route, callbacks){
        $.ajax({
            type:"GET",
            url: $SCRIPT_ROOT+route,
            success: function(msg){
                var data = JSON.parse(msg.result);
                // console.log(data[0].name);
                callbacks.forEach(function(callback){
                    callback(data) ;
                })
            },
            failure: function(msg){
                console.log("Failure message from server: "+msg);
            }
        });
    }
}


App = function(){
    this.init = function(){
        $("#get-ip").on('click', this.getIpCallback(this));
    };
    this.getIpCallback = function(self){
        return function(){
            var apiKey = $("#api-key").val();
            if (apiKey != ""){
                util.requestData("/{}/get-ip".format(apiKey),[self.displayIpCallback(self)]);
            };
        };
    };
    this.displayIpCallback = function(self){
        return function(data){
            $("#display-ip").html("<h2>{}</h2>".format(data.ip));
        }
    }
}

$(document).ready(function(){
    var app = new App();
    app.init();
});
