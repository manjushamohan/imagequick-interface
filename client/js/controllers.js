'use strict';
var SERVER_DOMAIN = 'http://localhost:5000'
//Add no ending slashes.
/* Controllers */

function UserCtrl($scope,$http) {
  $scope.name = 'ImageQuick';

  $http.get(SERVER_DOMAIN+'/get/slogans/').then(function(response){
     $scope.slogans = response.data.slogans
    })
  $http.get(SERVER_DOMAIN+'/get/stations/').then(function(response){
     $scope.stations = response.data.stations
    })
  $http.get(SERVER_DOMAIN+'/get/frequency/').then(function(response){
     $scope.frequencies = response.data.frequencies
    })
  $http.get(SERVER_DOMAIN+'/get/groups/').then(function(response){
     $scope.groups = response.data.groups
    })

  $scope.add = function(user){
    console.log(user)
    $http.post( SERVER_DOMAIN + "/backend/create_user",user).then(function(data){
       $.notify("Added",'success')
       $scope.user={};
       
      });

  }
}
function GroupCtrl($scope,$http,TemplateIds,VoiceIds) {
  $scope.name = 'ImageQuick';
  $scope.hooktemps=[];
  $scope.temps=[];
  $http.get(SERVER_DOMAIN+'/get/voices/').then(function(response){
     $scope.voices = response.data.voices
    })
  $http.get(SERVER_DOMAIN+'/get/templates/').then(function(response){
    $scope.temps = response.data.templates
    })
  $http.get(SERVER_DOMAIN+'/get/hooktemplates/').then(function(response){
    $scope.hooktemps = response.data.hooktemplates
    })
  $http.get(SERVER_DOMAIN+'/get/formats/').then(function(response){
     $scope.formats = response.data.formats
    })
  
  $scope.select_voice=function(voice,value){
     if(value==true){
          
          
         VoiceIds.push(voice.name);
         console.log(VoiceIds)
      
     }
     else{
          
          var index=VoiceIds.indexOf(voice.name)
           VoiceIds.splice(index,1);  

          
          console.log(VoiceIds)
          
     }
    }

    $scope.select_template=function(template,value1){
      console.log(template)
     if(value1==true){
          
          
         TemplateIds.push(template._id);
         console.log(TemplateIds)
      
     }
     else{
          
          var index=TemplateIds.indexOf(template._id)
           TemplateIds.splice(index,1);  

          
          console.log(TemplateIds)
          
     }
    }
    $scope.$watch('group.format', function(newVal, oldVal) {
      $scope.hooktemplates=[];
      $scope.templates=[];
      console.log(newVal, oldVal);
      for(var i=0;i<$scope.hooktemps.length;i++){
          for(var j=0;j<$scope.hooktemps[i].formatids.length;j++){
            if(newVal.uid==$scope.hooktemps[i].formatids[j]){
              $scope.hooktemplates.push($scope.hooktemps[i])
            }
          }
      }
      for(var i=0;i<$scope.temps.length;i++){
        for(var j=0;j<$scope.temps[i].formatids.length;j++){
          if(newVal.uid==$scope.temps[i].formatids[j]){
            $scope.templates.push($scope.temps[i])
          }
        }
      }
    });
    $scope.add = function(group){
      
      group.voices=VoiceIds;
      group.templates=TemplateIds;
     group['format']=group.format['uid'];

      console.log(group)
      $http.post( SERVER_DOMAIN + "/add/group",group).then(function(data){
        if(data.data.status == 'success'){
          $.notify("Added "+data.data.data.name,'success')
          $scope.group = {}
          

        }
        else{
          $.notify("Error adding "+group.name,'error')
          TemplateIds=[];
        }
      });

     
    }



    VoiceIds=[];
    TemplateIds=[];

}

function HomeCtrl($scope) {
  $scope.name = 'ImageQuick';
}

function HookTCtrl($scope) {
  $scope.name = 'ImageQuick';
}

function HookLCtrl($scope) {
  $scope.name = 'ImageQuick';
}


function BillmCtrl($scope) {
  $scope.name = 'BillmCtrl';
}


function CouponsCtrl($scope,$http) {
    $scope.name = 'Coupons';

    $scope.add = function(coupon){
      $http.post( SERVER_DOMAIN + "/add/coupon",coupon).then(function(data){
        if(data.data.status == 'success'){
          $.notify("Added "+data.data.data.code,'success')
          $scope.coupon = {}
        }
        else{
          $.notify("Error adding "+coupon.code,'error')
        }
      });
    }

}


function DeliveryCtrl($scope,$http) {
  $scope.name = 'Delivery';
    $scope.add = function(style){
      console.log(style)
      $http.post( SERVER_DOMAIN + "/add/style",style).then(function(data){
        if(data.data.status == 'success'){
          $.notify("Added "+data.data.data.name,'success')
          $scope.style = {}
        }
        else{
          $.notify("Error adding "+style.name,'error')
        }
      });
    }

}



function FormatCtrl($scope,$http,VoiceIds) {
    $scope.name = 'Format';
   
    $http.get(SERVER_DOMAIN+'/get/voices/').then(function(response){
     $scope.voices = response.data.voices
    })

    $scope.select_voice=function(voice,value){
     if(value==true){
          
          
         VoiceIds.push(voice.uid);
         console.log(VoiceIds)
      
     }
     else{
          
          var index=VoiceIds.indexOf(voice.uid)
           VoiceIds.splice(index,1);  

          
          console.log(VoiceIds)
          
     }
    }

    $scope.add = function(format){
      
      format.voiceIds=VoiceIds;
      console.log(format)
      $http.post( SERVER_DOMAIN + "/add/format",format).then(function(data){
        if(data.data.status == 'success'){
          $.notify("Added "+data.data.data.name,'success')
          $scope.format = {}
          

        }
        else{
          $.notify("Error adding "+format.name,'error')
        }
      });

     
    }
    VoiceIds=[];

}


function FrequencyCtrl($scope,$http) {
    $scope.name = 'Frequency';


    $scope.add = function(frequency){
     
      $http.post( SERVER_DOMAIN + "/add/frequency",frequency).then(function(data){
        if(data.data.status == 'success'){
          $.notify("Added "+data.data.data.frequency,'success')
          $scope.frequency = {}
        }
        else{
          $.notify("Error adding "+frequency.frequency,'error')
        }
      });
    }
}


function HookCtrl($scope,$http) {
    $scope.name = 'Hook';

    $http.get(SERVER_DOMAIN+'/get/formats/').then(function(response){
      console.log(response.data.formats)
     $scope.formats = response.data.formats
    })
    $scope.add = function(hook){
      
      hook['format']=hook.format['name'];
      console.log(hook)
      $http.post( SERVER_DOMAIN + "/add/hook",hook).then(function(data){
        if(data.data.status == 'success'){
          $.notify("Added "+data.data.data.hook,'success')
          $scope.hook = {}
        }
        else{
          $.notify("Error adding "+hook.hook,'error')
        }
      });
    }
    
}


function HooktempCtrl($scope,$http,FormatIds,PosVoiceIds,FreVoiceIds,StatVoiceIds,PosStyleIds,FreStyleIds,StatStyleIds) {
    $scope.name = 'Hooktemp';
    $http.get(SERVER_DOMAIN+'/get/formats/').then(function(response){
     $scope.formats = response.data.formats
    })
  $http.get(SERVER_DOMAIN+'/get/voices/').then(function(response){
     $scope.voices = response.data.voices
    })
  $http.get(SERVER_DOMAIN+'/get/styles/').then(function(response){
     $scope.styles = response.data.styles
    })


  $scope.select_format=function(format,value){
     if(value==true){
          
          FormatIds.push(format.uid);
          console.log(FormatIds)
     }
     else{
         
          var index=FormatIds.indexOf(format.uid)
          FormatIds.splice(index,1);  
          console.log(FormatIds)
     }
    }

    $scope.select_posvoice=function(voice,value1){
     if(value1==true){
          
          PosVoiceIds.push(voice.uid);
          console.log(PosVoiceIds)
     }
     else{
         
          var index=PosVoiceIds.indexOf(voice.uid)
          PosVoiceIds.splice(index,1);  
          console.log(PosVoiceIds)
     }
    }

    $scope.select_frevoice=function(voice,value5){
     if(value5==true){
          
          FreVoiceIds.push(voice.uid);
          console.log(FreVoiceIds)
     }
     else{
         
          var index=FreVoiceIds.indexOf(voice.uid)
          FreVoiceIds.splice(index,1);  
          console.log(FreVoiceIds)
     }
    }
    $scope.select_statvoice=function(voice,value3){
     if(value3==true){
          
          StatVoiceIds.push(voice.uid);
          console.log(StatVoiceIds)
     }
     else{
         
          var index=StatVoiceIds.indexOf(voice.uid)
          StatVoiceIds.splice(index,1);  
          console.log(StatVoiceIds)
     }
    }
    $scope.select_posstyle=function(style,value2){
     if(value2==true){
          
          PosStyleIds.push(style.uid);
          console.log(PosStyleIds)
     }
     else{
         
          var index=PosStyleIds.indexOf(style.uid)
          PosStyleIds.splice(index,1);  
          console.log(PosStyleIds)
     }
    }
    $scope.select_frestyle=function(style,value6){
     if(value6==true){
          
          FreStyleIds.push(style.uid);
          console.log(FreStyleIds)
     }
     else{
         
          var index=FreStyleIds.indexOf(style.uid)
          FreStyleIds.splice(index,1);  
          console.log(FreStyleIds)
     }
    }

    $scope.select_statstyle=function(style,value4){
     if(value4==true){
          
          StatStyleIds.push(style.uid);
          console.log(StatStyleIds)
     }
     else{
         
          var index=StatStyleIds.indexOf(style.uid)
          StatStyleIds.splice(index,1);  
          console.log(StatStyleIds)
     }
    }
    $scope.add = function(hooktemp){


      hooktemp.formatids=FormatIds;
      hooktemp.posVoiceids=PosVoiceIds;
      hooktemp.posStyleids=PosStyleIds;
      hooktemp.freVoiceids=FreVoiceIds;
      hooktemp.freStyleids=FreStyleIds;
      hooktemp.statVoiceids=StatVoiceIds;
      hooktemp.statStyleids=StatStyleIds;
      console.log(hooktemp)
      $http.post( SERVER_DOMAIN + "/add/hooktemplate",hooktemp).then(function(data){
        if(data.data.status == 'success'){
          $.notify("Added "+data.data.data.name,'success')
          $scope.hooktemp = {}
        }
        else{
          $.notify("Error adding "+hooktemp.name,'error')
        }
      });

       
    }

      FormatIds=[];
      PosVoiceIds=[];
      PosStyleIds=[];
      FreVoiceIds=[];
      FreStyleIds=[];
      StatVoiceIds=[];
      StatStyleIds=[];
      $scope.value=false;

}


function PositionCtrl($scope,$http,FormatIds) {
  $scope.name = 'Position';
  $http.get(SERVER_DOMAIN+'/get/formats/').then(function(response){
     $scope.formats = response.data.formats
    })

  $scope.select_format=function(format,value){
     if(value==true){
          
          FormatIds.push(format.uid);
          console.log(FormatIds)
     }
     else{
         
          var index=FormatIds.indexOf(format.uid)
          FormatIds.splice(index,1);  
          console.log(FormatIds)
     }
    }

  $scope.add = function(position){
      
      position.formatIds=FormatIds;
      console.log(position)
      $http.post( SERVER_DOMAIN + "/add/position",position).then(function(data){
        if(data.data.status == 'success'){
          $.notify("Added "+data.data.data.name,'success')
          $scope.position = {}
        }
        else{
          $.notify("Error adding "+position.name,'error')
        }
      });
      FormatIds=[];

    }

}


function SfpCtrl($scope) {
  $scope.name = 'Sfp';
}



function SloganCtrl($scope,$http) {
    $scope.name = 'Slogan';
    $scope.add = function(slogan){
      $http.post( SERVER_DOMAIN + "/add/slogan_length",slogan).then(function(data){
        if(data.data.status == 'success'){
          $.notify("Added "+data.data.data.slogan,'success')
          $scope.slogan = {}
        }
        else{
          $.notify("Error adding "+slogan.slogan,'error')
        }
      });
    }


}


function StationCtrl($scope,$http,FormatIds) {
    $scope.name = 'Station';
    $http.get(SERVER_DOMAIN+'/get/formats/').then(function(response){
     $scope.formats = response.data.formats
    })

    $scope.select_format=function(format,value){
     if(value==true){
          
          FormatIds.push(format.uid);
          console.log(FormatIds)
     }
     else{
         
          var index=FormatIds.indexOf(format.uid)
          FormatIds.splice(index,1);  
          console.log(FormatIds)
     }
    }




    $scope.add = function(station){
      station.formatIds=FormatIds;
      $http.post( SERVER_DOMAIN + "/add/station",station).then(function(data){
        if(data.data.status == 'success'){
          $.notify("Added "+data.data.data.name,'success')
          $scope.station = {}
        }
        else{
          $.notify("Error adding "+station.name,'error')
        }
      });

       
    }
    FormatIds=[];

}


function TemplateCtrl($scope,$http,FormatIds,PosVoiceIds,FreVoiceIds,StatVoiceIds,PosStyleIds,FreStyleIds,StatStyleIds) {
  $scope.name = 'Template';
  $http.get(SERVER_DOMAIN+'/get/formats/').then(function(response){
     $scope.formats = response.data.formats
    })
  $http.get(SERVER_DOMAIN+'/get/voices/').then(function(response){
     $scope.voices = response.data.voices
    })
  $http.get(SERVER_DOMAIN+'/get/styles/').then(function(response){
     $scope.styles = response.data.styles
    })

  $scope.select_format=function(format,value){
     if(value==true){
          
          FormatIds.push(format.uid);
          console.log(FormatIds)
     }
     else{
         
          var index=FormatIds.indexOf(format.uid)
          FormatIds.splice(index,1);  
          console.log(FormatIds)
     }
    }

    $scope.select_posvoice=function(voice,value1){
     if(value1==true){
          
          PosVoiceIds.push(voice.uid);
          console.log(PosVoiceIds)
     }
     else{
         
          var index=PosVoiceIds.indexOf(voice.uid)
          PosVoiceIds.splice(index,1);  
          console.log(PosVoiceIds)
     }
    }

    $scope.select_frevoice=function(voice,value5){
     if(value5==true){
          
          FreVoiceIds.push(voice.uid);
          console.log(FreVoiceIds)
     }
     else{
         
          var index=FreVoiceIds.indexOf(voice.uid)
          FreVoiceIds.splice(index,1);  
          console.log(FreVoiceIds)
     }
    }
    $scope.select_statvoice=function(voice,value3){
     if(value3==true){
          
          StatVoiceIds.push(voice.uid);
          console.log(StatVoiceIds)
     }
     else{
         
          var index=StatVoiceIds.indexOf(voice.uid)
          StatVoiceIds.splice(index,1);  
          console.log(StatVoiceIds)
     }
    }
    $scope.select_posstyle=function(style,value2){
     if(value2==true){
          
          PosStyleIds.push(style.uid);
          console.log(PosStyleIds)
     }
     else{
         
          var index=PosStyleIds.indexOf(style.uid)
          PosStyleIds.splice(index,1);  
          console.log(PosStyleIds)
     }
    }
    $scope.select_frestyle=function(style,value6){
     if(value6==true){
          
          FreStyleIds.push(style.uid);
          console.log(FreStyleIds)
     }
     else{
         
          var index=FreStyleIds.indexOf(style.uid)
          FreStyleIds.splice(index,1);  
          console.log(FreStyleIds)
     }
    }

    $scope.select_statstyle=function(style,value4){
     if(value4==true){
          
          StatStyleIds.push(style.uid);
          console.log(StatStyleIds)
     }
     else{
         
          var index=StatStyleIds.indexOf(style.uid)
          StatStyleIds.splice(index,1);  
          console.log(StatStyleIds)
     }
    }
    $scope.add = function(template){


      template.formatids=FormatIds;
      template.posVoiceids=PosVoiceIds;
      template.posStyleids=PosStyleIds;
      template.freVoiceids=FreVoiceIds;
      template.freStyleids=FreStyleIds;
      template.statVoiceids=StatVoiceIds;
      template.statStyleids=StatStyleIds;
      console.log(template)
      $http.post( SERVER_DOMAIN + "/add/template",template).then(function(data){
        if(data.data.status == 'success'){
          $.notify("Added "+data.data.data.name,'success')
          $scope.template = {}
        }
        else{
          $.notify("Error adding "+template.name,'error')
        }
      });

       
    }
      FormatIds=[];
      PosVoiceIds=[];
      PosStyleIds=[];
      FreVoiceIds=[];
      FreStyleIds=[];
      StatVoiceIds=[];
      StatStyleIds=[];
      $scope.value=false;



}


function VoiceCtrl($scope,$http) {
  $scope.name = 'Voice';
  $scope.add = function(voice){
    $http.post( SERVER_DOMAIN + "/add/voice",voice).then(function(data){
      if(data.data.status == 'success'){
        $.notify("Added "+data.data.data.name,'success')
        $scope.voice = {}
      }
      else{
        $.notify("Error adding "+voice.name,'error')
      }
    });
  }
}




function Analt_HomeCtrl($scope,$http){
  $http.get(SERVER_DOMAIN+'/analytics/voice/').then(function(response){
    $scope.chart = response.data.chart
    var chart = response.data.chart
    var ctx = $("#myChart").get(0).getContext("2d");
    //This will get the first returned node in the jQuery collection.
    var data = {
      labels : chart.labels,
      datasets : [
      {
        fillColor : "rgba(220,220,220,0.5)",
        strokeColor : "#d30000",
        pointColor : "rgba(220,220,220,1)",
        pointStrokeColor : "#d30000",
        data : chart.play
      },
      ]
    }
    new Chart(ctx).Bar(data);

    //Buy Ratio Chart
    var ctx2 = $("#buyChart").get(0).getContext("2d");
    //This will get the first returned node in the jQuery collection.
    var data = {
      labels : chart.labels,
      datasets : [
      {
        fillColor : "rgba(220,220,220,0.5)",
        strokeColor : "#689512",
        pointColor : "rgba(220,220,220,1)",
        pointStrokeColor : "#689512",
        data : chart.buy
      },
      ]
    }
    new Chart(ctx2).Bar(data);
})

  //Get Month Info
  $http.get(SERVER_DOMAIN+'/analytics/voice/monthly/2/').then(function(response){
    var charts = response.data.charts
    var ctxPlayMonth = $("#playChartMonth").get(0).getContext("2d");
    //This will get the first returned node in the jQuery collection.
    $scope.months = [charts[0].month,charts[1].month]
    var data = {
      labels : charts[1].labels,
      datasets : [
      {
        fillColor : "rgba(220,220,220,0.5)",
        strokeColor : "#d30000",
        pointColor : "rgba(220,220,220,1)",
        pointStrokeColor : "#d30000",
        data : charts[0].play
      },
      {
        fillColor : "rgba(220,220,220,0.5)",
        strokeColor : "rgba(220,220,220,0.5)",
        pointColor : "rgba(220,220,220,1)",
        pointStrokeColor : "#000000",
        data : charts[1].play
      },
      ]
    }
    new Chart(ctxPlayMonth).Bar(data);

    //Buy
    var ctxBuyMonth = $("#buyChartMonth").get(0).getContext("2d");
    //This will get the first returned node in the jQuery collection.
    $scope.months = [charts[0].month,charts[1].month]
    var data = {
      labels : charts[1].labels,
      datasets : [
      {
        fillColor : "rgba(220,220,220,0.5)",
        strokeColor : "#689512",
        pointColor : "rgba(220,220,220,1)",
        pointStrokeColor : "#689512",
        data : charts[0].buy
      },
      {
        fillColor : "rgba(220,220,220,0.5)",
        strokeColor : "rgba(220,220,220,0.5)",
        pointColor : "rgba(220,220,220,1)",
        pointStrokeColor : "#000000",
        data : charts[1].buy
      },
      ]
    }
    new Chart(ctxBuyMonth).Bar(data);
  })
}

function TemplateImagingViewCtrl($http,$scope){
  $http.get(SERVER_DOMAIN+'/view/templates/imaging').then(function(response){
    $scope.templates = response.data.templates;

  })

  $scope.edit = function(template){
    $scope.textarea = template;
    $('#json').foundation('reveal', 'open');
    var a = angular.copy(template)
    var session = ace.EditSession(a)
    var editor = ace.edit("editor",session);
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/javascript");
    
  }
}



function UserviewCtrl($scope,$http) {
  $scope.name = 'ImageQuick';
  $http.get(SERVER_DOMAIN+'/get/slogans/').then(function(response){
     $scope.slogans = response.data.slogans
    })
  $http.get(SERVER_DOMAIN+'/get/stations/').then(function(response){
     $scope.stations = response.data.stations
    })
  $http.get(SERVER_DOMAIN+'/get/frequency/').then(function(response){
     $scope.frequencies = response.data.frequencies
    })
  $http.get(SERVER_DOMAIN+'/get/groups/').then(function(response){
     $scope.groups = response.data.groups
    })
  $http.get(SERVER_DOMAIN+'/all/users/').then(function(response){
     $scope.users = response.data.users;
       })
  $scope.edit=function(id){
   $('#edituser').foundation('reveal', 'open'); 
   $http.get(SERVER_DOMAIN+'/gets/user/'+id).then(function(response){
     $scope.edituser=response.data.user;
     })
    $scope.save=function(user){
      console.log(user)
       $http.post( SERVER_DOMAIN + "/edit/user",user).then(function(data){
      if(data.data.status == 'success'){
        $.notify("Edited "+data.data.data.username,'success')
        $scope.edituser = {}
        $http.get(SERVER_DOMAIN+'/all/users/').then(function(response){
        $scope.users = response.data.users
    })
      }
      else{
        $.notify("Error adding "+user.username,'error')
      }
    });
    $('#edituser').foundation('reveal', 'close');

    
    }
  }
  $scope.delete=function(id){
    var d=window.confirm('Are you sure want to delete ');
    if (d){
      $http.post( SERVER_DOMAIN + "/delete/user",id).then(function(response){
        $http.get(SERVER_DOMAIN+'/all/users/').then(function(response){
        $scope.users = response.data.users;
       })
    })
    }
  }

}


function GroupviewCtrl($scope,$http,VoiceIds,TemplateIds) {
  $scope.temps=[];
  $scope.hooktemps=[];
  $http.get(SERVER_DOMAIN+'/all/groups/').then(function(response){
     $scope.groups = response.data.groups;
       })
  $http.get(SERVER_DOMAIN+'/get/voices/').then(function(response){
     $scope.voices = response.data.voices
    })
  $http.get(SERVER_DOMAIN+'/get/templates/').then(function(response){
     $scope.temps = response.data.templates
    })
  $http.get(SERVER_DOMAIN+'/get/hooktemplates/').then(function(response){
     $scope.hooktemps = response.data.hooktemplates
    })
  $http.get(SERVER_DOMAIN+'/get/formats/').then(function(response){
     $scope.formats = response.data.formats
    })
  $scope.$watch('editgroup.format', function(newVal, oldVal) {
      $scope.hooktemplates=[];
      $scope.templates=[];
      console.log(newVal, oldVal);
      for(var i=0;i<$scope.hooktemps.length;i++){
          for(var j=0;j<$scope.hooktemps[i].formatids.length;j++){
            if(newVal==$scope.hooktemps[i].formatids[j]||newVal.uid==$scope.hooktemps[i].formatids[j]){
              $scope.hooktemplates.push($scope.hooktemps[i])
            }
          }
      }
      for(var i=0;i<$scope.temps.length;i++){
        for(var j=0;j<$scope.temps[i].formatids.length;j++){
          if(newVal==$scope.temps[i].formatids[j]||newVal.uid==$scope.temps[i].formatids[j]){
            $scope.templates.push($scope.temps[i])
          }
        }
      }
    });
  $scope.select_voice=function(voice,value){
     if(value==true){
          
          
         VoiceIds.push(voice.name);
         console.log(VoiceIds)
      
     }
     else{
          
          var index=VoiceIds.indexOf(voice.name)
           VoiceIds.splice(index,1);  

          
          console.log(VoiceIds)
          
     }
    }
    $scope.select_template=function(template,value1){
     if(value1==true){
          
          
         TemplateIds.push(template._id);
         console.log(TemplateIds)
      
     }
     else{
          
          var index=TemplateIds.indexOf(template._id)
           TemplateIds.splice(index,1);  

          
          console.log(TemplateIds)
          
     }
    }

  $scope.edit=function(id){
    var fid;
    $('#editgroup').foundation('reveal', 'open');
    $http.get(SERVER_DOMAIN+'/gets/group/'+id).then(function(response){
     $scope.editgroup=response.data.group;
     VoiceIds=$scope.editgroup.voices;
     fid=$scope.editgroup.format;
     TemplateIds=$scope.editgroup.templates;
     })

    $scope.save=function(group){
      console.log(group)
      console.log(fid)
      group.voices=VoiceIds;
      group.templates=TemplateIds;
      if(group['format']!=fid){
        group['format']=group.format['uid'];
      }
      console.log(group)
      $http.post( SERVER_DOMAIN + "/edit/group",group).then(function(data){
      if(data.data.status == 'success'){
        $.notify("Edited "+data.data.data.name,'success')
        $http.get(SERVER_DOMAIN+'/all/groups/').then(function(response){
        $scope.groups = response.data.groups;
        })
      }
      else{
        $.notify("Error adding "+group.name,'error')
      }
    });
    
    $('#editgroup').foundation('reveal', 'close');

    }

  }

  $scope.delete=function(id){
    var d=window.confirm('Are you sure want to delete ');
    if (d){
      $http.post( SERVER_DOMAIN + "/delete/group",id).then(function(response){
        $http.get(SERVER_DOMAIN+'/all/groups/').then(function(response){
     $scope.groups = response.data.groups;
       })
    })
    }
  }

}



function VoiceviewCtrl($scope,$http) {
  $http.get(SERVER_DOMAIN+'/all/voices/').then(function(response){
     $scope.voices = response.data.voices
    })

  $scope.edit=function(id){
    $('#editvoice').foundation('reveal', 'open');
    $http.get(SERVER_DOMAIN+'/gets/voice/'+id).then(function(response){
     $scope.editvoice=response.data.voice
    })

    $scope.save=function(voice){
      console.log(voice)
    $http.post( SERVER_DOMAIN + "/edit/voice",voice).then(function(data){
      if(data.data.status == 'success'){
        $.notify("Edited "+data.data.data.name,'success')
        $scope.editvoice = {}
        $http.get(SERVER_DOMAIN+'/all/voices/').then(function(response){
        $scope.voices = response.data.voices
    })
      }
      else{
        $.notify("Error adding "+voice.name,'error')
      }
    });
    $('#editvoice').foundation('reveal', 'close');

    }

  }

  $scope.delete=function(id){
    var d=window.confirm('Are you sure want to delete ');
    if (d){
      $http.post( SERVER_DOMAIN + "/delete/voice",id).then(function(data){
        $http.get(SERVER_DOMAIN+'/all/voices/').then(function(response){
        $scope.voices = response.data.voices
    })
            
       })

    }
  }

  

}



function CouponviewCtrl($scope,$http) {
  $http.get(SERVER_DOMAIN+'/all/coupons/').then(function(response){
     $scope.coupons = response.data.coupons
    })

  $scope.edit=function(id){
    console.log(id)
    $('#editcoupon').foundation('reveal', 'open');
    $http.get(SERVER_DOMAIN+'/gets/coupon/'+id).then(function(response){
    $scope.editcoupon=response.data.coupon
    })
    }
  $scope.save=function(coupon){
      console.log(coupon)
      $http.post( SERVER_DOMAIN + "/edit/coupon",coupon).then(function(data){
      if(data.data.status == 'success'){
        $.notify("Edited "+data.data.data.code,'success')
        $scope.editcoupon = {}
        $http.get(SERVER_DOMAIN+'/all/coupons/').then(function(response){
        $scope.coupons = response.data.coupons
      })

      }
      else{
        $.notify("Error adding "+coupon.code,'error')
      }
    });
    $('#editcoupon').foundation('reveal', 'close');

    }

  $scope.delete=function(id){
    var d=window.confirm('Are you sure want to delete ');
    if (d){
      $http.post( SERVER_DOMAIN + "/delete/coupon",id).then(function(response){
        $http.get(SERVER_DOMAIN+'/all/coupons/').then(function(response){
     $scope.coupons = response.data.coupons
    })

       
      })
    }
  }

  

}



function DeliveryviewCtrl($scope,$http) {
  $http.get(SERVER_DOMAIN+'/all/styles/').then(function(response){
     $scope.styles = response.data.styles
    })

  $scope.edit=function(id){
    console.log(id)
    $('#editstyle').foundation('reveal', 'open');
    $http.get(SERVER_DOMAIN+'/gets/style/'+id).then(function(response){
     $scope.editstyle=response.data.style
    })
    }
    
    $scope.save=function(style){
      console.log(style)
      $http.post( SERVER_DOMAIN + "/edit/style",style).then(function(data){
      if(data.data.status == 'success'){
        $.notify("Edited "+data.data.data.name,'success')
        $scope.editstyle = {}
        $http.get(SERVER_DOMAIN+'/all/styles/').then(function(response){
        $scope.styles = response.data.styles
      })

      }
      else{
        $.notify("Error adding "+style.name,'error')
      }
    });
    

    $('#editstyle').foundation('reveal', 'close');

    }

  
    $scope.delete=function(id){
    var d=window.confirm('Are you sure want to delete ');
    if (d){
      $http.post( SERVER_DOMAIN + "/delete/style",id).then(function(response){
        $http.get(SERVER_DOMAIN+'/all/styles/').then(function(response){
     $scope.styles = response.data.styles
    })

       
      })
    }
  }
  

}


function SloganviewCtrl($scope,$http) {
  $http.get(SERVER_DOMAIN+'/all/slogans/').then(function(response){
     $scope.slogans = response.data.slogans
    })

  $scope.edit=function(id){
    console.log(id)
    $('#editslogan').foundation('reveal', 'open');
    $http.get(SERVER_DOMAIN+'/gets/slogan/'+id).then(function(response){
     $scope.editslogan=response.data.slogan
    })

    $scope.save=function(slogan){
      console.log(slogan)
      $http.post( SERVER_DOMAIN + "/edit/slogan_length",slogan).then(function(data){
      if(data.data.status == 'success'){
        $.notify("Edited "+data.data.data.slogan,'success')
        $scope.editslogan = {}
        $http.get(SERVER_DOMAIN+'/all/slogans/').then(function(response){
        $scope.slogans = response.data.slogans
      })

      }
      else{
        $.notify("Error adding "+slogan.slogan,'error')
      }
    });
    
    $('#editslogan').foundation('reveal', 'close');

    }

  }
  $scope.delete=function(id){
    var d=window.confirm('Are you sure want to delete ');
    if (d){
         $http.post( SERVER_DOMAIN + "/delete/slogan_length",id).then(function(response){
        $http.get(SERVER_DOMAIN+'/all/slogans/').then(function(response){
        $scope.slogans = response.data.slogans
    })

       
      })
    }
  }
  

}


function FormatviewCtrl($scope,$http,VoiceIds) {
  $http.get(SERVER_DOMAIN+'/all/formats/').then(function(response){
     $scope.formats = response.data.formats;
       })
  $http.get(SERVER_DOMAIN+'/get/voices/').then(function(response){
     $scope.voices = response.data.voices
    })
  
  $scope.select_voice=function(voice,value){
     if(value==true){
          
          
         VoiceIds.push(voice.uid);
         console.log(VoiceIds)
      
     }
     else{
          
          var index=VoiceIds.indexOf(voice.uid)
           VoiceIds.splice(index,1);  

          
          console.log(VoiceIds)
          
     }
    }

  $scope.edit=function(id){
    console.log(id)
    $('#editformat').foundation('reveal', 'open');
    $http.get(SERVER_DOMAIN+'/gets/format/'+id).then(function(response){
     $scope.editformat=response.data.format;
     VoiceIds=$scope.editformat.voiceIds;
     console.log(VoiceIds)
    })

    $scope.save=function(format){
      format.voiceIds=VoiceIds;
      console.log(format)
      $http.post( SERVER_DOMAIN + "/edit/format",format).then(function(data){
      if(data.data.status == 'success'){
        $.notify("Edited "+data.data.data.name,'success')
        $scope.editformat = {}
        $http.get(SERVER_DOMAIN+'/all/formats/').then(function(response){
        $scope.formats = response.data.formats;
      

     
    })
        
      }
      else{
        $.notify("Error adding "+format.name,'error')
      }
    });
    
    $('#editformat').foundation('reveal', 'close');

    }

  }

  $scope.delete=function(id){
    var d=window.confirm('Are you sure want to delete ');
    if (d){
      $http.post( SERVER_DOMAIN + "/delete/format",id).then(function(response){
        $http.get(SERVER_DOMAIN+'/all/formats/').then(function(response){
     $scope.formats = response.data.formats;
       })
    })
    }
  }

}




function FrequencyviewCtrl($scope,$http) {
  $http.get(SERVER_DOMAIN+'/all/frequencies/').then(function(response){
     $scope.frequencies = response.data.frequencies
    })

  $scope.edit=function(id){
    console.log(id)
    $('#editfrequency').foundation('reveal', 'open');
    $http.get(SERVER_DOMAIN+'/gets/frequency/'+id).then(function(response){
     $scope.editfrequency=response.data.frequency
    })

    $scope.save=function(frequency){
      console.log(frequency)
      $http.post( SERVER_DOMAIN + "/edit/frequency",frequency).then(function(data){
      if(data.data.status == 'success'){
        $.notify("Edited "+data.data.data.frequency,'success')
        $scope.editfrequency = {}
        $http.get(SERVER_DOMAIN+'/all/frequencies/').then(function(response){
        $scope.frequencies = response.data.frequencies
    
      })

      }
      else{
        $.notify("Error adding "+frequency.frequency,'error')
      }
    });
    
    $('#editfrequency').foundation('reveal', 'close');

    }

  }

  $scope.delete=function(id){
    var d=window.confirm('Are you sure want to delete ');
    if (d){
        $http.post( SERVER_DOMAIN + "/delete/frequency",id).then(function(response){
        $http.get(SERVER_DOMAIN+'/all/frequencies/').then(function(response){
        $scope.frequencies = response.data.frequencies
    })
    })
    }
  }

}


function HookviewCtrl($scope,$http) {
  $http.get(SERVER_DOMAIN+'/all/hooks/').then(function(response){
     $scope.hooks = response.data.hooks
    })
  $http.get(SERVER_DOMAIN+'/get/formats/').then(function(response){
     $scope.formats = response.data.formats
    })

  $scope.edit=function(id){
    var fname;
    console.log(id)
    $('#edithook').foundation('reveal', 'open');
    $http.get(SERVER_DOMAIN+'/gets/hook/'+id).then(function(response){
    console.log(response.data.hook)
     $scope.edithook=response.data.hook
     fname=$scope.edithook.format
    })

    $scope.save=function(hook){
      if(hook['format']!=fname){
        hook['format']=hook.format['name'];
      }
      console.log(hook)
    $http.post( SERVER_DOMAIN + "/edit/hook",hook).then(function(data){
      if(data.data.status == 'success'){
        $.notify("Edited "+data.data.data.hook,'success')
        $scope.edithook = {}
        $http.get(SERVER_DOMAIN+'/all/hooks/').then(function(response){
          $scope.hooks = response.data.hooks
        })
      }
      else{
        $.notify("Error adding "+hook.hook,'error')
      }
    });
    $('#edithook').foundation('reveal', 'close');

    }

  }

  $scope.delete=function(id){
    var d=window.confirm('Are you sure want to delete ');
    if (d){
    $http.get(SERVER_DOMAIN+'/gets/hook/'+id).then(function(response){
    
     $scope.hook=response.data.hook
     
      console.log($scope.hook)
      $http.post( SERVER_DOMAIN + "/delete/hook",$scope.hook).then(function(data){
        if(data.data.status == 'success'){
        $.notify("Edited ",'success')
        $http.get(SERVER_DOMAIN+'/all/hooks/').then(function(response){
        $scope.hooks = response.data.hooks
      })
      }
      else{
        $.notify("Error",'error')
      }
      })
    })
    }
  }

}



function PositionviewCtrl($scope,$http,FormatIds) {
  $http.get(SERVER_DOMAIN+'/all/positions/').then(function(response){
     $scope.positions = response.data.positions;
      })
  $http.get(SERVER_DOMAIN+'/get/formats/').then(function(response){
     $scope.formats = response.data.formats
    })

  $scope.select_format=function(format,value){
     if(value==true){
          
          FormatIds.push(format.uid);
          console.log(FormatIds)
     }
     else{
         
          var index=FormatIds.indexOf(format.uid)
          FormatIds.splice(index,1);  
          console.log(FormatIds)
     }
    }

  $scope.edit=function(id){
    console.log(id)
    $('#editslogan').foundation('reveal', 'open');
    $http.get(SERVER_DOMAIN+'/gets/position/'+id).then(function(response){
     $scope.editposition=response.data.position;
     FormatIds=$scope.editposition.formatIds;
     console.log(FormatIds)
    })

    $scope.save=function(position){
      position.formatIds=FormatIds;
      console.log(position)
      $http.post( SERVER_DOMAIN + "/edit/position",position).then(function(data){
      if(data.data.status == 'success'){
        $.notify("Edited "+data.data.data.name,'success')
        $scope.editposition = {}
        $http.get(SERVER_DOMAIN+'/all/positions/').then(function(response){
        $scope.positions = response.data.positions;
      

     
    })
        
      }
      else{
        $.notify("Error adding "+position.name,'error')
      }
    });
    
    $('#editslogan').foundation('reveal', 'close');

    }

  }

  $scope.delete=function(id){
    var d=window.confirm('Are you sure want to delete ');
    if (d){
        $http.post( SERVER_DOMAIN + "/delete/position",id).then(function(response){
        $http.get(SERVER_DOMAIN+'/all/positions/').then(function(response){
     $scope.positions = response.data.positions;
      })
    })
    }
  }

}



function StationviewCtrl($scope,$http,FormatIds) {
  $http.get(SERVER_DOMAIN+'/all/stations/').then(function(response){
     $scope.stations = response.data.stations;
       })
  $http.get(SERVER_DOMAIN+'/get/formats/').then(function(response){
     $scope.formats = response.data.formats
    })

  $scope.select_format=function(format,value){
     if(value==true){
          
          FormatIds.push(format.uid);
          console.log(FormatIds)
     }
     else{
         
          var index=FormatIds.indexOf(format.uid)
          FormatIds.splice(index,1);  
          console.log(FormatIds)
     }
    }

  $scope.edit=function(id){
    console.log(id)
    $('#editstation').foundation('reveal', 'open');
    $http.get(SERVER_DOMAIN+'/gets/station/'+id).then(function(response){
     $scope.editstation=response.data.station;
     FormatIds=$scope.editstation.formatIds;
     console.log(FormatIds)
    })

    $scope.save=function(station){
      station.formatIds=FormatIds;
      console.log(station)
      $http.post( SERVER_DOMAIN + "/edit/station",station).then(function(data){
      if(data.data.status == 'success'){
        $.notify("Edited "+data.data.data.name,'success')
        $scope.editstation = {}
        $http.get(SERVER_DOMAIN+'/all/stations/').then(function(response){
        $scope.stations = response.data.stations;
      

     
    })
        
      }
      else{
        $.notify("Error adding "+station.name,'error')
      }
    });
    
    $('#editstation').foundation('reveal', 'close');

    }

  }
  $scope.delete=function(id){
    var d=window.confirm('Are you sure want to delete ');
    if (d){
      $http.post( SERVER_DOMAIN + "/delete/station",id).then(function(response){
        $http.get(SERVER_DOMAIN+'/all/stations/').then(function(response){
     $scope.stations = response.data.stations;
       })
    })
    }
  }
  

}

function HooktempviewCtrl($scope,$http,FormatIds,PosVoiceIds,FreVoiceIds,StatVoiceIds,PosStyleIds,FreStyleIds,StatStyleIds) {
  $http.get(SERVER_DOMAIN+'/all/hooktemps/').then(function(response){
     $scope.hooktemps = response.data.hooktemps
    })
  $http.get(SERVER_DOMAIN+'/get/formats/').then(function(response){
     $scope.formats = response.data.formats
    })
  $http.get(SERVER_DOMAIN+'/get/voices/').then(function(response){
     $scope.voices = response.data.voices
    })
  $http.get(SERVER_DOMAIN+'/get/styles/').then(function(response){
     $scope.styles = response.data.styles
    })

  $scope.select_format=function(format,value){
     if(value==true){
          
          FormatIds.push(format.uid);
          console.log(FormatIds)
     }
     else{
         
          var index=FormatIds.indexOf(format.uid)
          FormatIds.splice(index,1);  
          console.log(FormatIds)
     }
    }

    $scope.select_posvoice=function(voice,value1){
     if(value1==true){
          
          PosVoiceIds.push(voice.uid);
          console.log(PosVoiceIds)
     }
     else{
         
          var index=PosVoiceIds.indexOf(voice.uid)
          PosVoiceIds.splice(index,1);  
          console.log(PosVoiceIds)
     }
    }

    $scope.select_frevoice=function(voice,value5){
     if(value5==true){
          
          FreVoiceIds.push(voice.uid);
          console.log(FreVoiceIds)
     }
     else{
         
          var index=FreVoiceIds.indexOf(voice.uid)
          FreVoiceIds.splice(index,1);  
          console.log(FreVoiceIds)
     }
    }
    $scope.select_statvoice=function(voice,value3){
     if(value3==true){
          
          StatVoiceIds.push(voice.uid);
          console.log(StatVoiceIds)
     }
     else{
         
          var index=StatVoiceIds.indexOf(voice.uid)
          StatVoiceIds.splice(index,1);  
          console.log(StatVoiceIds)
     }
    }
    $scope.select_posstyle=function(style,value2){
     if(value2==true){
          
          PosStyleIds.push(style.uid);
          console.log(PosStyleIds)
     }
     else{
         
          var index=PosStyleIds.indexOf(style.uid)
          PosStyleIds.splice(index,1);  
          console.log(PosStyleIds)
     }
    }
    $scope.select_frestyle=function(style,value6){
     if(value6==true){
          
          FreStyleIds.push(style.uid);
          console.log(FreStyleIds)
     }
     else{
         
          var index=FreStyleIds.indexOf(style.uid)
          FreStyleIds.splice(index,1);  
          console.log(FreStyleIds)
     }
    }

    $scope.select_statstyle=function(style,value4){
     if(value4==true){
          
          StatStyleIds.push(style.uid);
          console.log(StatStyleIds)
     }
     else{
         
          var index=StatStyleIds.indexOf(style.uid)
          StatStyleIds.splice(index,1);  
          console.log(StatStyleIds)
     }
    }

  $scope.edit=function(id){
    console.log(id)
    $('#edithooktemp').foundation('reveal', 'open');
    $http.get(SERVER_DOMAIN+'/gets/hooktemp/'+id).then(function(response){
    console.log(response.data.hooktemp)
     $scope.edithooktemp=response.data.hooktemp
      FormatIds=$scope.edithooktemp.formatids;
      PosVoiceIds=$scope.edithooktemp.posVoiceids;
      PosStyleIds=$scope.edithooktemp.posStyleids;
      FreVoiceIds=$scope.edithooktemp.freVoiceids;
      FreStyleIds=$scope.edithooktemp.freStyleids;
      StatVoiceIds=$scope.edithooktemp.statVoiceids;
      StatStyleIds=$scope.edithooktemp.statStyleids;

    })

    $scope.save=function(hooktemp){
      hooktemp.formatids=FormatIds;
      hooktemp.posVoiceids=PosVoiceIds;
      hooktemp.posStyleids=PosStyleIds;
      hooktemp.freVoiceids=FreVoiceIds;
      hooktemp.freStyleids=FreStyleIds;
      hooktemp.statVoiceids=StatVoiceIds;
      hooktemp.statStyleids=StatStyleIds;
      console.log(hooktemp)
      $http.post( SERVER_DOMAIN + "/edit/hooktemp",hooktemp).then(function(data){
      if(data.data.status == 'success'){
        $.notify("Edited "+data.data.data.name,'success')
        $scope.edithooktemp = {}
        $http.get(SERVER_DOMAIN+'/all/hooktemps/').then(function(response){
     $scope.hooktemps = response.data.hooktemps
    })

      }
      else{
        $.notify("Error adding "+hooktemp.name,'error')
      }
    });
    
    $('#edithooktemp').foundation('reveal', 'close');

    }

  }

  $scope.delete=function(id){
    var d=window.confirm('Are you sure want to delete ');
    if (d){
        $http.post( SERVER_DOMAIN + "/delete/hooktemplate",id).then(function(response){
        $http.get(SERVER_DOMAIN+'/all/hooktemps/').then(function(response){
     $scope.hooktemps = response.data.hooktemps
    })
    })
    }
  }

}

function TemplateviewCtrl($scope,$http,FormatIds,PosVoiceIds,FreVoiceIds,StatVoiceIds,PosStyleIds,FreStyleIds,StatStyleIds) {
  $http.get(SERVER_DOMAIN+'/all/templates/').then(function(response){
     $scope.templates = response.data.templates
    })
  $http.get(SERVER_DOMAIN+'/get/formats/').then(function(response){
     $scope.formats = response.data.formats
    })
  $http.get(SERVER_DOMAIN+'/get/voices/').then(function(response){
     $scope.voices = response.data.voices
    })
  $http.get(SERVER_DOMAIN+'/get/styles/').then(function(response){
     $scope.styles = response.data.styles
    })

  $scope.select_format=function(format,value){
     if(value==true){
          
          FormatIds.push(format.uid);
          console.log(FormatIds)
     }
     else{
         
          var index=FormatIds.indexOf(format.uid)
          FormatIds.splice(index,1);  
          console.log(FormatIds)
     }
    }

    $scope.select_posvoice=function(voice,value1){
     if(value1==true){
          
          PosVoiceIds.push(voice.uid);
          console.log(PosVoiceIds)
     }
     else{
         
          var index=PosVoiceIds.indexOf(voice.uid)
          PosVoiceIds.splice(index,1);  
          console.log(PosVoiceIds)
     }
    }

    $scope.select_frevoice=function(voice,value5){
     if(value5==true){
          
          FreVoiceIds.push(voice.uid);
          console.log(FreVoiceIds)
     }
     else{
         
          var index=FreVoiceIds.indexOf(voice.uid)
          FreVoiceIds.splice(index,1);  
          console.log(FreVoiceIds)
     }
    }
    $scope.select_statvoice=function(voice,value3){
     if(value3==true){
          
          StatVoiceIds.push(voice.uid);
          console.log(StatVoiceIds)
     }
     else{
         
          var index=StatVoiceIds.indexOf(voice.uid)
          StatVoiceIds.splice(index,1);  
          console.log(StatVoiceIds)
     }
    }
    $scope.select_posstyle=function(style,value2){
     if(value2==true){
          
          PosStyleIds.push(style.uid);
          console.log(PosStyleIds)
     }
     else{
         
          var index=PosStyleIds.indexOf(style.uid)
          PosStyleIds.splice(index,1);  
          console.log(PosStyleIds)
     }
    }
    $scope.select_frestyle=function(style,value6){
     if(value6==true){
          
          FreStyleIds.push(style.uid);
          console.log(FreStyleIds)
     }
     else{
         
          var index=FreStyleIds.indexOf(style.uid)
          FreStyleIds.splice(index,1);  
          console.log(FreStyleIds)
     }
    }

    $scope.select_statstyle=function(style,value4){
     if(value4==true){
          
          StatStyleIds.push(style.uid);
          console.log(StatStyleIds)
     }
     else{
         
          var index=StatStyleIds.indexOf(style.uid)
          StatStyleIds.splice(index,1);  
          console.log(StatStyleIds)
     }
    }

  $scope.edit=function(id){
    console.log(id)
    $('#edittemplate').foundation('reveal', 'open');
    $http.get(SERVER_DOMAIN+'/gets/template/'+id).then(function(response){
    console.log(response.data.template)
     $scope.edittemplate=response.data.template
      FormatIds=$scope.edittemplate.formatids;
      PosVoiceIds=$scope.edittemplate.posVoiceids;
      PosStyleIds=$scope.edittemplate.posStyleids;
      FreVoiceIds=$scope.edittemplate.freVoiceids;
      FreStyleIds=$scope.edittemplate.freStyleids;
      StatVoiceIds=$scope.edittemplate.statVoiceids;
      StatStyleIds=$scope.edittemplate.statStyleids;

    })

    $scope.save=function(template){
      template.formatids=FormatIds;
      template.posVoiceids=PosVoiceIds;
      template.posStyleids=PosStyleIds;
      template.freVoiceids=FreVoiceIds;
      template.freStyleids=FreStyleIds;
      template.statVoiceids=StatVoiceIds;
      template.statStyleids=StatStyleIds;
      console.log(template)
      $http.post( SERVER_DOMAIN + "/edit/template",template).then(function(data){
      if(data.data.status == 'success'){
        $.notify("Edited "+data.data.data.name,'success')
        $scope.edittemplate = {}
        $http.get(SERVER_DOMAIN+'/all/templates/').then(function(response){
     $scope.templates = response.data.templates
    })

      }
      else{
        $.notify("Error adding "+template.name,'error')
      }
    });
    
    $('#edittemplate').foundation('reveal', 'close');

    }

  }

  $scope.delete=function(id){
    var d=window.confirm('Are you sure want to delete ');
    if (d){
      $http.post( SERVER_DOMAIN + "/delete/template",id).then(function(response){
       $http.get(SERVER_DOMAIN+'/all/templates/').then(function(response){
     $scope.templates = response.data.templates
    })
    })
    }
  }

}



function SfpbatchCtrl($scope,$http) {
  $scope.name = 'SFP';
  $http.get(SERVER_DOMAIN+'/get/formats/').then(function(response){
     $scope.formats = response.data.formats
    })
  $http.get(SERVER_DOMAIN+'/get/voices/').then(function(response){
     $scope.voices = response.data.voices
    })
  $scope.update = function(sfp){
      console.log(sfp)
      $http.post( SERVER_DOMAIN + "/update/sfp",sfp).then(function(data){
        if(data.data.status == 'success'){
          $.notify("updated",'success')
         
        }
        else{
          $.notify("Error ",'error')
        }
      });
    }


}

function SfbatchCtrl($scope,$http) {
  $scope.name = 'SF';
  $http.get(SERVER_DOMAIN+'/get/formats/').then(function(response){
     $scope.formats = response.data.formats
    })
  $http.get(SERVER_DOMAIN+'/get/voices/').then(function(response){
     $scope.voices = response.data.voices
    })
  $scope.update = function(sf){
      console.log(sf)
      $http.post( SERVER_DOMAIN + "/update/sf",sf).then(function(data){
        if(data.data.status == 'success'){
          $.notify("updated",'success')
          
        }
        else{
          $.notify("Error ",'error')
        }
      });
    }

}

function StationbatchCtrl($scope,$http) {
  $scope.name = 'Station';
  $http.get(SERVER_DOMAIN+'/get/formats/').then(function(response){
     $scope.formats = response.data.formats
    })
  $http.get(SERVER_DOMAIN+'/get/voices/').then(function(response){
     $scope.voices = response.data.voices
    })
  $scope.update = function(station){
      console.log(station)
      $http.post( SERVER_DOMAIN + "/update/station",station).then(function(data){
        if(data.data.status == 'success'){
          $.notify("updated",'success')
          
        }
        else{
          $.notify("Error ",'error')
        }
      });
    }

}

function FrequencybatchCtrl($scope,$http) {
  $scope.name = 'Frequency';
  $http.get(SERVER_DOMAIN+'/get/formats/').then(function(response){
     $scope.formats = response.data.formats
    })
  $http.get(SERVER_DOMAIN+'/get/voices/').then(function(response){
     $scope.voices = response.data.voices
    })
  $scope.update = function(frequency){
      console.log(frequency)
      $http.post( SERVER_DOMAIN + "/update/frequency",frequency).then(function(data){
        if(data.data.status == 'success'){
          $.notify("updated",'success')
          
        }
        else{
          $.notify("Error ",'error')
        }
      });
    }

}

function PositionbatchCtrl($scope,$http) {
  $scope.name = 'Position Statement';
  $http.get(SERVER_DOMAIN+'/get/formats/').then(function(response){
     $scope.formats = response.data.formats
    })
  $http.get(SERVER_DOMAIN+'/get/voices/').then(function(response){
     $scope.voices = response.data.voices
    })
  $scope.update = function(position){
      console.log(position)
      $http.post( SERVER_DOMAIN + "/update/position",position).then(function(data){
        if(data.data.status == 'success'){
          $.notify("updated",'success')
          
        }
        else{
          $.notify("Error ",'error')
        }
      });
    }

}